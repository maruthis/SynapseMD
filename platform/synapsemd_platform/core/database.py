from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from synapsemd_platform.core.config import get_settings

# Embedded so API containers apply RLS even when migrations/ is not in the image.
# Keep in sync with platform/migrations/001_rls.sql.
_RLS_SQL = """
DO $$
BEGIN
  IF to_regclass('public.ai_interactions') IS NULL THEN
    RAISE NOTICE 'ai_interactions does not exist yet; skipping RLS setup';
    RETURN;
  END IF;

  EXECUTE 'ALTER TABLE ai_interactions ENABLE ROW LEVEL SECURITY';

  EXECUTE 'DROP POLICY IF EXISTS tenant_isolation ON ai_interactions';

  EXECUTE $policy$
    CREATE POLICY tenant_isolation ON ai_interactions
      FOR ALL
      USING (
        tenant_id = current_setting('app.tenant_id', true)::uuid
        AND user_id = current_setting('app.user_id', true)::uuid
      )
      WITH CHECK (
        tenant_id = current_setting('app.tenant_id', true)::uuid
        AND user_id = current_setting('app.user_id', true)::uuid
      )
  $policy$;
END
$$;
"""


class Base(DeclarativeBase):
    pass


settings = get_settings()
engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


def _load_rls_sql() -> str:
    migrations_sql = Path(__file__).resolve().parents[2] / "migrations" / "001_rls.sql"
    if migrations_sql.is_file():
        return migrations_sql.read_text(encoding="utf-8")
    return _RLS_SQL


async def init_db() -> None:
    from synapsemd_platform.models import audit, review, tenant  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(_load_rls_sql()))
