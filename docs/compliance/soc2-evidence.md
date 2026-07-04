# SOC 2 Evidence Collection

## Control mapping

| SOC 2 criteria | SynapseMD evidence |
|----------------|-------------------|
| CC6.1 Logical access | JWT + RBAC tests, `tests/unit/test_auth_*.py` |
| CC6.2 Credential management | [secret-rotation.md](../runbooks/secret-rotation.md) |
| CC7.2 System monitoring | `/metrics`, [slo.md](../slo.md), Prometheus rules |
| CC8.1 Change management | GitHub PR reviews, CI (`platform-ci.yml`) |
| PI1.1 Processing integrity | Guardrails tests, eval harness |

## Artifact collection process

1. **Per release**: Export CI green screenshot, coverage report, release-gates checklist
2. **Monthly**: Audit log sample (redacted), access review of admin roles
3. **Quarterly**: BAA status review, backup/restore drill log, pen test summary (if applicable)

## Storage

Store evidence in secure document repository (not in git). Reference paths in `mydocs/compliance/evidence-index.md` (create per org).

## Auditor engagement

| Milestone | Target date | Status |
|-----------|-------------|--------|
| Readiness assessment | (schedule) | Planned |
| Type I audit | (schedule) | Planned |
| Type II audit | (schedule) | Planned |

Update dates when external audit is scheduled.
