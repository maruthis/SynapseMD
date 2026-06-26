# Initial Release Gates

Checklist before promoting SynapseMD to staging or production.

## PHI Safety

- [ ] Presidio enabled (`PRESIDIO_ENABLED=true`) in non-dev environments
- [ ] PHI block on anonymization failure enforced (`PHI_BLOCK_ON_FAILURE=true`)
- [ ] No PHI in application logs, audit payloads, or LLM prompt storage (hashes only)
- [ ] Vault/KMS used for tokenized PHI when `VAULT_ENABLED=true`
- [ ] Automated PHI leakage tests pass (`tests/release/test_phi_safety.py`)

## Tenant Isolation

- [ ] JWT claims enforce `tenant_id` on every API and MCP tool call
- [ ] Cross-tenant negative tests pass at API, FHIR, RAG, and audit layers
- [ ] Org intelligence RAG sources are tenant-scoped and opt-in
- [ ] PostgreSQL RLS policies applied (`platform/migrations/001_rls.sql`)

## Clinical Safety

- [ ] Medical guardrails block diagnostic claims and unsafe medication advice
- [ ] High-risk commands (`consult`, `mental-health`) require human review in production
- [ ] Emergency disclaimers present on low-confidence responses
- [ ] Human review queue operational for clinician workflow

## LLM Provider Readiness

- [ ] Signed BAA on file for each production provider (`*_BAA_SIGNED=true`)
- [ ] Provider routing configured per environment (`LLM_DEFAULT_PROVIDER`)
- [ ] Fallback model path tested for provider outages
- [ ] Model evaluation harness passes golden prompt regression suite

## Observability and SLOs

- [ ] `/health` and `/metrics` endpoints monitored
- [ ] SLOs defined: API p95 latency, LLM latency, error rate, PHI block rate
- [ ] Audit events emitted to Kafka in staging/prod (`AUDIT_USE_KAFKA=true`)
- [ ] Alerting on guardrail blocks and review queue backlog

## Operations

- [ ] Database backup and restore drill completed
- [ ] Secret rotation runbook documented
- [ ] Incident response playbook documented
- [ ] Rollback procedure tested for API and MCP deployments
- [ ] Docker Compose profiles validated for local/dev
- [ ] Kubernetes overlays validated for staging and production

## Compliance

- [ ] HIPAA technical safeguards mapped in [compliance-controls.md](compliance-controls.md)
- [ ] SOC 2 control evidence collection process defined
- [ ] Consent flow for org RAG and LLM calls documented
- [ ] Data export and erasure endpoints planned or implemented
- [ ] External HIPAA/SOC 2 audit engagement scheduled

## UI Integration

- [ ] MCP tool contract documented in [ui-mcp-integration.md](ui-mcp-integration.md)
- [ ] AnythingLLM MCP attachment validated locally
- [ ] Open WebUI OpenAPI bridge validated as fallback
- [ ] Chat UI does not store PHI outside SynapseMD platform boundaries
