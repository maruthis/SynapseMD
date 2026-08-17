"""Refresh-token sessions (opaque token, hashed at rest, rotated on use)."""

from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.auth.jwt import create_access_token
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.models.iam import Session


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def new_refresh_token() -> str:
    return secrets.token_urlsafe(48)


async def create_session(
    db: AsyncSession,
    *,
    user_id: UUID,
    tenant_id: UUID,
) -> tuple[Session, str]:
    settings = get_settings()
    raw = new_refresh_token()
    session = Session(
        tenant_id=tenant_id,
        user_id=user_id,
        refresh_token_hash=hash_refresh_token(raw),
        expires_at=datetime.now(UTC) + timedelta(days=settings.jwt_refresh_expire_days),
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session, raw


async def rotate_refresh_token(db: AsyncSession, refresh_token: str) -> Session | None:
    hashed = hash_refresh_token(refresh_token)
    result = await db.execute(select(Session).where(Session.refresh_token_hash == hashed))
    current = result.scalar_one_or_none()
    if current is None or current.revoked_at is not None:
        return None
    if _as_utc(current.expires_at) < datetime.now(UTC):
        return None
    current.revoked_at = datetime.now(UTC)
    await db.commit()
    return current


async def issue_token_pair(
    db: AsyncSession,
    *,
    user_id: UUID,
    tenant_id: UUID,
    roles: list[str],
    scopes: list[str],
    amr: list[str] | None = None,
    purpose: str = "treatment",
    llm_processing: bool = True,
) -> dict[str, str | int]:
    settings = get_settings()
    access = create_access_token(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=roles,
        scopes=scopes,
        amr=amr,
        purpose=purpose,
        llm_processing=llm_processing,
    )
    _, refresh = await create_session(db, user_id=user_id, tenant_id=tenant_id)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": settings.jwt_expire_minutes * 60,
    }
