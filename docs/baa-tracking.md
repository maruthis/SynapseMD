# BAA Tracking

Business Associate Agreements must be on file before enabling production LLM providers.

## Provider gates

| Provider | Env var | Required in staging | Required in production |
|----------|---------|---------------------|------------------------|
| Anthropic | `ANTHROPIC_BAA_SIGNED` | `false` (mock preferred) | `true` |
| OpenAI | `OPENAI_BAA_SIGNED` | `false` | `true` |
| Google | `GOOGLE_BAA_SIGNED` | `false` | `true` |

Enforced in code: `ModelPolicyEngine` checks `baa_records` (falling back to `*_BAA_SIGNED` env flags). `create_provider()` still raises `BaaGateError` when `APP_ENV` is `staging` or `production` and the env flag is false.

Tenant admins can set `baa_required: true` on `PUT /admin/models/policy` to forbid non-BAA catalog entries (including `mock`).

## Kustomize overlays

- **Staging**: `deploy/k8s/overlays/staging/` — `LLM_DEFAULT_PROVIDER=mock`, BAA flags `false`
- **Production**: `deploy/k8s/overlays/production/` — `LLM_DEFAULT_PROVIDER=anthropic`, all BAA flags `true`

## Record keeping

Rows in `baa_records` (`provider`, `signed`, `contract_ref`, `signed_at`) are the enforcement registry. The table below is the human log.

| Provider | BAA signed date | Contract ref | Owner |
|----------|-----------------|--------------|-------|
| Anthropic | (fill) | | |
| OpenAI | (fill) | | |
| Google | (fill) | | |

## Verification

```bash
pytest tests/unit/test_llm_providers.py -k baa
kubectl get configmap synapsemd-config -n synapsemd -o yaml | grep BAA
```

## Renewal

Review BAA status quarterly. Update K8s overlays if provider changes.
