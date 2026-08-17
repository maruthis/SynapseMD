"""Postgres append-only trigger on audit_events (C-6)."""

from __future__ import annotations

import os
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.audit.append_only import apply_audit_append_only
from synapsemd_platform.core.database import Base
from synapsemd_platform.core.rls import RLS_SQL, set_rls_context
from synapsemd_platform.models import audit as audit_models  # noqa: F401
from synapsemd_platform.models.audit import AuditEvent


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_postgres_rejects_audit_update() -> None:
    url = os.environ.get("POSTGRES_TEST_URL")
    if not url:
        pytest.skip("POSTGRES_TEST_URL not set")

    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(RLS_SQL))
        await apply_audit_append_only(conn)

    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    tenant_id = uuid4()
    user_id = uuid4()
    async with factory() as session:
        async with session.begin():
            await set_rls_context(session, tenant_id, user_id)
            session.add(
                AuditEvent(
                    tenant_id=tenant_id,
                    user_id=user_id,
                    event_type="test.append",
                    payload={"outcome": "success"},
                    partition_month="2026-08",
                )
            )

    async with factory() as session:
        async with session.begin():
            await set_rls_context(session, tenant_id, user_id)
            with pytest.raises(Exception, match="append-only"):
                await session.execute(
                    text("UPDATE audit_events SET event_type = 'tampered' WHERE tenant_id = :tid"),
                    {"tid": str(tenant_id)},
                )

    await engine.dispose()
