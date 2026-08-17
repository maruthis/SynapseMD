"""CI restore drill: dump identity rows and restore into a fresh database (E-5)."""

from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.core.database import Base
from synapsemd_platform.jobs.backup_restore import dump_identity, restore_identity
from synapsemd_platform.models.tenant import Tenant, User


@pytest.mark.asyncio
async def test_identity_dump_restore_drill() -> None:
    source = create_async_engine("sqlite+aiosqlite:///:memory:")
    target = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with source.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with target.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    tenant_id = uuid4()
    user_id = uuid4()
    src_factory = async_sessionmaker(source, class_=AsyncSession, expire_on_commit=False)
    dst_factory = async_sessionmaker(target, class_=AsyncSession, expire_on_commit=False)

    async with src_factory() as session:
        session.add(Tenant(id=tenant_id, name="Drill Clinic", plan="starter"))
        session.add(
            User(id=user_id, tenant_id=tenant_id, email_hash="drill", role="patient")
        )
        await session.commit()
        payload = await dump_identity(session)

    async with dst_factory() as session:
        counts = await restore_identity(session, payload)
        assert counts["tenants"] == 1
        assert counts["users"] == 1
        restored = await session.get(Tenant, tenant_id)
        assert restored is not None
        assert restored.name == "Drill Clinic"
        user = await session.get(User, user_id)
        assert user is not None
        assert user.email_hash == "drill"

    await source.dispose()
    await target.dispose()
