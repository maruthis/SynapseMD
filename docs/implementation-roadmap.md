# SynapseMD Platform — Implementation Roadmap

Phased delivery of the enterprise architecture.

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

## Initial Release Components

| Component | Local/Dev | Staging/Prod |
|-----------|-----------|--------------|
| UI | AnythingLLM (default) or Open WebUI | Same via MCP or OpenAPI bridge |
| LLM | Mock / Claude Code CLI (dev workflow) | Health-specific providers with BAA |
| Runtime | Docker Compose profiles | Kubernetes (Kustomize overlays) |
| FHIR | Local file store + optional HAPI | HAPI FHIR or managed FHIR |
| Audit | In-memory | Kafka + immutable store |
| Secrets | Dev Vault container | Vault / cloud KMS |

## Release Gates

See [release-gates.md](release-gates.md) for the full pre-release checklist.

## Run Locally

```bash
# Core API + Postgres
cd platform && docker compose --profile core up

# Full stack: API, MCP, HAPI, Kafka, Vault, AnythingLLM
cd platform && docker compose --profile full up
```

## Deploy to Kubernetes

```bash
kubectl apply -k deploy/k8s/overlays/staging
kubectl apply -k deploy/k8s/overlays/production
```
