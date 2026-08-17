# Service Level Objectives

## API

| SLO | Target | Measurement |
|-----|--------|-------------|
| Availability | 99.5% monthly | `/health` success rate |
| Latency p95 | < 500ms (non-LLM routes) | `http_request_duration_seconds` |
| Error rate | < 0.5% | 5xx / total requests |

## LLM / Command orchestrator

| SLO | Target | Measurement |
|-----|--------|-------------|
| Latency p95 | < 15s | `synapsemd_llm_latency_seconds` |
| PHI block rate | monitored, no fixed SLO | `synapsemd_phi_blocks_total` |
| Guardrail block rate | monitored | `synapsemd_guardrail_blocks_total` |
| Anonymize failures | page on spike | `synapsemd_anonymize_failures_total` |

## MCP

| SLO | Target | Measurement |
|-----|--------|-------------|
| Tool success rate | 99% | MCP client error logs |
| Auth failure rate | < 1% | 403 on bridge `/tools/invoke` |

## Audit

| SLO | Target | Measurement |
|-----|--------|-------------|
| Durable write | 100% when `AUDIT_USE_MEMORY=false` | `synapsemd_audit_write_failures_total` (page on any increase) |
| Chain integrity | 100% | `verify_chain` on tenant-day stream; HMAC `event_hash` |
| Signing integrity | 100% | All events have `signature` field |
| Optional SIEM copy | best-effort | Kafka consumer lag (not the SoR) |

## Review queue

| SLO | Target | Measurement |
|-----|--------|-------------|
| Time to first review | < 4 hours (business hours) | `synapsemd_review_queue_oldest_seconds` |
| Backlog | < 20 pending items | `GET /review/queue` |

## Error budget

Monthly error budget = 0.5% downtime (~3.6 hours). Breach triggers release freeze until root cause addressed.
