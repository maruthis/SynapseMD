import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ai_status(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.get(
        "/api/v1/ai/status",
        headers={"Authorization": patient_auth["Authorization"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["action"] == "status"
    assert body["result"]["enabled"] is True
    assert body["disclaimer"]


@pytest.mark.asyncio
async def test_ai_predict(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.post(
        "/api/v1/ai/predict",
        headers={"Authorization": patient_auth["Authorization"]},
        json={"risk_type": "hypertension"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["action"] == "predict"
    assert body["result"]["risk_type"] == "hypertension"


@pytest.mark.asyncio
async def test_ai_analyze(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.post(
        "/api/v1/ai/analyze",
        headers={"Authorization": patient_auth["Authorization"]},
        json={"time_range": "last_quarter"},
    )
    assert response.status_code == 200
    assert "predictions" in response.json()["result"]


@pytest.mark.asyncio
async def test_ai_chat(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.post(
        "/api/v1/ai/chat",
        headers={"Authorization": patient_auth["Authorization"]},
        json={"query": "How is my sleep?"},
    )
    assert response.status_code == 200
    assert response.json()["result"]["response"]


@pytest.mark.asyncio
async def test_ai_report(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.post(
        "/api/v1/ai/report",
        headers={"Authorization": patient_auth["Authorization"]},
        json={"report_type": "comprehensive", "time_range": "last_quarter"},
    )
    assert response.status_code == 200
    assert response.json()["result"]["report_type"] == "comprehensive"


@pytest.mark.asyncio
async def test_ai_endpoints_require_auth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/ai/status")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_commands_include_ai(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.get(
        "/api/v1/commands/",
        headers={"Authorization": patient_auth["Authorization"]},
    )
    assert response.status_code == 200
    assert "ai" in response.json()["commands"]


@pytest.mark.asyncio
async def test_execute_ai_command(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.post(
        "/api/v1/commands/execute",
        headers={"Authorization": patient_auth["Authorization"]},
        json={
            "command": "ai",
            "context_text": "",
            "payload": {"action": "status"},
        },
    )
    assert response.status_code == 200
    assert response.json()["command"] == "ai"
    assert response.json()["model_used"] == "synapsemd-ai"
