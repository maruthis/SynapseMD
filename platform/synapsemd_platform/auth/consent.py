"""Consent lookup for LLM processing purpose."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.core.config import get_settings
from synapsemd_platform.models.governance import LLM_PROCESSING_PURPOSE, Consent


async def llm_processing_allowed(
    session: AsyncSession,
    *,
    tenant_id: UUID,
    user_id: UUID,
) -> bool:
    result = await session.execute(
        select(Consent).where(
            Consent.tenant_id == tenant_id,
            Consent.user_id == user_id,
            Consent.purpose == LLM_PROCESSING_PURPOSE,
        )
    )
    row = result.scalar_one_or_none()
    if row is not None:
        return bool(row.granted)
    return not get_settings().is_production_like()


async def upsert_consent(
    session: AsyncSession,
    *,
    tenant_id: UUID,
    user_id: UUID,
    purpose: str,
    granted: bool,
    source: str = "explicit",
) -> Consent:
    result = await session.execute(
        select(Consent).where(
            Consent.tenant_id == tenant_id,
            Consent.user_id == user_id,
            Consent.purpose == purpose,
        )
    )
    row = result.scalar_one_or_none()
    if row is None:
        row = Consent(
            tenant_id=tenant_id,
            user_id=user_id,
            purpose=purpose,
            granted=granted,
            source=source,
        )
        session.add(row)
    else:
        row.granted = granted
        row.source = source
    await session.commit()
    await session.refresh(row)
    return row
