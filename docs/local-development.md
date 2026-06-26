# Local Development — SynapseMD Platform

## Prerequisites

- Python 3.11+
- Optional: Docker for PostgreSQL

## Setup

```bash
cd platform
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Run API

```bash
uvicorn synapsemd_platform.api.main:app --reload --port 8000
```

## Example Flow

```bash
# Create tenant
curl -X POST http://localhost:8000/api/v1/auth/tenants \
  -H "Content-Type: application/json" \
  -d '{"name":"Demo Clinic","plan":"professional"}'

# Register user (use tenant id from above)
curl -X POST http://localhost:8000/api/v1/auth/tenants/{tenant_id}/users \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass1","role":"patient"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass1","tenant_id":"{tenant_id}"}'

# Execute /goal command
curl -X POST http://localhost:8000/api/v1/commands/execute \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"command":"goal","context_text":"Lose 5kg in 3 months"}'
```

## Run Tests

```bash
pytest -v
```
