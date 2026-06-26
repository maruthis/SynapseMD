import os
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

# Use isolated sqlite DB for every test session
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("JWT_SECRET", "test-secret-key")
os.environ.setdefault("AUDIT_USE_MEMORY", "true")
os.environ.setdefault("FHIR_LOCAL_STORE", "/tmp/synapsemd-test-fhir")
os.environ.setdefault("PRESIDIO_ENABLED", "false")

from synapsemd_platform.api.main import create_app
from synapsemd_platform.audit.events import audit_producer
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.database import init_db


@pytest.fixture(autouse=True)
def _clear_audit_events() -> None:
    audit_producer._memory_events.clear()
    get_settings.cache_clear()


@pytest.fixture
async def app():
    application = create_app()
    await init_db()
    return application


@pytest.fixture
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def tenant_id(client: AsyncClient) -> str:
    response = await client.post(
        "/api/v1/auth/tenants",
        json={"name": "Test Clinic", "plan": "professional"},
    )
    assert response.status_code == 201
    return response.json()["id"]


@pytest.fixture
async def patient_auth(client: AsyncClient, tenant_id: str) -> dict:
    await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "patient@test.com", "password": "securepass1", "role": "patient"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "patient@test.com", "password": "securepass1", "tenant_id": tenant_id},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "tenant_id": tenant_id}


@pytest.fixture
async def admin_auth(client: AsyncClient, tenant_id: str) -> dict:
    await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "admin@test.com", "password": "securepass1", "role": "admin"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "securepass1", "tenant_id": tenant_id},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "tenant_id": tenant_id}


@pytest.fixture
async def auditor_auth(client: AsyncClient, tenant_id: str) -> dict:
    await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "auditor@test.com", "password": "securepass1", "role": "auditor"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "auditor@test.com", "password": "securepass1", "tenant_id": tenant_id},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "tenant_id": tenant_id}


@pytest.fixture
async def clinician_auth(client: AsyncClient, tenant_id: str) -> dict:
    await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "clinician@test.com", "password": "securepass1", "role": "clinician"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "clinician@test.com", "password": "securepass1", "tenant_id": tenant_id},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "tenant_id": tenant_id}
