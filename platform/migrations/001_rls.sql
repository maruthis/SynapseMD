-- PostgreSQL row-level security policies (production)
-- Apply after tenants/users tables exist

ALTER TABLE IF EXISTS ai_interactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY IF NOT EXISTS tenant_isolation ON ai_interactions
  USING (
    tenant_id = current_setting('app.tenant_id', true)::uuid
    AND user_id = current_setting('app.user_id', true)::uuid
  );
