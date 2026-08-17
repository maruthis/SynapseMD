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
2. Set `JWT_SECRET_PREVIOUS` to the **current** `JWT_SECRET` (dual-verify window).
3. Set `JWT_SECRET` to the new value. Rolling restart API + MCP.
4. Tokens signed with the previous secret still verify (`decode_access_token` tries current, then previous).
5. After the 15-minute access TTL (+ refresh overlap), clear `JWT_SECRET_PREVIOUS`.
6. Invalidate refresh sessions if the rotation is incident-driven: revoke `sessions` rows for the tenant.

## Tenant DEK / Vault token-map rotation (staging drill)

1. Create a new Vault key version / KMS key (`KMS_MASTER_KEY_ID`).
2. Re-wrap token maps under `secret/synapsemd/tokens/{tenant}/{user}` (new `_kms_key_id` in the payload).
3. Confirm a command execute still deanonymizes for a test user.
4. Retire the old key version after the overlap window.
5. Log the drill in `mydocs/ops-log.md` (date, operator, tenants touched, issues).

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
