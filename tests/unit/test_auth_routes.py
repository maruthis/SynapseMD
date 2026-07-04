"""Unit tests for auth route handlers."""

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from synapsemd_platform.api.routes import auth
from synapsemd_platform.api.schemas import LoginRequest, TenantCreate, UserRegister


@pytest.mark.asyncio
async def test_create_tenant_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    tenant_id = uuid4()
    fake_tenant = SimpleNamespace(id=tenant_id, name="Clinic", plan="starter")
    session = AsyncMock()
    monkeypatch.setattr(auth, "create_tenant", AsyncMock(return_value=fake_tenant))
    result = await auth.create_tenant_endpoint(TenantCreate(name="Clinic", plan="starter"), session)
    assert result.id == tenant_id
    assert result.name == "Clinic"


@pytest.mark.asyncio
async def test_register_user_endpoint_success(monkeypatch: pytest.MonkeyPatch) -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    fake_user = SimpleNamespace(id=user_id, tenant_id=tenant_id, role="patient")
    session = AsyncMock()
    monkeypatch.setattr(auth, "register_user", AsyncMock(return_value=fake_user))
    result = await auth.register_user_endpoint(
        tenant_id,
        UserRegister(email="p@test.com", password="securepass1", role="patient"),
        session,
    )
    assert result.id == user_id
    assert result.role == "patient"


@pytest.mark.asyncio
async def test_register_user_endpoint_invalid_role() -> None:
    with pytest.raises(HTTPException) as exc:
        await auth.register_user_endpoint(
            uuid4(),
            UserRegister(email="p@test.com", password="securepass1", role="invalid"),
            AsyncMock(),
        )
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_login_endpoint_success(monkeypatch: pytest.MonkeyPatch) -> None:
    user_id = uuid4()
    tenant_id = uuid4()
    fake_user = SimpleNamespace(id=user_id, tenant_id=tenant_id, role="patient")
    session = AsyncMock()
    monkeypatch.setattr(auth, "authenticate_user", AsyncMock(return_value=fake_user))
    monkeypatch.setattr(auth, "scopes_for_role", lambda role: ["read:own", "write:own"])
    result = await auth.login_endpoint(
        LoginRequest(email="p@test.com", password="securepass1", tenant_id=tenant_id),
        session,
    )
    assert result.access_token


@pytest.mark.asyncio
async def test_login_endpoint_invalid_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    session = AsyncMock()
    monkeypatch.setattr(auth, "authenticate_user", AsyncMock(return_value=None))
    with pytest.raises(HTTPException) as exc:
        await auth.login_endpoint(
            LoginRequest(email="p@test.com", password="wrong", tenant_id=uuid4()),
            session,
        )
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_me_endpoint_returns_role_scopes() -> None:
    from synapsemd_platform.auth.jwt import TokenClaims

    claims = TokenClaims(
        sub=uuid4(),
        org=uuid4(),
        roles=["patient"],
        scope=["read:own", "write:own"],
    )
    result = await auth.me_endpoint(claims=claims)
    assert "patient" in result["role_scopes"]
    assert result["user_id"] == str(claims.sub)
