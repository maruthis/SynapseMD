"""Postgres trigger: audit_events cannot be updated or deleted (C-6)."""

from sqlalchemy import text

# Split for asyncpg: one prepared statement cannot contain multiple commands.
AUDIT_APPEND_ONLY_STATEMENTS: tuple[str, ...] = (
    """
    CREATE OR REPLACE FUNCTION audit_events_deny_mutation() RETURNS trigger AS $$
    BEGIN
      RAISE EXCEPTION 'audit_events is append-only';
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    DO $$
    BEGIN
      IF to_regclass('public.audit_events') IS NULL THEN
        RETURN;
      END IF;
      DROP TRIGGER IF EXISTS audit_events_no_update ON audit_events;
      DROP TRIGGER IF EXISTS audit_events_no_delete ON audit_events;
      CREATE TRIGGER audit_events_no_update
        BEFORE UPDATE ON audit_events
        FOR EACH ROW EXECUTE FUNCTION audit_events_deny_mutation();
      CREATE TRIGGER audit_events_no_delete
        BEFORE DELETE ON audit_events
        FOR EACH ROW EXECUTE FUNCTION audit_events_deny_mutation();
    END
    $$;
    """,
)

AUDIT_APPEND_ONLY_SQL = "\n".join(AUDIT_APPEND_ONLY_STATEMENTS)


async def apply_audit_append_only(conn) -> None:
    for statement in AUDIT_APPEND_ONLY_STATEMENTS:
        await conn.execute(text(statement))
