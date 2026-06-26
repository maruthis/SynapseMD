from prometheus_client import Counter, Histogram

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

GUARDRAIL_BLOCK_COUNT = Counter(
    "synapsemd_guardrail_blocks_total",
    "Guardrail blocks",
    ["command"],
)
