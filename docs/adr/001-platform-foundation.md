# ADR-001: Modular Monolith First

**Status:** Accepted

Start with a modular FastAPI monolith (`synapsemd_platform`) that can be split into microservices later. Each phase maps to a Python package.

# ADR-002: SQLite for Tests, PostgreSQL for Platform

**Status:** Accepted (amended 2026-08-17)

Use SQLite + `HEALTH_STORE=json` for fast unit tests. Use PostgreSQL 16 with Alembic and RLS for local platform runs (Compose `core`) and staging/prod. JSON files remain the local IDE vault, not the production system of record.

CI and local Docker tests that exercise RLS/Alembic must use `POSTGRES_TEST_URL` against a dedicated `synapsemd_test` database. The Compose bootstrap user is a superuser and bypasses RLS; those tests use a non-superuser login role.

# ADR-003: Mock LLM Provider by Default

**Status:** Accepted

Default to `MockLLMProvider` so development and CI do not require external API keys or BAAs.

# ADR-004: Regex Anonymization Fallback

**Status:** Accepted

Presidio is optional (`PRESIDIO_ENABLED=true`). Regex-based PHI detection is used when Presidio is unavailable.

# ADR-005: Structured Reasoning Summaries

**Status:** Accepted

Store structured reasoning summaries, not raw chain-of-thought, for audit and explainability.
