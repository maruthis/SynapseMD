# Compliance Controls Mapping

Maps SynapseMD platform controls to regulatory frameworks. See [enterprise-architecture.md](enterprise-architecture.md) for full details.

## HIPAA Technical Safeguards

| Requirement | Implementation |
|---|---|
| Access Control | JWT + RBAC + tenant isolation |
| Audit Controls | `audit/events.py`, immutable event signatures |
| Integrity | FHIR resource versioning, content hashes |
| Transmission Security | TLS 1.3 (deployment), HTTPS-only API |
| Encryption at Rest | Per-tenant KMS keys (production); Vault KV for PHI tokens |
| PHI Minimum Necessary | Anonymization before LLM; audit hash-only; [phi-handling runbook](runbooks/phi-handling.md) |

## GDPR

| Right | Endpoint / Process |
|---|---|
| Access | `/admin/export/{user_id}` — FHIR bundle export (admin, tenant-scoped) |
| Erasure | `POST /admin/users/{user_id}/erase` — FHIR delete + user marked `erased` |
| Portability | FHIR R4 bundle via export endpoint |
| Consent | [consent-flow.md](consent-flow.md) — org RAG opt-in, LLM anonymization |

## SOC 2

- CC6: MFA, SSO via OIDC, RBAC
- CC8: GitOps, PR approvals, signed commits
- PI1: Medical guardrails on all LLM outputs — [clinical-safety-policy.md](clinical-safety-policy.md)
- Evidence process: [compliance/soc2-evidence.md](compliance/soc2-evidence.md)

## Initial Release

See [release-gates.md](release-gates.md) for the pre-release checklist covering PHI safety, tenant isolation, clinical safety, and operations.
