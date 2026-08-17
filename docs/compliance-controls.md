# Compliance Controls Mapping

Maps SynapseMD platform controls to regulatory frameworks. See [architecture.md](architecture.md), [release-gates.md](release-gates.md), and [platform/README.md](../platform/README.md) for details.

## HIPAA Technical Safeguards

| Requirement | Implementation |
|---|---|
| Access Control | JWT (15 min) + OIDC SSO + RBAC/PDP + MFA for privileged roles in prod + PostgreSQL RLS |
| Audit Controls | Durable `audit_events` (Postgres when `AUDIT_USE_MEMORY=false`); HMAC hash chain (`prev_hash`/`event_hash`); append-only trigger; auditor JSONL export |
| Integrity | Hash-chained audit stream (`audit/chain.py`); FHIR JSONB projection on clinical writes; object-store content hashes (`stored_objects.sha256`) |
| Transmission Security | TLS 1.3 (deployment), HTTPS-only API |
| Encryption at Rest | Per-tenant KMS keys (production); Vault KV for PHI tokens |
| PHI Minimum Necessary | Anonymization before LLM (Presidio in staging/prod); custom MRN/accession recognizers; audit hash-only; [phi-handling runbook](runbooks/phi-handling.md) |

## GDPR

| Right | Endpoint / Process |
|---|---|
| Access | `POST /privacy/dsr` (`request_type=access`) — FHIR + row counts; certificate has no PHI. Legacy: `GET /admin/export/{user_id}` |
| Erasure | `POST /privacy/dsr` (`request_type=erase`) — clinical rows, FHIR, object-store prefix, Vault tokens; user marked `erased`. Legal hold → 409. Legacy admin erase still FHIR-scoped. |
| Portability | FHIR R4 bundle via access DSR / export endpoint |
| Consent | [consent-flow.md](consent-flow.md) — `llm_processing` purpose, org RAG opt-in, LLM anonymization |

## SOC 2

- CC6: MFA (IdP `amr` claim in production), SSO via OIDC, RBAC + coded PDP
- CC8: GitOps, PR approvals, signed commits
- PI1: Medical guardrails on all LLM outputs — [clinical-safety-policy.md](clinical-safety-policy.md)
- Evidence process: [compliance/soc2-evidence.md](compliance/soc2-evidence.md)

## Initial Release

See [release-gates.md](release-gates.md) for the pre-release checklist covering PHI safety, tenant isolation, clinical safety, and operations.
