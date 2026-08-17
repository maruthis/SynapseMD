"""Postgres RLS negative tests — cross-tenant SELECT/INSERT denied."""

from __future__ import annotations

import os
from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.core.database import Base
from synapsemd_platform.core.rls import RLS_SQL, set_rls_context
from synapsemd_platform.models import clinical, governance, tenant, trackers  # noqa: F401
from synapsemd_platform.models.clinical import PatientProfile
from synapsemd_platform.models.trackers import AllergyRecord, GoutFlare

APP_ROLE = "synapsemd_app"


def _postgres_url() -> str | None:
    return os.environ.get("POSTGRES_TEST_URL")


def _app_role_url(url: str) -> str:
    return url.replace("://synapsemd:", f"://{APP_ROLE}:", 1)


async def _prepare_nonsuperuser_engine(url: str):
    """Compose/CI POSTGRES_USER is a superuser and bypasses RLS; tests use a login role."""
    admin = create_async_engine(url)
    async with admin.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(RLS_SQL))
        await conn.execute(
            text(
                f"""
                DO $$
                BEGIN
                  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{APP_ROLE}') THEN
                    CREATE ROLE {APP_ROLE} LOGIN PASSWORD 'synapsemd' NOSUPERUSER INHERIT;
                  END IF;
                END
                $$;
                """
            )
        )
        await conn.execute(text(f"GRANT USAGE, CREATE ON SCHEMA public TO {APP_ROLE}"))
        await conn.execute(text(f"GRANT ALL ON ALL TABLES IN SCHEMA public TO {APP_ROLE}"))
        await conn.execute(text(f"GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO {APP_ROLE}"))
    await admin.dispose()
    return create_async_engine(_app_role_url(url))


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_rls_denies_cross_tenant_clinical_and_trackers() -> None:
    url = _postgres_url()
    if not url:
        pytest.skip("POSTGRES_TEST_URL not set")

    engine = await _prepare_nonsuperuser_engine(url)

    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    tenant_a, tenant_b = uuid4(), uuid4()
    user_a, user_b = uuid4(), uuid4()

    async with factory() as session:
        async with session.begin():
            await set_rls_context(session, tenant_a, user_a)
            session.add(
                PatientProfile(
                    tenant_id=tenant_a,
                    user_id=user_a,
                    payload={"basic_info": {"gender": "M"}},
                )
            )
            session.add(
                AllergyRecord(
                    tenant_id=tenant_a,
                    user_id=user_a,
                    record_id="allergy_a",
                    allergen_name="penicillin",
                    payload={"id": "allergy_a"},
                )
            )
            session.add(
                GoutFlare(
                    tenant_id=tenant_a,
                    user_id=user_a,
                    record_id="gout_a",
                    joint="ankle",
                    payload={"id": "gout_a"},
                )
            )

    async with factory() as session:
        async with session.begin():
            await set_rls_context(session, tenant_b, user_b)
            profiles = (await session.execute(select(PatientProfile))).scalars().all()
            allergies = (await session.execute(select(AllergyRecord))).scalars().all()
            flares = (await session.execute(select(GoutFlare))).scalars().all()
            assert profiles == []
            assert allergies == []
            assert flares == []

    async with factory() as session:
        async with session.begin():
            await set_rls_context(session, tenant_a, user_a)
            profiles = (await session.execute(select(PatientProfile))).scalars().all()
            assert len(profiles) == 1
            assert profiles[0].tenant_id == tenant_a

    await engine.dispose()
