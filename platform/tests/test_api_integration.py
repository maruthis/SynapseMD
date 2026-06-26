import pytest
from httpx import ASGITransport, AsyncClient

from synapsemd_platform.api.main import create_app
from synapsemd_platform.core.database import init_db


@pytest.fixture
async def client():
    app = create_app()
    await init_db()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_auth_and_command_flow(client: AsyncClient):
    tenant_resp = await client.post(
        "/api/v1/auth/tenants",
        json={"name": "Test Hospital", "plan": "professional"},
    )
    assert tenant_resp.status_code == 201
    tenant_id = tenant_resp.json()["id"]

    user_resp = await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "patient@example.com", "password": "securepass1", "role": "patient"},
    )
    assert user_resp.status_code == 201

    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "patient@example.com", "password": "securepass1", "tenant_id": tenant_id},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    cmd_resp = await client.post(
        "/api/v1/commands/execute",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "command": "goal",
            "context_text": "Patient John Smith wants to lose 5kg by June. Email: john@example.com",
            "payload": {"data_sources": ["data/profile.json"]},
        },
    )
    assert cmd_resp.status_code == 200
    body = cmd_resp.json()
    assert body["command"] == "goal"
    assert "response" in body
    assert "john@example.com" not in body["response"] or "TOKEN" in body["response"]
