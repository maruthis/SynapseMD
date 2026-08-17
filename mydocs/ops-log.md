# Operations Log

Record drills and production incidents here.

| Date | Activity | Operator | Result | Notes |
|------|----------|----------|--------|-------|
| 2026-08-17 | Phase E runbooks: PITR restore, JWT dual-verify, API/MCP rollback | platform | Ready | Execute live staging drill before prod cutover |
| 2026-08-17 | CI identity dump/restore drill (`jobs/backup_restore.py`) | platform | Pass | `tests/unit/test_backup_restore.py` — tenant+user round-trip into a fresh SQLite DB. Not a live staging PITR. |
| | DB backup/restore drill (staging PITR clone) | | | |
| | API rollback drill | | | |
| | MCP rollback drill | | | |
| | Secret rotation (JWT + tenant DEK) | | | |

## Rollback procedure (API + MCP)

```bash
kubectl rollout undo deployment/synapsemd-api -n synapsemd
kubectl rollout undo deployment/synapsemd-mcp -n synapsemd
kubectl rollout status deployment/synapsemd-api -n synapsemd
kubectl rollout status deployment/synapsemd-mcp -n synapsemd
curl -fsS https://api.example.com/health
```

Record each drill above with timestamp, image before/after, and outcome.

## Staging restore drill checklist

Copy this block into a dated section when the drill is executed:

```text
Date:
Operator:
Backup / PITR timestamp (UTC):
Restore target (clone name):
RTO observed:
RPO observed:
/health 200:
Login OK:
Audit chain verify:
Issues:
```
