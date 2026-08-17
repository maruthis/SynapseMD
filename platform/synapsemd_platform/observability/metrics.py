from prometheus_client import Counter, Gauge, Histogram

REQUEST_COUNT = Counter(
    "synapsemd_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

LLM_LATENCY = Histogram(
    "synapsemd_llm_latency_seconds",
    "LLM call latency",
    ["model", "command"],
)

PHI_BLOCK_COUNT = Counter(
    "synapsemd_phi_blocks_total",
    "PHI anonymization blocks",
)

ANONYMIZE_FAILURE_COUNT = Counter(
    "synapsemd_anonymize_failures_total",
    "Anonymization failures that blocked an LLM call",
)

GUARDRAIL_BLOCK_COUNT = Counter(
    "synapsemd_guardrail_blocks_total",
    "Guardrail blocks",
    ["command"],
)

AUTH_FAILURE_COUNT = Counter(
    "synapsemd_auth_failures_total",
    "Authentication failures",
    ["reason"],
)

RLS_DENIAL_COUNT = Counter(
    "synapsemd_rls_denials_total",
    "Cross-tenant / RLS denials",
)

AUDIT_WRITE_FAILURE_COUNT = Counter(
    "synapsemd_audit_write_failures_total",
    "Failed durable audit writes",
)

REVIEW_QUEUE_AGE = Gauge(
    "synapsemd_review_queue_oldest_seconds",
    "Age in seconds of the oldest pending review item",
)
