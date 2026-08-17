from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from synapsemd_platform.audit.chain import verify_chain
from synapsemd_platform.audit.events import (
    AuditEventPayload,
    AuditProducer,
    fetch_persisted_events,
    filter_audit_events,
    query_audit_events,
)
from synapsemd_platform.core.config import Settings, get_settings
from synapsemd_platform.core.database import async_session_factory
from synapsemd_platform.models.audit import AppendOnlyError, AuditEvent


@pytest.mark.asyncio
async def test_audit_persists_and_chain_survives_producer_restart(app) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    producer = AuditProducer()
    producer.settings = Settings(audit_use_memory=False)
    first = await producer.emit(
        AuditEventPayload(
            event_type="test.persist",
            tenant_id=str(tenant_id),
            user_id=str(user_id),
            resource={"command": "gout"},
        )
    )
    second = await producer.emit(
        AuditEventPayload(
            event_type="test.persist",
            tenant_id=str(tenant_id),
            user_id=str(user_id),
            resource={"command": "allergy"},
        )
    )
    assert first["event_hash"]
    assert second["prev_hash"] == first["event_hash"]
    assert producer.get_events() == []

    restarted = AuditProducer()
    restarted.settings = Settings(audit_use_memory=False)
    async with async_session_factory() as session:
        events = await fetch_persisted_events(session, tenant_id)
    assert len(events) == 2
    verify_chain(events, secret=producer.settings.jwt_secret)
    assert restarted.get_events() == []
    assert UUID(events[0]["tenant_id"]) == tenant_id


@pytest.mark.asyncio
async def test_audit_event_orm_update_is_append_only(app) -> None:
    async with async_session_factory() as session:
        row = AuditEvent(
            tenant_id=uuid4(),
            event_type="test.append",
            payload={"outcome": "success"},
        )
        session.add(row)
        await session.commit()
        row.event_type = "tampered"
        with pytest.raises(AppendOnlyError):
            await session.commit()


def test_filter_audit_events_by_command_and_type() -> None:
    now = datetime(2026, 8, 17, 10, 0, tzinfo=UTC)
    events = [
        {
            "event_type": "ai.command.executed",
            "user_id": "u1",
            "resource": {"command": "gout"},
            "occurred_at": now,
        },
        {
            "event_type": "authz.denied",
            "user_id": "u2",
            "resource": {"command": "goal"},
            "occurred_at": "2026-08-17T11:00:00",
        },
        {
            "event_type": "ai.command.executed",
            "user_id": "u1",
            "resource": {"command": "allergy"},
            "occurred_at": "not-a-date",
        },
    ]
    filtered = filter_audit_events(events, event_type="ai.command.executed", command="gout")
    assert len(filtered) == 1
    assert filtered[0]["user_id"] == "u1"
    assert filter_audit_events(events, user_id="u2")[0]["event_type"] == "authz.denied"
    assert filter_audit_events(events, command="missing") == []
    assert filter_audit_events(events, since=now + timedelta(hours=2)) == []
    assert filter_audit_events(events, until=now - timedelta(hours=1)) == []


@pytest.mark.asyncio
async def test_query_audit_events_reads_db_without_session(
    app, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("AUDIT_USE_MEMORY", "false")
    get_settings.cache_clear()
    tenant_id = uuid4()
    user_id = uuid4()
    producer = AuditProducer()
    producer.settings = get_settings()
    await producer.emit(
        AuditEventPayload(
            event_type="test.query",
            tenant_id=str(tenant_id),
            user_id=str(user_id),
            resource={"command": "gout"},
        )
    )
    events = await query_audit_events(
        tenant_id=str(tenant_id),
        event_type="test.query",
        user_id=str(user_id),
        command="gout",
        since=datetime.now(UTC) - timedelta(minutes=5),
        until=datetime.now(UTC) + timedelta(minutes=5),
    )
    assert len(events) == 1
    async with async_session_factory() as session:
        via_session = await query_audit_events(
            tenant_id=str(tenant_id),
            session=session,
            command="gout",
        )
    assert len(via_session) == 1
    assert await query_audit_events(tenant_id="not-a-uuid") == []
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_audit_event_orm_delete_is_append_only(app) -> None:
    async with async_session_factory() as session:
        row = AuditEvent(
            tenant_id=uuid4(),
            event_type="test.append",
            payload={"outcome": "success"},
        )
        session.add(row)
        await session.commit()
        await session.delete(row)
        with pytest.raises(AppendOnlyError):
            await session.commit()
