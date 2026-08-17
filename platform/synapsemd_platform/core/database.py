from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from synapsemd_platform.audit.append_only import apply_audit_append_only
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.rls import RLS_SQL, set_rls_context


class Base(DeclarativeBase):
    pass


settings = get_settings()
engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def _import_models() -> None:
    from synapsemd_platform.models import (  # noqa: F401
        audit,
        clinical,
        governance,
        iam,
        models_catalog,
        objects,
        review,
        tenant,
        trackers,
        commands,
    )


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_rls_session(tenant_id: str, user_id: str) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        async with session.begin():
            await set_rls_context(session, tenant_id, user_id)
            yield session


async def init_db() -> None:
    _import_models()
    dialect = engine.dialect.name
    async with engine.begin() as conn:
        if dialect == "sqlite" or settings.auto_create_schema:
            await conn.run_sync(Base.metadata.create_all)
        if dialect == "postgresql":
            await conn.execute(text(RLS_SQL))
            await apply_audit_append_only(conn)
