# ADR-001: Modular Monolith First

**Status:** Accepted

Start with a modular FastAPI monolith (`synapsemd_platform`) that can be split into microservices later. Each phase maps to a Python package.

# ADR-002: SQLite for Dev, PostgreSQL for Production

**Status:** Accepted

Use SQLite for local development and tests; PostgreSQL with RLS for production multi-tenancy.

# ADR-003: Mock LLM Provider by Default

**Status:** Accepted

Default to `MockLLMProvider` so development and CI do not require external API keys or BAAs.

# ADR-004: Regex Anonymization Fallback

**Status:** Accepted

Presidio is optional (`PRESIDIO_ENABLED=true`). Regex-based PHI detection is used when Presidio is unavailable.

# ADR-005: Structured Reasoning Summaries

**Status:** Accepted

Store structured reasoning summaries, not raw chain-of-thought, for audit and explainability.
