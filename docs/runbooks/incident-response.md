# Incident Response Playbook

## Severity levels

| Level | Example | Response time |
|-------|---------|---------------|
| SEV-1 | Confirmed PHI exposed externally | Immediate |
| SEV-2 | Guardrail bypass, cross-tenant data access | < 1 hour |
| SEV-3 | Provider outage, elevated error rate | < 4 hours |
| SEV-4 | Non-critical degradation | Next business day |

## SEV-1: PHI exposure

1. **Contain**: Set `LLM_DEFAULT_PROVIDER=mock`, scale MCP to 0 if UI is leaking context
2. **Assess**: Pull audit logs (`/admin/audit`), check provider logs (must be hash-only)
3. **Notify**: Engage security lead; follow HIPAA breach assessment if applicable
4. **Remediate**: Patch, rotate secrets, redeploy
5. **Document**: Post-incident report in `mydocs/ops-log.md`

## SEV-2: Cross-tenant access

1. Identify affected endpoints and tenants from audit `event_type`
2. Run `tests/release/test_tenant_isolation.py` against deployed build
3. Hotfix JWT middleware or DAL filtering
4. Notify affected tenants per policy

## SEV-3: LLM provider outage

1. Confirm fallback path: `LLMOrchestrator` uses `fallback_model`
2. Switch `LLM_DEFAULT_PROVIDER=mock` temporarily if all providers fail
3. Monitor `llm_latency_seconds` and error rate

## Communication template

```
SynapseMD incident [SEV-N]: [one-line summary]
Status: investigating | mitigated | resolved
Impact: [tenants/users affected]
Next update: [time UTC]
```

## Contacts

- Platform on-call: (define in org)
- Security: (define in org)
- Clinical safety reviewer: (define in org)
