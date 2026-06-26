# Compliance Controls Mapping

Maps SynapseMD platform controls to regulatory frameworks. See [enterprise-architecture.md](enterprise-architecture.md) for full details.

## HIPAA Technical Safeguards

| Requirement | Implementation |
|---|---|
| Access Control | JWT + RBAC + tenant isolation |
| Audit Controls | `audit/events.py`, immutable event signatures |
| Integrity | FHIR resource versioning, content hashes |
| Transmission Security | TLS 1.3 (deployment), HTTPS-only API |
| Encryption at Rest | Per-tenant KMS keys (production) |
| PHI Minimum Necessary | Anonymization before LLM; tokenized logs |

## GDPR

| Right | Endpoint / Process |
|---|---|
| Access | `/admin/export/{user_id}` (planned) |
| Erasure | Soft-delete + KMS key revocation (planned) |
| Portability | FHIR R4 `.ndjson` export via migration layer |
| Consent | Consent check before LLM calls (planned) |

## SOC 2

- CC6: MFA, SSO via OIDC, RBAC
- CC8: GitOps, PR approvals, signed commits
- PI1: Medical guardrails on all LLM outputs
