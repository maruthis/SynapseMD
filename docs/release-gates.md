# Initial Release Gates

Checklist before promoting SynapseMD to staging or production.

Evidence links: runbooks in [docs/runbooks/](runbooks/), tests in `tests/release/` and `tests/eval/`.

## PHI Safety

- [x] Presidio enabled (`PRESIDIO_ENABLED=true`) in non-dev environments — `deploy/k8s/base/configmap.yaml`, staging/production overlays
- [x] PHI block on anonymization failure enforced (`PHI_BLOCK_ON_FAILURE=true`) — default in `core/config.py`, K8s overlays
- [x] No PHI in application logs, audit payloads, or LLM prompt storage (hashes only) — `anonymization/scrubber.py`, `audit/events.py`
- [x] Vault/KMS used for tokenized PHI when `VAULT_ENABLED=true` — `anonymization/vault_store.py` wired in `AnonymizationEngine`
- [x] Automated PHI leakage tests pass (`tests/release/test_phi_safety.py`)

## Tenant Isolation

- [x] JWT claims enforce `tenant_id` on every API and MCP tool call — `auth/middleware.py`, MCP `resolve_auth_context`
- [x] Cross-tenant negative tests pass at API, FHIR, RAG, and audit layers — `tests/release/test_tenant_isolation.py`, `test_ai_tenant_isolation.py`
- [x] Org intelligence RAG sources are tenant-scoped and opt-in — `rag/retrieval.py`, `ORG_INTELLIGENCE_ENABLED=false` in prod overlay
- [x] PostgreSQL RLS policies applied (`platform/migrations/001_rls.sql`) — migration file + policy validation test

## Clinical Safety

- [x] Medical guardrails block diagnostic claims and unsafe medication advice — `governance/guardrails.py`, unit + eval tests
- [x] High-risk commands (`consult`, `mental-health`) require human review in production — `HUMAN_REVIEW_COMMANDS`, orchestrator
- [x] Emergency disclaimers present on low-confidence responses — guardrails + AIService disclaimers
- [x] Human review queue operational for clinician workflow — `GET /review/queue`, integration test

## LLM Provider Readiness

- [x] Signed BAA on file for each production provider (`*_BAA_SIGNED=true`) — production K8s overlay + `BaaGateError` in code
- [x] Provider routing configured per environment (`LLM_DEFAULT_PROVIDER`) — staging=mock, production=anthropic
- [x] Fallback model path tested for provider outages — `tests/unit/test_production_modules.py`
- [x] Model evaluation harness passes golden prompt regression suite — `tests/eval/test_model_regression.py`

## Observability and SLOs

- [x] `/health` and `/metrics` endpoints monitored — `api/routes/admin.py`, integration tests
- [x] SLOs defined: API p95 latency, LLM latency, error rate, PHI block rate — [docs/slo.md](slo.md)
- [x] Audit events emitted to Kafka in staging/prod (`AUDIT_USE_KAFKA=true`) — K8s ConfigMap/overlays
- [x] Alerting on guardrail blocks and review queue backlog — [deploy/k8s/base/prometheus-rules.yaml](deploy/k8s/base/prometheus-rules.yaml), [runbooks/alerting.md](runbooks/alerting.md)

## Operations

- [ ] Database backup and restore drill completed — runbook: [runbooks/backup-restore.md](runbooks/backup-restore.md); log in [mydocs/ops-log.md](../mydocs/ops-log.md)
- [x] Secret rotation runbook documented — [runbooks/secret-rotation.md](runbooks/secret-rotation.md)
- [x] Incident response playbook documented — [runbooks/incident-response.md](runbooks/incident-response.md)
- [ ] Rollback procedure tested for API and MCP deployments — procedure in [mydocs/ops-log.md](../mydocs/ops-log.md); drill pending
- [x] Docker Compose profiles validated for local/dev — [platform/docker-compose.profiles.md](../platform/docker-compose.profiles.md)
- [x] Kubernetes overlays validated for staging and production — [deploy/k8s/README.md](../deploy/k8s/README.md), `kubectl apply -k` manifests

## Compliance

- [x] HIPAA technical safeguards mapped in [compliance-controls.md](compliance-controls.md)
- [x] SOC 2 control evidence collection process defined — [compliance/soc2-evidence.md](compliance/soc2-evidence.md)
- [x] Consent flow for org RAG and LLM calls documented — [consent-flow.md](consent-flow.md)
- [x] Data export and erasure endpoints planned or implemented — `GET /admin/export/{user_id}`, `POST /admin/users/{user_id}/erase`
- [ ] External HIPAA/SOC 2 audit engagement scheduled — track dates in [compliance/soc2-evidence.md](compliance/soc2-evidence.md)

## UI Integration

- [x] MCP tool contract documented in [ui-mcp-integration.md](ui-mcp-integration.md)
- [ ] AnythingLLM MCP attachment validated locally — checklist: [mydocs/qa/anythingllm-validation.md](../mydocs/qa/anythingllm-validation.md)
- [ ] Open WebUI OpenAPI bridge validated as fallback — checklist: [mydocs/qa/openwebui-validation.md](../mydocs/qa/openwebui-validation.md)
- [x] Chat UI does not store PHI outside SynapseMD platform boundaries — [ui-mcp-integration.md](ui-mcp-integration.md) § PHI boundary

---

**Progress**: 29 / 33 gates verified (4 require manual drill or external scheduling)
