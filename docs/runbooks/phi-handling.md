# PHI Handling Runbook

## Overview

SynapseMD processes PHI through a layered defense: anonymization before LLM calls, hash-only audit storage, optional Vault token persistence, Presidio in non-dev environments, and object-store blobs that never land in Postgres (URI + SHA-256 only).

## Configuration

| Variable | Dev default | Staging/Prod |
|----------|-------------|--------------|
| `PRESIDIO_ENABLED` | `false` (explicit in tests) | unset → **on** (`presidio_is_enabled()`) |
| `PHI_BLOCK_ON_FAILURE` | `true` | `true` |
| `VAULT_ENABLED` | `false` | `true` (memory token vault is forbidden) |
| `VAULT_URL` | — | Vault address |

## Anonymization flow

1. User context enters `AnonymizationEngine.anonymize_for_llm()`
2. Presidio (staging/prod default) or regex patterns tokenize emails, phones, SSNs, dates, names, MRN, accession, Indian phones
3. Token map stored in `VaultTokenVault` (required in staging/prod) or in-memory `TokenVault` (dev/tests only)
4. Post-anonymization validation runs; if PHI remains and `PHI_BLOCK_ON_FAILURE=true`, the LLM call is blocked — no provider HTTP
5. `ModelPolicyEngine` may still refuse the call (BAA, residency, budget, allowlist) before the provider is invoked

## Audit policy

- Audit `ai` section stores **hashes only** (`prompt_hash`, `response_hash`)
- Raw strings in `resource` are scrubbed via `scrub_audit_payload()` before emit
- Verify: `pytest tests/release/test_phi_safety.py`

## Vault operations

```bash
# Dev Vault (Docker Compose profile infra)
export VAULT_ADDR=http://localhost:8200
vault kv put secret/synapsemd/tokens/<user_id> TOKEN_EMAIL_abc=redacted@example.com
```

Token paths: `secret/data/synapsemd/tokens/{tenant_id}/{user_id}` (KV v2)

## Incident: suspected PHI leakage

1. Disable LLM routing (`LLM_DEFAULT_PROVIDER=mock`) via ConfigMap
2. Pull audit events for affected tenant: `GET /admin/audit`
3. Confirm no raw PHI in event payloads (only hashes)
4. Rotate JWT secret and LLM API keys
5. File incident per [incident-response.md](incident-response.md)

## Verification checklist

- [ ] `PRESIDIO_ENABLED=true` in staging/production overlays
- [ ] `tests/release/test_phi_safety.py` passes in CI
- [ ] Audit sample review shows hash-only AI fields
- [ ] Application logs contain no email/phone patterns (grep audit)
