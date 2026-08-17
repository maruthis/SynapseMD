# Alerting Runbook

## Metrics endpoints

- API health: `GET /health`
- Prometheus scrape: `GET /metrics` (text format in JSON wrapper for dev; use raw endpoint in prod)

## Recommended alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| `SynapseMDHighErrorRate` | 5xx rate > 1% for 5m | Check API logs, DB connectivity |
| `SynapseMDPHIBlockSpike` | `synapsemd_phi_blocks_total` increase > 10/5m | Review anonymization config; possible attack |
| `SynapseMDGuardrailBlockSpike` | `synapsemd_guardrail_blocks_total` increase | Review recent command patterns |
| `SynapseMDAuditWriteFailure` | any `synapsemd_audit_write_failures_total` increase | **Page** — durable audit write failed; events may be memory-only |
| `SynapseMDAuthFailureSpike` | `synapsemd_auth_failures_total` increase > 50/5m | Credential stuffing or IdP outage |
| `SynapseMDAnonymizeFailureSpike` | `synapsemd_anonymize_failures_total` increase > 5/5m | LLM path blocked; check Presidio/regex engine |
| `SynapseMDReviewQueueBacklog` | pending review items > 50 | Page clinician on-call |
| `SynapseMDLLMLatencyHigh` | p95 `synapsemd_llm_latency_seconds` > 30s | Check provider status; enable fallback |
| `SynapseMDAuditKafkaLag` | consumer lag > 1000 | Check Redpanda/Kafka (optional copy; Postgres is SoR) |

## Prometheus rules

See [deploy/k8s/base/prometheus-rules.yaml](../../deploy/k8s/base/prometheus-rules.yaml).

## Triage steps

1. Confirm alert via Grafana/dashboard
2. Check recent deploys: `kubectl rollout history deployment/synapsemd-api -n synapsemd`
3. Run smoke tests: `pytest tests/integration/test_api.py -k health`
4. Escalate per [incident-response.md](incident-response.md)

## Staging validation

Before promoting to production, verify alerts fire in staging by injecting test guardrail blocks (dev-only endpoint or test command with blocked pattern).
