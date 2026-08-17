# Local Development — SynapseMD Platform

## Prerequisites

- Python 3.11+
- Docker Desktop (recommended) for PostgreSQL 16 — required for RLS and staging-like runs

## Recommended: Docker Desktop (`core` profile)

This is the verified local path for the enterprise data plane. Compose sets `HEALTH_STORE=postgres` and the API entrypoint runs `alembic upgrade head` on start.

```bash
cd platform
docker compose --profile core up --build
```

| Service | URL |
|---------|-----|
| API docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |
| Postgres | localhost:5432 (`synapsemd` / `synapsemd`) |

Use `@example.com` emails when registering users (Pydantic rejects `.test` domains).

Restart the API container after writing profile / allergy / gout rows — those rows survive because they live in Postgres, not the JSON vault. Writes also store a FHIR JSONB projection. PDFs and reports use `OBJECT_STORE_BACKEND` (default `memory`); Postgres keeps URI + SHA-256 only.

Existing Compose volumes created before consent `source` / `expires_at` need Alembic `0007_consent_columns` (runs automatically on API start). If login returns 500 about a missing `consents.source` column, rebuild the API image so `alembic upgrade head` can run, or recreate the volume.

## Python venv (SQLite + JSON for unit tests)

```bash
cd platform
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

`HEALTH_STORE=json` (default) is fine for fast unit tests. Schema for SQLite tests uses `create_all`. Staging/prod schema is Alembic-only.

To point a local uvicorn at Compose Postgres instead:

```bash
# from platform/ — Postgres already running via compose
# .env
DATABASE_URL=postgresql+asyncpg://synapsemd:synapsemd@localhost:5432/synapsemd
HEALTH_STORE=postgres
alembic upgrade head
uvicorn synapsemd_platform.api.main:app --reload --port 8000
```

## Example Flow

```bash
# Create tenant
curl -X POST http://localhost:8000/api/v1/auth/tenants \
  -H "Content-Type: application/json" \
  -d '{"name":"Demo Clinic","plan":"professional"}'

# Register user (use tenant id from above; @example.com required)
curl -X POST http://localhost:8000/api/v1/auth/tenants/{tenant_id}/users \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass1","role":"patient"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass1","tenant_id":"{tenant_id}"}'

# Execute /goal command (LLM orchestrator)
curl -X POST http://localhost:8000/api/v1/commands/execute \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"command":"goal","context_text":"Lose 5kg in 3 months"}'

# Persist profile / allergy / gout (HealthDataService — no LLM)
curl -X POST http://localhost:8000/api/v1/commands/execute \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"command":"profile","payload":{"action":"upsert","basic_info":{"gender":"M","height":175,"weight":70}}}'

curl -X POST http://localhost:8000/api/v1/commands/execute \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"command":"allergy","payload":{"action":"add","allergen":"penicillin","severity":"severe"}}'

curl -X POST http://localhost:8000/api/v1/commands/execute \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"command":"gout","payload":{"action":"add","joint":"left ankle","severity":"moderate"}}'
```

Payload shapes: [data-structures.md](data-structures.md) § Platform SoR mapping.

Password login works in `APP_ENV=development`. Staging/prod use OIDC (`POST /api/v1/auth/oidc/login`). Access tokens expire in 15 minutes; use `/api/v1/auth/refresh`. Optional Keycloak: `docker compose --profile infra up keycloak`.

## Run Tests

```bash
# From repo root (SQLite unit tests; Postgres tests skip without POSTGRES_TEST_URL)
pytest -v

# Full suite including RLS, Alembic, and append-only trigger (Docker Desktop Postgres)
# Use a dedicated database — Alembic downgrade and RLS tests drop schema.
docker exec platform-postgres-1 psql -U synapsemd -d postgres -c "CREATE DATABASE synapsemd_test;"
POSTGRES_TEST_URL=postgresql+asyncpg://synapsemd:synapsemd@localhost:5432/synapsemd_test pytest -v
```

Compose `POSTGRES_USER=synapsemd` is a superuser and **bypasses RLS**. Release RLS tests connect as a non-superuser role (`synapsemd_app`). Do not point `POSTGRES_TEST_URL` at the live `synapsemd` app database.

Coverage gate: ≥95% on `synapsemd_platform` (currently ~98%, 426 tests).
