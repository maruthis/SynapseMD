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
| Latency p95 | < 15s | `llm_latency_seconds` |
| PHI block rate | monitored, no fixed SLO | `phi_block_total` |
| Guardrail block rate | monitored | `guardrail_block_total` |

## MCP

| SLO | Target | Measurement |
|-----|--------|-------------|
| Tool success rate | 99% | MCP client error logs |
| Auth failure rate | < 1% | 403 on bridge `/tools/invoke` |

## Audit

| SLO | Target | Measurement |
|-----|--------|-------------|
| Event delivery | 99.9% | Kafka consumer lag |
| Signing integrity | 100% | All events have `signature` field |

## Review queue

| SLO | Target | Measurement |
|-----|--------|-------------|
| Time to first review | < 4 hours (business hours) | `review_queue` pending age |
| Backlog | < 20 pending items | `GET /review/queue` |

## Error budget

Monthly error budget = 0.5% downtime (~3.6 hours). Breach triggers release freeze until root cause addressed.
