-- PostgreSQL row-level security policies (production)
-- Apply after ai_interactions exists (SQLAlchemy create_all / migrations).
-- Safe for docker-entrypoint-initdb.d: no-ops if the table is not present yet.
--
-- Note: CREATE POLICY does not support IF NOT EXISTS in PostgreSQL.

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
