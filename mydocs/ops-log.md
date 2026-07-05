# Operations Log

Record drills and production incidents here.

| Date | Activity | Operator | Result | Notes |
|------|----------|----------|--------|-------|
| | DB backup/restore drill | | | |
| | API rollback drill | | | |
| | MCP rollback drill | | | |
| | Secret rotation | | | |

## Rollback procedure (API + MCP)

```bash
kubectl rollout undo deployment/synapsemd-api -n synapsemd
kubectl rollout undo deployment/synapsemd-mcp -n synapsemd
kubectl rollout status deployment/synapsemd-api -n synapsemd
```

Record each drill above with timestamp and outcome.
