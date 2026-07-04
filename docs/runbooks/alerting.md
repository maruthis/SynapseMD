# Alerting Runbook

## Metrics endpoints

- API health: `GET /health`
- Prometheus scrape: `GET /metrics` (text format in JSON wrapper for dev; use raw endpoint in prod)

## Recommended alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| `SynapseMDHighErrorRate` | 5xx rate > 1% for 5m | Check API logs, DB connectivity |
| `SynapseMDPHIBlockSpike` | `phi_block_total` increase > 10/min | Review anonymization config; possible attack |
| `SynapseMDGuardrailBlockSpike` | `guardrail_block_total` increase | Review recent command patterns |
| `SynapseMDReviewQueueBacklog` | pending review items > 50 | Page clinician on-call |
| `SynapseMDLLMLatencyHigh` | p95 `llm_latency_seconds` > 30s | Check provider status; enable fallback |
| `SynapseMDAuditKafkaLag` | consumer lag > 1000 | Check Redpanda/Kafka |

## Prometheus rules

See [deploy/k8s/base/prometheus-rules.yaml](../../deploy/k8s/base/prometheus-rules.yaml).

## Triage steps

1. Confirm alert via Grafana/dashboard
2. Check recent deploys: `kubectl rollout history deployment/synapsemd-api -n synapsemd`
3. Run smoke tests: `pytest tests/integration/test_api.py -k health`
4. Escalate per [incident-response.md](incident-response.md)

## Staging validation

Before promoting to production, verify alerts fire in staging by injecting test guardrail blocks (dev-only endpoint or test command with blocked pattern).
