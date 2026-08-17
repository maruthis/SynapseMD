"""Time-boxed break-glass elevation with extra audit + notify stub."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.audit.events import AuditEventPayload, audit_producer
from synapsemd_platform.models.iam import BreakGlassGrant

DEFAULT_MINUTES = 15
MAX_MINUTES = 60


async def activate_break_glass(
    db: AsyncSession,
    *,
    user_id: UUID,
    tenant_id: UUID,
    reason: str,
    minutes: int = DEFAULT_MINUTES,
) -> BreakGlassGrant:
    duration = max(1, min(minutes, MAX_MINUTES))
    grant = BreakGlassGrant(
        tenant_id=tenant_id,
        user_id=user_id,
        reason=reason.strip() or "unspecified",
        expires_at=datetime.now(UTC) + timedelta(minutes=duration),
        notified=True,
    )
    db.add(grant)
    await db.commit()
    await db.refresh(grant)
    await audit_producer.emit(
        AuditEventPayload(
            event_type="auth.break_glass.activated",
            tenant_id=str(tenant_id),
            user_id=str(user_id),
            resource={
                "grant_id": str(grant.id),
                "minutes": duration,
                "notify": True,
            },
            outcome="success",
        )
    )
    return grant


def is_grant_active(grant: BreakGlassGrant, *, now: datetime | None = None) -> bool:
    moment = now or datetime.now(UTC)
    expires = grant.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=UTC)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return expires > moment
