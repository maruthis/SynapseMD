import json
from pathlib import Path

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_e2e_health_goal_audit_flow(client: AsyncClient, tmp_path: Path) -> None:
  """End-to-end: tenant → user → login → goal command → audit trail → FHIR migrate."""

  tenant = await client.post(
      "/api/v1/auth/tenants",
      json={"name": "E2E Clinic", "plan": "enterprise"},
  )
  tenant_id = tenant.json()["id"]

  await client.post(
      f"/api/v1/auth/tenants/{tenant_id}/users",
      json={"email": "e2e@test.com", "password": "securepass1", "role": "admin"},
  )
  login = await client.post(
      "/api/v1/auth/login",
      json={"email": "e2e@test.com", "password": "securepass1", "tenant_id": tenant_id},
  )
  token = login.json()["access_token"]
  headers = {"Authorization": f"Bearer {token}"}

  goal = await client.post(
      "/api/v1/commands/execute",
      headers=headers,
      json={
          "command": "goal",
          "context_text": "Patient wants to lose 5kg by December. Email: e2e@test.com",
          "payload": {"data_sources": ["data/profile.json"]},
      },
  )
  assert goal.status_code == 200
  body = goal.json()
  assert body["human_review_required"] is False or body["human_review_required"] is True
  assert "interaction_id" in body

  audit = await client.get("/admin/audit", headers=headers)
  assert audit.status_code == 200
  events = audit.json()["events"]
  assert any(e["event_type"] == "ai.command.executed" for e in events)

  (tmp_path / "profile.json").write_text(
      json.dumps({"basic_info": {"gender": "female", "birth_date": "1990-01-01"}}),
      encoding="utf-8",
  )
  (tmp_path / "allergies.json").write_text(json.dumps({"allergies": []}), encoding="utf-8")

  migrate = await client.post(
      "/admin/migrate",
      headers=headers,
      json={"source_directory": str(tmp_path)},
  )
  assert migrate.status_code == 200
  assert "Patient" in migrate.json()["resource_types"]

  health = await client.get("/health")
  assert health.json()["status"] == "healthy"
