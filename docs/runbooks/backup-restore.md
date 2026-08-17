# Backup and Restore Runbook

## Scope

PostgreSQL (tenant/users/audit/review/DSR tables), FHIR local store or HAPI FHIR, RAG vector store files, Vault secrets (PHI token maps).

Production topology is **managed HA Postgres** (primary + synchronous replica) with **encrypted PITR**. Compose `full` is not a production topology.

## HA Postgres (staging / production)

Use a managed offering (Aurora, Cloud SQL, or equivalent) with:

- One primary and at least one synchronous replica in the same region
- Storage encryption at rest (CMK / customer-managed key)
- Automated backups retained ≥ 7 days (HIPAA: align with tenant retention, default 6 years for audit)
- Point-in-time recovery (PITR) enabled; WAL / transaction logs encrypted in transit and at rest
- Network path only from `synapsemd-api` (see `deploy/k8s/base/network-policies.yaml`)

Connection string stays `DATABASE_URL` (asyncpg). Do not run a single-node Postgres in production overlays.

## PostgreSQL backup

```bash
# Logical dump (staging drill)
pg_dump "$DATABASE_URL" -Fc -f synapsemd-$(date +%Y%m%d).dump
```

Managed PITR does not replace a periodic logical dump used for tenant-scoped restore tests.

CI covers a logical identity dump/restore (`synapsemd_platform.jobs.backup_restore.dump_identity` / `restore_identity`) in `tests/unit/test_backup_restore.py`. That is not a substitute for a staging PITR clone.

Existing Compose volumes created before Consent.`source` / `expires_at` need Alembic `0007_consent_columns` (API entrypoint runs `alembic upgrade head`). That is schema migration, not a PITR drill.

## PostgreSQL restore drill (PITR)

1. Record the restore target timestamp (UTC) and ticket id in `mydocs/ops-log.md`.
2. Restore to a **new** instance / database (`synapsemd_restore_test`), never onto the live primary.
3. For managed PITR:

```bash
# Example: restore to a clone at a point in time (provider CLI varies)
# gcloud sql backups restore ... --backup-id=... --backup-instance=...
# aws rds restore-db-instance-to-point-in-time ...
```

4. Verify:

```bash
psql "$RESTORE_URL" -c "SELECT count(*) FROM tenants;"
psql "$RESTORE_URL" -c "SELECT count(*) FROM audit_events;"
psql "$RESTORE_URL" -c "SELECT count(*) FROM dsr_requests;"
```

5. Confirm RLS is still enabled (`platform/migrations/001_rls.sql`).
6. Record RTO/RPO observed in `mydocs/ops-log.md`.

**Drill log**: date, operator, RTO, RPO, issues.

## FHIR data

- **Local store**: backup `FHIR_LOCAL_STORE` directory (`data/fhir/`)
- **HAPI FHIR**: use HAPI export or Postgres backup of HAPI schema

## RAG vector store

Backup `RAG_VECTOR_STORE_PATH` when `RAG_VECTOR_STORE=file`.

## Vault / tenant DEK

Use Vault snapshot/raft backup per HashiCorp docs. PHI token maps live under `secret/synapsemd/tokens/{tenant}/{user}`. After a DB restore, rotate the tenant DEK if the restore is for a compromised environment (see [secret-rotation.md](secret-rotation.md)).

## Recovery order

1. PostgreSQL (PITR clone, then promote if this is a real DR)
2. Vault secrets
3. FHIR bundles
4. RAG index
5. Redeploy API + MCP from last known-good image (`kubectl rollout undo` if the incident was a bad deploy)

## Verification

- [ ] `/health` returns 200
- [ ] Login succeeds for test tenant
- [ ] FHIR profile summary returns data for migrated user
- [ ] DSR access for a test user returns expected resource counts
- [ ] Audit hash-chain verify still passes on the restored stream
