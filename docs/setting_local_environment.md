# Setting Up Local Environment

Use the **`core` profile** from `platform/`. Every Compose service is profile-gated, so `docker compose up` with no profile starts nothing.

## Prerequisites

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and start it. Wait until the menu bar whale is idle (not “starting”).
2. Confirm the engine is up:

```bash
docker info >/dev/null && echo "Docker is running"
```

3. Free **port 8000** (API) and **port 5432** (Postgres). If something else already owns them, stop it or Compose will fail to bind.

4. You need `jq` for the smoke-test curls (`brew install jq`), or use the Swagger UI instead.

---

## 1. Start API + Postgres

From the repo root:

```bash
cd /Users/maruti/Documents/MaruGit/SynapseMD/platform

docker compose --profile core up --build
```

Leave this terminal open. First build takes a few minutes. You want:

- Postgres: `database system is ready to accept connections`
- API: Alembic `Running upgrade ... -> head`, then Uvicorn on port 8000

To run in the background instead:

```bash
docker compose --profile core up --build -d
docker compose --profile core logs -f api
```

`--build` is required after platform code or migration changes so the image includes the latest Alembic revisions (including consent columns).

---

## 2. Confirm it is healthy

In a **second** terminal:

```bash
cd /Users/maruti/Documents/MaruGit/SynapseMD/platform

docker compose --profile core ps
```

Both `api` and `postgres` should be `running`; Postgres should be `healthy`.

```bash
curl -s http://localhost:8000/health
```

Expected:

```json
{"status":"healthy","service":"synapsemd-platform"}
```

Open interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

| Service | Where |
|---------|--------|
| API + Swagger | http://localhost:8000/docs |
| Health | http://localhost:8000/health |
| Postgres | `localhost:5432` — user `synapsemd`, password `synapsemd`, database `synapsemd` |

Compose sets `HEALTH_STORE=postgres`, `APP_ENV=development` (password login on), and `LLM_DEFAULT_PROVIDER=mock`. The API entrypoint runs `alembic upgrade head` on every start.

---

## 3. Smoke test (optional but recommended)

Access tokens last **15 minutes**. Use `@example.com` emails — Pydantic `EmailStr` rejects `.test`.

```bash
BASE=http://localhost:8000

# 1. Tenant
TENANT=$(curl -s -X POST "$BASE/api/v1/auth/tenants" \
  -H "Content-Type: application/json" \
  -d '{"name":"Demo Clinic","plan":"professional"}')
echo "$TENANT"
TENANT_ID=$(echo "$TENANT" | jq -r .id)

# 2. Patient user
curl -s -X POST "$BASE/api/v1/auth/tenants/$TENANT_ID/users" \
  -H "Content-Type: application/json" \
  -d '{"email":"patient@example.com","password":"securepass1","role":"patient"}'

# 3. Login
LOGIN=$(curl -s -X POST "$BASE/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"patient@example.com\",\"password\":\"securepass1\",\"tenant_id\":\"$TENANT_ID\"}")
TOKEN=$(echo "$LOGIN" | jq -r .access_token)
echo "token length: ${#TOKEN}"

# 4. Persist a profile (Postgres SoR + FHIR JSONB)
curl -s -X POST "$BASE/api/v1/commands/execute" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command":"profile","payload":{"action":"upsert","basic_info":{"gender":"M","height":175,"weight":70}}}'
```

You can also Authorize in Swagger with `Bearer <token>` and try the same calls in the browser.

Refresh before the 15-minute expiry:

```bash
REFRESH=$(echo "$LOGIN" | jq -r .refresh_token)
curl -s -X POST "$BASE/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH\"}"
```

Longer copy-paste flows (profile/allergy/gout, AI predict, admin/audit) are in section 4.

---

## 4. End-to-end API tests

Run these in the same terminal after the stack is healthy. Tokens last **15 minutes** — re-run the login blocks if you get `401`.

Health writes go through `POST /api/v1/commands/execute` and land in Postgres (`patient_profiles`, `allergies`, `gout_flares`) with a FHIR JSONB projection. Command `response` is a JSON string; pipe it through `jq -r .response | jq` to read it.

### Shared setup (tenant + three roles)

```bash
BASE=http://localhost:8000
AUTH() { echo "Authorization: Bearer $1"; }

register_and_login() {
  local email="$1" password="$2" role="$3" varname="$4"
  local user login
  user=$(curl -s -X POST "$BASE/api/v1/auth/tenants/$TENANT_ID/users" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$email\",\"password\":\"$password\",\"role\":\"$role\"}")
  echo "$user"
  login=$(curl -s -X POST "$BASE/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$email\",\"password\":\"$password\",\"tenant_id\":\"$TENANT_ID\"}")
  eval "${varname}_ID=$(echo "$user" | jq -r .id)"
  eval "${varname}_TOKEN=$(echo "$login" | jq -r .access_token)"
}

TENANT=$(curl -s -X POST "$BASE/api/v1/auth/tenants" \
  -H "Content-Type: application/json" \
  -d '{"name":"Harbor Clinic","plan":"professional"}')
TENANT_ID=$(echo "$TENANT" | jq -r .id)
echo "tenant: $TENANT_ID"

register_and_login "patient@example.com" "securepass1" "patient" PATIENT
register_and_login "admin@example.com" "securepass1" "admin" ADMIN
register_and_login "auditor@example.com" "securepass1" "auditor" AUDITOR

echo "patient=$PATIENT_ID admin=$ADMIN_ID auditor=$AUDITOR_ID"
curl -s "$BASE/api/v1/auth/me" -H "$(AUTH "$PATIENT_TOKEN")" | jq
```

Expect `GET /api/v1/auth/me` to show `"roles": ["patient"]` and scopes `read:own` / `write:own`. Admin has `admin`; auditor has `audit`.

---

### Use case 1 — Profile, allergy, gout (Postgres SoR)

**What you are proving:** a patient can persist structured health data; list/get round-trips the same rows; data survives an API restart because it is in Postgres, not a JSON vault.

```bash
# Upsert profile (columns + FHIR Patient JSONB)
curl -s -X POST "$BASE/api/v1/commands/execute" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "profile",
    "payload": {
      "action": "upsert",
      "basic_info": {
        "gender": "M",
        "height": 175,
        "weight": 82,
        "birth_date": "1978-04-12"
      }
    }
  }' | jq -r .response | jq

# Read it back
curl -s -X POST "$BASE/api/v1/commands/execute" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{"command":"profile","payload":{"action":"get"}}' \
  | jq -r .response | jq

# Add allergy
curl -s -X POST "$BASE/api/v1/commands/execute" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "allergy",
    "payload": {
      "action": "add",
      "allergen": "penicillin",
      "type": "medication",
      "severity": "severe",
      "notes": "Anaphylaxis in 2019"
    }
  }' | jq -r .response | jq

curl -s -X POST "$BASE/api/v1/commands/execute" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{"command":"allergy","payload":{"action":"list"}}' \
  | jq -r .response | jq

# Add gout flare
curl -s -X POST "$BASE/api/v1/commands/execute" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "gout",
    "payload": {
      "action": "add",
      "joint": "first MTP",
      "side": "left",
      "severity": "moderate",
      "uric_acid_mg_dl": 8.4,
      "triggers": ["beer", "red meat"],
      "notes": "Overnight onset"
    }
  }' | jq -r .response | jq

curl -s -X POST "$BASE/api/v1/commands/execute" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{"command":"gout","payload":{"action":"list"}}' \
  | jq -r .response | jq
```

**Pass if:** profile get returns the same gender/height/weight; allergy list `count` is at least 1 with `penicillin`; gout list includes `first MTP`.

Optional persistence check:

```bash
cd /Users/maruti/Documents/MaruGit/SynapseMD/platform
docker compose --profile core restart api
# wait a few seconds, then login again if the token expired
curl -s -X POST "$BASE/api/v1/commands/execute" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{"command":"allergy","payload":{"action":"list"}}' \
  | jq -r .response | jq .count
```

Inspect FHIR JSONB in Postgres:

```bash
docker compose --profile core exec postgres \
  psql -U synapsemd -d synapsemd -c \
  "SELECT gender, height_cm, weight_kg, fhir->>'resourceType' FROM patient_profiles;"
```

---

### Use case 2 — AI predict (and related Module 21 calls)

**What you are proving:** AI endpoints read the patient record just written, run mock/local scoring (Compose sets `LLM_DEFAULT_PROVIDER=mock`), and stay tenant-scoped.

Do use case 1 first so the profile exists. Hypertension scoring uses age (from `birth_date`) and BMI (from height/weight).

```bash
# Feature status
curl -s "$BASE/api/v1/ai/status" \
  -H "$(AUTH "$PATIENT_TOKEN")" | jq

# Hypertension risk from the stored profile
curl -s -X POST "$BASE/api/v1/ai/predict" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{"risk_type":"hypertension"}' | jq

# Same predict via the command orchestrator
curl -s -X POST "$BASE/api/v1/commands/execute" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{"command":"ai","payload":{"action":"predict","target":"hypertension"}}' \
  | jq -r .response | jq

curl -s -X POST "$BASE/api/v1/ai/analyze" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{"time_range":"last_quarter"}' | jq

curl -s -X POST "$BASE/api/v1/ai/chat" \
  -H "$(AUTH "$PATIENT_TOKEN")" \
  -H "Content-Type: application/json" \
  -d '{"query":"What does my penicillin allergy imply for antibiotics?"}' | jq
```

**Pass if:** `/ai/status` is 200; `/ai/predict` returns an `action` of `predict` and a `result` object (often `risk_type` / `risk_level` / `probability`). Chat/analyze return mock text — that is expected locally.

Other `risk_type` values: `diabetes`, `cardiovascular`, `nutritional_deficiency`, `sleep_disorder`, `all`.

---

### Use case 3 — Admin catalog, audit trail, and role isolation

**What you are proving:** `admin` can list the command catalog; `auditor` can read audit events generated by the earlier commands; a patient cannot.

```bash
# Patient must be denied
curl -s -o /tmp/patient-admin.json -w "patient /admin/commands HTTP %{http_code}\n" \
  "$BASE/admin/commands" -H "$(AUTH "$PATIENT_TOKEN")"
cat /tmp/patient-admin.json; echo

# Admin: seeded command catalog (profile, allergy, gout, ai, …)
curl -s "$BASE/admin/commands" -H "$(AUTH "$ADMIN_TOKEN")" | jq

# Auditor: events from profile/allergy/gout/ai (health.command.executed, etc.)
curl -s "$BASE/admin/audit" -H "$(AUTH "$AUDITOR_TOKEN")" | jq '.events | length'
curl -s "$BASE/admin/audit?command=allergy" -H "$(AUTH "$AUDITOR_TOKEN")" | jq
curl -s "$BASE/admin/audit/export" -H "$(AUTH "$AUDITOR_TOKEN")" | head

# Admin bypasses scope checks, so this also works:
curl -s "$BASE/admin/audit" -H "$(AUTH "$ADMIN_TOKEN")" | jq '.events | length'

# Auditor does not have the admin scope
curl -s -o /dev/null -w "auditor /admin/commands HTTP %{http_code}\n" \
  "$BASE/admin/commands" -H "$(AUTH "$AUDITOR_TOKEN")"
```

**Pass if:** patient `/admin/commands` is **403**; admin `/admin/commands` is **200** with a `commands` array; auditor `/admin/audit` is **200** and includes events after use case 1; auditor `/admin/commands` is **403**.

Optional DSR (privacy officer — `POST /privacy/dsr`, not under `/api/v1`):

```bash
PRIVACY=$(curl -s -X POST "$BASE/api/v1/auth/tenants/$TENANT_ID/users" \
  -H "Content-Type: application/json" \
  -d '{"email":"privacy@example.com","password":"securepass1","role":"privacy_officer"}')
PRIVACY_LOGIN=$(curl -s -X POST "$BASE/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"privacy@example.com\",\"password\":\"securepass1\",\"tenant_id\":\"$TENANT_ID\"}")
PRIVACY_TOKEN=$(echo "$PRIVACY_LOGIN" | jq -r .access_token)

curl -s -X POST "$BASE/privacy/dsr" \
  -H "$(AUTH "$PRIVACY_TOKEN")" \
  -H "Content-Type: application/json" \
  -d "{\"subject_user_id\":\"$PATIENT_ID\",\"request_type\":\"access\"}" | jq
```

---

## 5. Other profiles (only if you need them)

| Profile | What starts | When to use |
|---------|-------------|-------------|
| `core` | API + Postgres | Everyday local work |
| `mcp` | core + MCP SSE on **8081** | MCP client work |
| `full` | Everything (FHIR, Kafka-ish bus, Vault, UIs) | Full-stack demo |

```bash
docker compose --profile mcp up --build
# or
docker compose --profile full up --build
```

`full` also needs ports **3000**, **8080**, **8081**, **8100**, **8200**, **9092**.

---

## 6. Stop and reset

Stop (keep data):

```bash
cd /Users/maruti/Documents/MaruGit/SynapseMD/platform
docker compose --profile core down
```

Wipe Postgres (destroys local tenants/health rows):

```bash
docker compose --profile core down -v
```

---

## If something fails

**`Cannot connect to the Docker daemon`**  
Docker Desktop is not running yet. Start it and wait until it is fully up.

**`Bind for 0.0.0.0:5432 failed` or `:8000`**  
Something else is using that port (often a local Postgres). Stop it, or change the left-hand port in `platform/docker-compose.yml` (for example `"5433:5432"`).

**`docker compose up` starts no containers**  
You omitted `--profile core`. All services are profile-gated.

**Login 500 mentioning `consents.source`**  
An old volume is missing a later Alembic column. Rebuild so the entrypoint can migrate:

```bash
docker compose --profile core up --build -d
```

If that still fails:

```bash
docker compose --profile core down -v
docker compose --profile core up --build
```

**`GET /admin/commands` is 404**  
The running image is stale. Rebuild with `--build` as above.

**Register 422 on email**  
Use `you@example.com`, not `you@test.com`.

**401 after ~15 minutes**  
Call `POST /api/v1/auth/refresh` with the refresh token, or log in again.