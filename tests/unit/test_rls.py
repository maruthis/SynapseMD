"""RLS helper unit tests (SQLite no-ops) and SQL contract."""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from synapsemd_platform.core.database import Base, get_rls_session
from synapsemd_platform.core.rls import (
    RLS_SQL,
    TENANT_ONLY_TABLES,
    TENANT_USER_TABLES,
    apply_rls_policies,
    is_postgresql_url,
    set_rls_context,
)
from synapsemd_platform.models import clinical, governance, objects, tenant, trackers  # noqa: F401


def test_is_postgresql_url() -> None:
    assert is_postgresql_url("postgresql+asyncpg://u:p@localhost/db") is True
    assert is_postgresql_url("sqlite+aiosqlite:///:memory:") is False


def test_rls_sql_covers_slice_tables() -> None:
    sql = Path("platform/migrations/001_rls.sql").read_text(encoding="utf-8")
    assert "ENABLE ROW LEVEL SECURITY" in sql
    assert "FORCE ROW LEVEL SECURITY" in sql
    assert "tenant_user_isolation" in sql
    assert "tenant_isolation" in sql
    assert "app.tenant_id" in sql
    assert "app.user_id" in sql
    assert "CREATE POLICY IF NOT EXISTS" not in sql
    for table in TENANT_USER_TABLES:
        assert table in sql
        assert table in RLS_SQL
    for table in TENANT_ONLY_TABLES:
        assert table in sql


@pytest.mark.asyncio
async def test_rls_helpers_noop_on_sqlite() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        await apply_rls_policies(session)
        await set_rls_context(session, uuid4(), uuid4())
    await engine.dispose()


@pytest.mark.asyncio
async def test_apply_rls_policies_executes_on_postgresql() -> None:
    session = AsyncMock()
    bind = MagicMock()
    bind.dialect.name = "postgresql"
    session.bind = bind
    session.execute = AsyncMock()
    await apply_rls_policies(session)
    session.execute.assert_awaited_once()
    sql = str(session.execute.await_args.args[0])
    assert "ENABLE ROW LEVEL SECURITY" in sql


@pytest.mark.asyncio
async def test_set_rls_context_sets_configs_on_postgresql() -> None:
    session = AsyncMock()
    bind = MagicMock()
    bind.dialect.name = "postgresql"
    session.bind = bind
    session.execute = AsyncMock()
    tenant_id = uuid4()
    user_id = uuid4()
    await set_rls_context(session, tenant_id, user_id)
    assert session.execute.await_count == 2
    assert session.execute.await_args_list[0].args[1]["tenant_id"] == str(tenant_id)
    assert session.execute.await_args_list[1].args[1]["user_id"] == str(user_id)


@pytest.mark.asyncio
async def test_get_rls_session_sqlite() -> None:
    agen = get_rls_session(str(uuid4()), str(uuid4()))
    session = await agen.__anext__()
    assert session is not None
    await agen.aclose()
