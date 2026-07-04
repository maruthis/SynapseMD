# Backup and Restore Runbook

## Scope

PostgreSQL (tenant/users/audit/review tables), FHIR local store or HAPI FHIR, RAG vector store files, Vault secrets.

## PostgreSQL backup

```bash
# Staging/production (replace connection string)
pg_dump "$DATABASE_URL" -Fc -f synapsemd-$(date +%Y%m%d).dump
```

## PostgreSQL restore drill

```bash
createdb synapsemd_restore_test
pg_restore -d synapsemd_restore_test synapsemd-YYYYMMDD.dump
psql synapsemd_restore_test -c "SELECT count(*) FROM tenants;"
```

**Drill log**: Record date, operator, RTO observed, and issues in `mydocs/ops-log.md`.

## FHIR data

- **Local store**: backup `FHIR_LOCAL_STORE` directory (`data/fhir/`)
- **HAPI FHIR**: use HAPI export or Postgres backup of HAPI schema

## RAG vector store

Backup `RAG_VECTOR_STORE_PATH` when `RAG_VECTOR_STORE=file`.

## Vault

Use Vault snapshot/raft backup per HashiCorp docs. PHI token maps live under `secret/synapsemd/tokens/`.

## Recovery order

1. PostgreSQL
2. Vault secrets
3. FHIR bundles
4. RAG index
5. Redeploy API + MCP from last known-good image

## Verification

- [ ] `/health` returns 200
- [ ] Login succeeds for test tenant
- [ ] FHIR profile summary returns data for migrated user
