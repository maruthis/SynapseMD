-- PostgreSQL row-level security policies (production)
-- Canonical copy of synapsemd_platform.core.rls.RLS_SQL.
-- Applied by Alembic 0001_data_plane (not docker-entrypoint-initdb.d).

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
