# SynapseMD Enterprise Platform

Multi-tenant, PHI-safe, FHIR-backed health API implementing all enterprise architecture phases.

## Quick Start

```bash
cd platform
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn synapsemd_platform.api.main:app --reload
```

API docs: http://localhost:8000/docs

## Phases Implemented

| Phase | Module | Status |
|-------|--------|--------|
| 0 | `core/`, `api/`, CI, Docker | ✅ |
| 1 | `auth/`, `models/tenant.py`, RBAC | ✅ |
| 2 | `anonymization/engine.py` | ✅ |
| 3 | `fhir/migration.py` | ✅ |
| 4 | `audit/events.py`, `observability/metrics.py` | ✅ |
| 5 | `llm/router.py`, `llm/providers.py` | ✅ |
| 6 | `rag/retrieval.py` | ✅ |
| 7 | `governance/guardrails.py`, review API | ✅ |
| 8 | Docker, Terraform stub, compliance docs | ✅ |

## Tests

```bash
pytest -v
```

## Docker

```bash
# Core stack
docker compose --profile core up --build

# Full stack (MCP + HAPI + Kafka + Vault + UI)
docker compose --profile full up --build
```

See [docker-compose.profiles.md](docker-compose.profiles.md) for profile details.

## MCP Server

```bash
export SYNAPSEMD_ACCESS_TOKEN=<jwt-from-login>
synapsemd-mcp
```

## Kubernetes

```bash
kubectl apply -k ../deploy/k8s/overlays/staging
```
