# Secret Rotation Runbook

## Secrets inventory

| Secret | Location | Rotation cadence |
|--------|----------|------------------|
| JWT signing key | K8s Secret / env `JWT_SECRET` | 90 days |
| LLM API keys | K8s Secret | On compromise or 180 days |
| Vault root/token | Vault policy | 90 days (use short-lived tokens in prod) |
| Database credentials | K8s Secret / managed RDS | 90 days |

## JWT rotation (zero-downtime)

1. Generate new secret: `openssl rand -hex 32`
2. Update K8s Secret `synapsemd-secrets` with `JWT_SECRET_NEW`
3. Deploy API with dual-verify window (if supported) or maintenance window
4. Invalidate outstanding tokens (users re-login)
5. Remove old secret

## LLM provider keys

1. Issue new key in provider console (Anthropic/OpenAI/Google health deployment)
2. Update K8s Secret
3. Rolling restart API deployment: `kubectl rollout restart deployment/synapsemd-api -n synapsemd`
4. Revoke old key after 24h monitoring

## Vault token rotation

```bash
vault token renew -increment=768h
# Or create new AppRole and update synapsemd deployment
```

## Post-rotation verification

- [ ] Auth login succeeds
- [ ] Command execute returns 200
- [ ] Audit events still signed correctly
- [ ] MCP tools respond with valid JWT
