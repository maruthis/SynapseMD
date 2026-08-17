"""PostgreSQL row-level security policies and request-scoped session GUC helpers."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# Tenant + user scoped clinical/tracker/AI rows. FORCE so the table owner cannot bypass.
TENANT_USER_TABLES: tuple[str, ...] = (
    "patient_profiles",
    "allergies",
    "gout_flares",
    "ai_interactions",
    "review_queue",
    "consents",
    "break_glass_grants",
    "stored_objects",
)

# Tenant-scoped identity/audit. No FORCE so unauthenticated register/login still works.
TENANT_ONLY_TABLES: tuple[str, ...] = (
    "users",
    "audit_events",
    "tenant_model_policies",
    "routing_decisions_log",
    "dsr_requests",
    "legal_holds",
)

RLS_SQL = """
DO $$
DECLARE
  t text;
  tenant_user_tables text[] := ARRAY[
    'patient_profiles', 'allergies', 'gout_flares',
    'ai_interactions', 'review_queue', 'consents',
    'break_glass_grants', 'stored_objects'
  ];
  tenant_tables text[] := ARRAY['users', 'audit_events', 'tenant_model_policies', 'routing_decisions_log', 'dsr_requests', 'legal_holds'];
BEGIN
  FOREACH t IN ARRAY tenant_user_tables LOOP
    IF to_regclass('public.' || t) IS NULL THEN
      CONTINUE;
    END IF;
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', t);
    EXECUTE format('ALTER TABLE %I FORCE ROW LEVEL SECURITY', t);
    EXECUTE format('DROP POLICY IF EXISTS tenant_user_isolation ON %I', t);
    EXECUTE format(
      $policy$
      CREATE POLICY tenant_user_isolation ON %I FOR ALL
        USING (
          tenant_id = current_setting('app.tenant_id', true)::uuid
          AND user_id = current_setting('app.user_id', true)::uuid
        )
        WITH CHECK (
          tenant_id = current_setting('app.tenant_id', true)::uuid
          AND user_id = current_setting('app.user_id', true)::uuid
        )
      $policy$, t
    );
  END LOOP;

  FOREACH t IN ARRAY tenant_tables LOOP
    IF to_regclass('public.' || t) IS NULL THEN
      CONTINUE;
    END IF;
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', t);
    EXECUTE format('DROP POLICY IF EXISTS tenant_isolation ON %I', t);
    EXECUTE format(
      $policy$
      CREATE POLICY tenant_isolation ON %I FOR ALL
        USING (tenant_id = current_setting('app.tenant_id', true)::uuid)
        WITH CHECK (tenant_id = current_setting('app.tenant_id', true)::uuid)
      $policy$, t
    );
  END LOOP;
END
$$;
"""


def is_postgresql_url(database_url: str) -> bool:
    return "postgresql" in database_url.split("://", 1)[0]


async def apply_rls_policies(session: AsyncSession) -> None:
    bind = session.bind
    dialect_name = getattr(getattr(bind, "dialect", None), "name", "")
    if dialect_name != "postgresql":
        return
    await session.execute(text(RLS_SQL))


async def set_rls_context(
    session: AsyncSession,
    tenant_id: UUID | str,
    user_id: UUID | str,
) -> None:
    """SET LOCAL equivalent — must run inside an open transaction."""
    bind = session.bind
    dialect_name = getattr(getattr(bind, "dialect", None), "name", "")
    if dialect_name != "postgresql":
        return
    await session.execute(
        text("SELECT set_config('app.tenant_id', :tenant_id, true)"),
        {"tenant_id": str(tenant_id)},
    )
    await session.execute(
        text("SELECT set_config('app.user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )
