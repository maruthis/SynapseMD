# BAA Tracking

Business Associate Agreements must be on file before enabling production LLM providers.

## Provider gates

| Provider | Env var | Required in staging | Required in production |
|----------|---------|---------------------|------------------------|
| Anthropic | `ANTHROPIC_BAA_SIGNED` | `false` (mock preferred) | `true` |
| OpenAI | `OPENAI_BAA_SIGNED` | `false` | `true` |
| Google | `GOOGLE_BAA_SIGNED` | `false` | `true` |

Enforced in code: `create_provider()` raises `BaaGateError` when `APP_ENV` is `staging` or `production` and BAA flag is false.

## Kustomize overlays

- **Staging**: `deploy/k8s/overlays/staging/` — `LLM_DEFAULT_PROVIDER=mock`, BAA flags `false`
- **Production**: `deploy/k8s/overlays/production/` — `LLM_DEFAULT_PROVIDER=anthropic`, all BAA flags `true`

## Record keeping

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
