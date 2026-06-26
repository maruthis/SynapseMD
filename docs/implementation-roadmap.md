# SynapseMD Platform — Implementation Roadmap

Phased delivery of the enterprise architecture. **Status: Phase 0–8 scaffold implemented** in `platform/`.

## Vertical Slice (Complete)

```
Auth → Tenant-scoped API → PHI anonymization → RAG → LLM router → Guardrails → Audit
```

## Phase Status

| Phase | Scope | Location | Status |
|-------|-------|----------|--------|
| 0 | Foundation, CI, Docker, ADRs | `platform/`, `.github/workflows/` | ✅ |
| 1 | Auth, RBAC, multi-tenancy | `auth/`, `api/routes/auth.py` | ✅ |
| 2 | PHI anonymization | `anonymization/engine.py` | ✅ |
| 3 | FHIR migration | `fhir/migration.py`, `scripts/migrate_json_to_fhir.py` | ✅ |
| 4 | Audit & observability | `audit/`, `observability/` | ✅ |
| 5 | LLM router | `llm/router.py`, `llm/providers.py` | ✅ |
| 6 | RAG | `rag/retrieval.py` | ✅ |
| 7 | AI governance & review | `governance/`, `api/routes/admin.py` | ✅ |
| 8 | Security & deployment | `infra/terraform/`, `docker-compose.yml` | ✅ scaffold |

## Next Steps (Production Hardening)

- Wire real Anthropic/OpenAI providers with BAAs
- Enable Presidio in production (`PRESIDIO_ENABLED=true`)
- Deploy PostgreSQL + Kafka + Vault via Terraform
- HAPI FHIR server for cloud clinical storage
- SOC 2 / HIPAA audit engagement

## Run Locally

See [local-development.md](local-development.md).
