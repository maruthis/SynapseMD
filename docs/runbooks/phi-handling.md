# PHI Handling Runbook

## Overview

SynapseMD processes PHI through a layered defense: anonymization before LLM calls, hash-only audit storage, optional Vault token persistence, and Presidio in non-dev environments.

## Configuration

| Variable | Dev default | Staging/Prod |
|----------|-------------|--------------|
| `PRESIDIO_ENABLED` | `false` | `true` |
| `PHI_BLOCK_ON_FAILURE` | `true` | `true` |
| `VAULT_ENABLED` | `false` | `true` |
| `VAULT_URL` | — | `http://vault:8200` |

## Anonymization flow

1. User context enters `AnonymizationEngine.anonymize_for_llm()`
2. Presidio (if enabled) or regex patterns tokenize emails, phones, SSNs, dates, names
3. Token map stored in `TokenVault` (memory) or `VaultTokenVault` (production)
4. Post-anonymization validation runs; if PHI remains and `PHI_BLOCK_ON_FAILURE=true`, the LLM call is blocked

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

Token paths: `secret/data/synapsemd/tokens/{user_id}` (KV v2)

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
