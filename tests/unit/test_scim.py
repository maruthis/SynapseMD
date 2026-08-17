from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from synapsemd_platform.api.main import create_app
from synapsemd_platform.core.config import get_settings
from tests.helpers import make_token


@pytest.mark.asyncio
async def test_scim_list_requires_admin() -> None:
    app = create_app()
    token = make_token(roles=["patient"], scopes=["read:own", "write:own"])
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        denied = await client.get(
            "/api/v1/scim/v2/Users",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert denied.status_code == 403
        admin = make_token(roles=["admin"], scopes=["admin"])
        allowed = await client.get(
            "/api/v1/scim/v2/Users",
            headers={"Authorization": f"Bearer {admin}"},
        )
        assert allowed.status_code == 200
        body = allowed.json()
        assert body["totalResults"] >= 0
        assert isinstance(body["Resources"], list)
        assert "ListResponse" in body["schemas"][0]


@pytest.mark.asyncio
async def test_scim_create_is_stub() -> None:
    app = create_app()
    admin = make_token(roles=["admin"], scopes=["admin"])
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/scim/v2/Users",
            headers={"Authorization": f"Bearer {admin}"},
            json={"userName": "x"},
        )
        assert response.status_code == 501


def test_create_app_cors_not_wildcard_in_staging(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("CORS_ORIGINS", "https://clinic.example.com")
    get_settings.cache_clear()
    app = create_app()
    cors = next(m for m in app.user_middleware if m.cls.__name__ == "CORSMiddleware")
    assert "https://clinic.example.com" in cors.kwargs["allow_origins"]
    assert "*" not in cors.kwargs["allow_origins"]
    get_settings.cache_clear()
