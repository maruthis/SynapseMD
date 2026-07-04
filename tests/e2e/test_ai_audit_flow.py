"""End-to-end: tenant → AI analyze → audit trail verification."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_e2e_ai_analyze_audit_flow(client: AsyncClient) -> None:
    tenant = await client.post(
        "/api/v1/auth/tenants",
        json={"name": "AI Audit Clinic", "plan": "enterprise"},
    )
    assert tenant.status_code == 201
    tenant_id = tenant.json()["id"]

    patient_reg = await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "ai-patient@test.com", "password": "securepass1", "role": "patient"},
    )
    assert patient_reg.status_code == 201

    await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "ai-auditor@test.com", "password": "securepass1", "role": "auditor"},
    )

    patient_login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "ai-patient@test.com",
            "password": "securepass1",
            "tenant_id": tenant_id,
        },
    )
    patient_token = patient_login.json()["access_token"]
    patient_headers = {"Authorization": f"Bearer {patient_token}"}

    analyze = await client.post(
        "/api/v1/ai/analyze",
        headers=patient_headers,
        json={"time_range": "last_quarter"},
    )
    assert analyze.status_code == 200
    body = analyze.json()
    assert body["action"] == "analyze"
    assert "predictions" in body["result"]
    assert body["disclaimer"]

    auditor_login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "ai-auditor@test.com",
            "password": "securepass1",
            "tenant_id": tenant_id,
        },
    )
    auditor_headers = {"Authorization": f"Bearer {auditor_login.json()['access_token']}"}

    audit = await client.get("/admin/audit", headers=auditor_headers)
    assert audit.status_code == 200
    events = audit.json()["events"]
    ai_events = [e for e in events if e["event_type"].startswith("ai.")]
    assert any(e["event_type"] == "ai.analyze.completed" for e in ai_events)

    for event in ai_events:
        assert event["tenant_id"] == tenant_id
        assert "prompt_hash" in event.get("ai", {})
        assert "response_hash" in event.get("ai", {})
        assert "prompt" not in event.get("ai", {})


@pytest.mark.asyncio
async def test_e2e_ai_predict_and_command_audit(client: AsyncClient, patient_auth: dict) -> None:
    headers = {"Authorization": patient_auth["Authorization"]}

    predict = await client.post(
        "/api/v1/ai/predict",
        headers=headers,
        json={"risk_type": "hypertension"},
    )
    assert predict.status_code == 200

    command = await client.post(
        "/api/v1/commands/execute",
        headers=headers,
        json={"command": "ai", "payload": {"action": "status"}},
    )
    assert command.status_code == 200
    assert command.json()["command"] == "ai"

    audit = await client.get("/admin/audit", headers=headers)
    assert audit.status_code == 403
