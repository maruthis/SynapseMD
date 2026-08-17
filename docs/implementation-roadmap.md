# SynapseMD Platform — Implementation Roadmap

Phased delivery of the enterprise architecture.

**Enterprise upgrade (Postgres SoR, SSO, audit, model catalog):** design [enterprise-platform-architecture.md](enterprise-platform-architecture.md) · plan [enterprise-platform-implementation-plan.md](enterprise-platform-implementation-plan.md).

## Vertical Slice (Complete)

```
Auth → Tenant-scoped API → PHI anonymization → RAG → LLM router → Guardrails → Audit
```

## Phase Status

| Phase | Scope | Location | Status |
|-------|-------|----------|--------|
| 0 | Foundation, CI, Docker, ADRs | `platform/`, `.github/workflows/` | Done |
| 1 | Auth, RBAC, multi-tenancy | `auth/`, `api/routes/auth.py` | Done |
| 2 | PHI anonymization | `anonymization/engine.py` | Done |
| 3 | FHIR migration | `fhir/migration.py`, `scripts/migrate_json_to_fhir.py` | Done |
| 4 | Audit & observability | `audit/`, `observability/` | Done |
| 5 | LLM router | `llm/router.py`, `llm/providers.py` | Done |
| 6 | RAG | `rag/retrieval.py` | Done |
| 7 | AI governance & review | `governance/`, `api/routes/admin.py` | Done |
| 8 | Security & deployment | `deploy/k8s/`, `docker-compose.yml` | Done |
| 9 | MCP + UI integration | `mcp/`, `docs/ui-mcp-integration.md` | Done |
| 10 | Production hardening | Vault, Kafka, HAPI, BAA gates | In progress |
| A | Data plane (Postgres SoR) | Alembic, RLS, `HealthDataService`, FHIR JSONB, object store, command catalog | Done |
| B | Identity & access | OIDC, PDP, MFA, CORS, refresh sessions | Done (SCIM stub) |
| C | Observability & audit | OTel, PHI-free logs, hash-chained Postgres audit, JSONL export | Done |
| D | PHI & models | Presidio default, catalog + tenant policy, BAA registry, vLLM stub | Done |
| E | Privacy ops & HA | DSR, legal hold, NetworkPolicies, specialist workers, HA/PITR runbooks | Done |

## Initial Release Components

| Component | Local/Dev | Staging/Prod |
|-----------|-----------|--------------|
| UI | AnythingLLM (default) or Open WebUI | Same via MCP or OpenAPI bridge |
| LLM | Mock in tests/dev (`LLM_DEFAULT_PROVIDER=mock`) | Catalog + tenant policy; BAA registry; Presidio on |
| Runtime | Docker Compose (`core` = API + Postgres 16, `HEALTH_STORE=postgres`) | Kubernetes (Kustomize overlays) |
| Health SoR | Postgres (profile / allergy / gout + FHIR JSONB); JSON adapter for other domains / local CLI | Postgres for all tenant health data |
| FHIR | JSONB projection on write + local file store; optional HAPI | HAPI FHIR or managed FHIR |
| Objects | `OBJECT_STORE_BACKEND=memory` (tests/dev); DB stores URI + hash | S3-compatible bucket; no blob in Postgres |
| Audit | SQLite/memory in unit tests (`AUDIT_USE_MEMORY=true`) | Postgres hash-chained `audit_events`; optional Kafka copy; WORM stub |
| Secrets | Dev Vault container | Vault / cloud KMS |

## Release Gates

See [release-gates.md](release-gates.md) for the full pre-release checklist.

## Run Locally

```bash
# Core API + Postgres
cd platform && docker compose --profile core up

# Full suite against Docker Postgres (dedicated test DB, not the app database)
POSTGRES_TEST_URL=postgresql+asyncpg://synapsemd:synapsemd@localhost:5432/synapsemd_test pytest -v

# Full stack: API, MCP, HAPI, Kafka, Vault, AnythingLLM
cd platform && docker compose --profile full up
```

## Deploy to Kubernetes

```bash
kubectl apply -k deploy/k8s/overlays/staging
kubectl apply -k deploy/k8s/overlays/production
```
