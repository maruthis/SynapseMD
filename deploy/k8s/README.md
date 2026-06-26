# Kubernetes deployment for SynapseMD

## Structure

```
deploy/k8s/
  base/           # Shared manifests
  overlays/
    staging/      # Staging environment overrides
    production/   # Production environment overrides
```

## Deploy

```bash
# Staging
kubectl apply -k deploy/k8s/overlays/staging

# Production
kubectl apply -k deploy/k8s/overlays/production
```

## Components

| Resource | Purpose |
|----------|---------|
| `synapsemd-api` | FastAPI platform (2 replicas staging, 3 prod) |
| `synapsemd-mcp` | MCP server for chatbot UIs |
| ConfigMap | Non-secret environment configuration |
| Secret | JWT, DB, Vault, LLM API keys |

External managed services (recommended for production):
- PostgreSQL (Aurora / Cloud SQL)
- Kafka (MSK / Event Hubs)
- Vault (HashiCorp Cloud / cloud KMS)
- HAPI FHIR or managed FHIR
