from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.anonymization.scrubber import scrub_audit_payload
from synapsemd_platform.audit.chain import (
    GENESIS_HASH,
    chain_day,
    compute_event_hash,
    partition_month,
)
from synapsemd_platform.audit.kafka_sink import KafkaAuditSink
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.rls import set_rls_context
from synapsemd_platform.observability.metrics import AUDIT_WRITE_FAILURE_COUNT

logger = logging.getLogger(__name__)


@dataclass
class AuditEventPayload:
    event_type: str
    tenant_id: str
    user_id: str | None
    resource: dict[str, Any] = field(default_factory=dict)
    ai: dict[str, Any] = field(default_factory=dict)
    outcome: str = "success"


def _parse_uuid(value: str | None) -> UUID | None:
    if not value:
        return None
    try:
        return UUID(str(value))
    except ValueError:
        return None


def _event_time(event: dict[str, Any]) -> datetime | None:
    raw = event.get("occurred_at") or event.get("created_at")
    if isinstance(raw, datetime):
        return raw if raw.tzinfo else raw.replace(tzinfo=UTC)
    if isinstance(raw, str):
        try:
            stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
        return stamp if stamp.tzinfo else stamp.replace(tzinfo=UTC)
    return None


def filter_audit_events(
    events: list[dict[str, Any]],
    *,
    event_type: str | None = None,
    user_id: str | None = None,
    command: str | None = None,
    since: datetime | None = None,
    until: datetime | None = None,
) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for event in events:
        if event_type and event.get("event_type") != event_type:
            continue
        if user_id and str(event.get("user_id") or "") != str(user_id):
            continue
        if command:
            resource = event.get("resource") or {}
            if str(resource.get("command") or "") != command:
                continue
        stamp = _event_time(event)
        if since is not None and (stamp is None or stamp < since):
            continue
        if until is not None and (stamp is None or stamp > until):
            continue
        filtered.append(event)
    return filtered


def serialize_audit_row(row: Any) -> dict[str, Any]:
    payload = row.payload or {}
    return {
        "event_id": row.event_id,
        "event_type": row.event_type,
        "tenant_id": str(row.tenant_id),
        "user_id": str(row.user_id) if row.user_id else None,
        "resource": payload.get("resource") or {},
        "ai": payload.get("ai") or {},
        "outcome": payload.get("outcome"),
        "signature": row.signature,
        "event_hash": row.event_hash,
        "prev_hash": row.prev_hash,
        "occurred_at": row.occurred_at.isoformat() if row.occurred_at else None,
        "partition_month": row.partition_month,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


class AuditProducer:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._memory_events: list[dict[str, Any]] = []
        self._chain_heads: dict[tuple[str, str], str] = {}
        self._kafka_sink: KafkaAuditSink | None = None
        if self.settings.audit_use_kafka:
            self._kafka_sink = KafkaAuditSink(
                self.settings.kafka_bootstrap_servers,
                self.settings.kafka_audit_topic,
            )

    def _sign(self, payload: dict[str, Any]) -> str:
        import hashlib
        import hmac
        import json

        body = json.dumps(payload, sort_keys=True, default=str)
        return hmac.new(
            self.settings.jwt_secret.encode(),
            body.encode(),
            hashlib.sha256,
        ).hexdigest()

    def _next_prev_hash(self, tenant_id: str, day: str) -> str:
        return self._chain_heads.get((tenant_id, day), GENESIS_HASH)

    async def _load_prev_hash_from_db(self, tenant_id: str, day: str, user_id: str | None) -> str:
        tenant_uuid = _parse_uuid(tenant_id)
        if tenant_uuid is None:
            return GENESIS_HASH
        from synapsemd_platform.core.database import async_session_factory
        from synapsemd_platform.models.audit import AuditEvent

        start = datetime.fromisoformat(f"{day}T00:00:00+00:00")
        end = start + timedelta(days=1)
        user_uuid = _parse_uuid(user_id) or tenant_uuid
        async with async_session_factory() as session:
            async with session.begin():
                await set_rls_context(session, tenant_uuid, user_uuid)
                result = await session.execute(
                    select(AuditEvent.event_hash)
                    .where(
                        AuditEvent.tenant_id == tenant_uuid,
                        AuditEvent.occurred_at >= start,
                        AuditEvent.occurred_at < end,
                        AuditEvent.event_hash.is_not(None),
                    )
                    .order_by(AuditEvent.occurred_at.desc())
                    .limit(1)
                )
                last = result.scalar_one_or_none()
        return last or GENESIS_HASH

    async def _prev_hash(self, tenant_id: str, day: str, user_id: str | None) -> str:
        cached = self._chain_heads.get((tenant_id, day))
        if cached is not None:
            return cached
        if self.settings.audit_use_memory:
            return GENESIS_HASH
        return await self._load_prev_hash_from_db(tenant_id, day, user_id)

    async def emit(self, event: AuditEventPayload) -> dict[str, Any]:
        now = datetime.now(UTC)
        event_id = f"evt_{uuid4().hex[:12]}"
        record = scrub_audit_payload(
            {
                "event_type": event.event_type,
                "tenant_id": event.tenant_id,
                "user_id": event.user_id,
                "resource": event.resource,
                "ai": event.ai,
                "outcome": event.outcome,
            }
        )
        chain_payload = {
            "event_type": record.get("event_type"),
            "tenant_id": record.get("tenant_id"),
            "user_id": record.get("user_id"),
            "resource": record.get("resource") or {},
            "ai": record.get("ai") or {},
            "outcome": record.get("outcome"),
            "event_id": event_id,
        }
        day = chain_day(now)
        prev_hash = await self._prev_hash(event.tenant_id, day, event.user_id)
        event_hash = compute_event_hash(prev_hash, chain_payload, secret=self.settings.jwt_secret)
        record["event_id"] = event_id
        record["prev_hash"] = prev_hash
        record["event_hash"] = event_hash
        record["occurred_at"] = now.isoformat()
        record["partition_month"] = partition_month(now)
        record["signature"] = self._sign(record)
        self._chain_heads[(event.tenant_id, day)] = event_hash

        if self.settings.audit_use_memory:
            self._memory_events.append(record)
        else:
            try:
                await self._persist(record, now)
            except Exception:
                AUDIT_WRITE_FAILURE_COUNT.inc()
                logger.exception("audit persist failed")
                self._memory_events.append(record)
        if self._kafka_sink is not None:
            self._kafka_sink.publish(record)
        return record

    async def _persist(self, record: dict[str, Any], occurred_at: datetime) -> None:
        tenant_uuid = _parse_uuid(str(record.get("tenant_id")))
        if tenant_uuid is None:
            # Tests and non-UUID tenants stay off the durable path.
            return
        from synapsemd_platform.core.database import async_session_factory
        from synapsemd_platform.models.audit import AuditEvent

        user_uuid = _parse_uuid(record.get("user_id"))
        row = AuditEvent(
            tenant_id=tenant_uuid,
            user_id=user_uuid,
            event_type=str(record.get("event_type")),
            payload={
                "resource": record.get("resource") or {},
                "ai": record.get("ai") or {},
                "outcome": record.get("outcome"),
            },
            signature=record.get("signature"),
            event_id=record.get("event_id"),
            event_hash=record.get("event_hash"),
            prev_hash=record.get("prev_hash"),
            occurred_at=occurred_at,
            partition_month=record.get("partition_month"),
        )
        async with async_session_factory() as session:
            async with session.begin():
                await set_rls_context(session, tenant_uuid, user_uuid or tenant_uuid)
                session.add(row)

    def get_events(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        if tenant_id is None:
            return list(self._memory_events)
        return [e for e in self._memory_events if e.get("tenant_id") == tenant_id]


async def fetch_persisted_events(
    session: AsyncSession,
    tenant_id: UUID,
    *,
    event_type: str | None = None,
    user_id: str | None = None,
    command: str | None = None,
    since: datetime | None = None,
    until: datetime | None = None,
) -> list[dict[str, Any]]:
    from synapsemd_platform.models.audit import AuditEvent

    stmt = select(AuditEvent).where(AuditEvent.tenant_id == tenant_id)
    if event_type:
        stmt = stmt.where(AuditEvent.event_type == event_type)
    user_uuid = _parse_uuid(user_id)
    if user_uuid is not None:
        stmt = stmt.where(AuditEvent.user_id == user_uuid)
    if since is not None:
        stmt = stmt.where(AuditEvent.occurred_at >= since)
    if until is not None:
        stmt = stmt.where(AuditEvent.occurred_at <= until)
    stmt = stmt.order_by(AuditEvent.occurred_at.asc())
    result = await session.execute(stmt)
    events = [serialize_audit_row(row) for row in result.scalars().all()]
    if command:
        events = filter_audit_events(events, command=command)
    return events


async def query_audit_events(
    *,
    tenant_id: str,
    event_type: str | None = None,
    user_id: str | None = None,
    command: str | None = None,
    since: datetime | None = None,
    until: datetime | None = None,
    session: AsyncSession | None = None,
) -> list[dict[str, Any]]:
    settings = get_settings()
    if settings.audit_use_memory:
        return filter_audit_events(
            audit_producer.get_events(tenant_id=tenant_id),
            event_type=event_type,
            user_id=user_id,
            command=command,
            since=since,
            until=until,
        )
    tenant_uuid = _parse_uuid(tenant_id)
    if tenant_uuid is None:
        return []
    if session is not None:
        return await fetch_persisted_events(
            session,
            tenant_uuid,
            event_type=event_type,
            user_id=user_id,
            command=command,
            since=since,
            until=until,
        )
    from synapsemd_platform.core.database import async_session_factory

    async with async_session_factory() as owned:
        async with owned.begin():
            await set_rls_context(owned, tenant_uuid, tenant_uuid)
            return await fetch_persisted_events(
                owned,
                tenant_uuid,
                event_type=event_type,
                user_id=user_id,
                command=command,
                since=since,
                until=until,
            )


audit_producer = AuditProducer()
