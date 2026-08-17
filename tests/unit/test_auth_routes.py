"""Unit tests for auth route handlers."""

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import HTTPException
from starlette.responses import Response

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
    monkeypatch.setattr(auth, "llm_processing_allowed", AsyncMock(return_value=True))
    monkeypatch.setattr(
        auth,
        "issue_token_pair",
        AsyncMock(
            return_value={
                "access_token": "tok",
                "refresh_token": "ref",
                "token_type": "bearer",
                "expires_in": 900,
            }
        ),
    )
    monkeypatch.setattr(auth, "scopes_for_role", lambda role: ["read:own", "write:own"])
    result = await auth.login_endpoint(
        LoginRequest(email="p@test.com", password="securepass1", tenant_id=tenant_id),
        Response(),
        session,
    )
    assert result.access_token == "tok"
    assert result.refresh_token == "ref"


@pytest.mark.asyncio
async def test_login_endpoint_invalid_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    session = AsyncMock()
    monkeypatch.setattr(auth, "authenticate_user", AsyncMock(return_value=None))
    with pytest.raises(HTTPException) as exc:
        await auth.login_endpoint(
            LoginRequest(email="p@test.com", password="wrong", tenant_id=uuid4()),
            Response(),
            session,
        )
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_login_disabled_in_production(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.core.config import Settings, get_settings

    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    monkeypatch.setattr(auth, "get_settings", lambda: Settings())
    with pytest.raises(HTTPException) as exc:
        await auth.login_endpoint(
            LoginRequest(email="p@test.com", password="securepass1", tenant_id=uuid4()),
            Response(),
            AsyncMock(),
        )
    assert exc.value.status_code == 403
    get_settings.cache_clear()


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


@pytest.mark.asyncio
async def test_oidc_callback_invalid_state() -> None:
    from synapsemd_platform.api.schemas import OidcCallbackRequest

    with pytest.raises(HTTPException) as exc:
        await auth.oidc_callback_endpoint(
            OidcCallbackRequest(code="x", state="missing"),
            Response(),
            AsyncMock(),
        )
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_oidc_token_unconfigured() -> None:
    from synapsemd_platform.api.schemas import OidcTokenRequest

    with pytest.raises(HTTPException) as exc:
        await auth.oidc_token_exchange(
            OidcTokenRequest(id_token="x", tenant_id=uuid4()),
            Response(),
            AsyncMock(),
        )
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_oidc_callback_success(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.api.schemas import OidcCallbackRequest
    from synapsemd_platform.auth.oidc import put_oidc_state

    tenant_id = uuid4()
    user = SimpleNamespace(id=uuid4(), tenant_id=tenant_id, role="clinician")
    put_oidc_state(state="st1", code_verifier="ver", tenant_id=str(tenant_id), redirect_uri="http://cb")

    class FakeClient:
        def enabled(self) -> bool:
            return True

        async def exchange_code(self, **kwargs):
            return {"id_token": "idt"}

        def validate_id_token(self, token: str) -> dict:
            return {"sub": "idp-1", "iss": "http://idp", "amr": ["mfa"], "groups": ["clinician"]}

    monkeypatch.setattr(auth, "OidcClient", lambda: FakeClient())
    monkeypatch.setattr(auth, "_upsert_oidc_user", AsyncMock(return_value=user))
    monkeypatch.setattr(auth, "llm_processing_allowed", AsyncMock(return_value=True))
    monkeypatch.setattr(
        auth,
        "issue_token_pair",
        AsyncMock(return_value={"access_token": "a", "refresh_token": "r", "token_type": "bearer", "expires_in": 900}),
    )
    result = await auth.oidc_callback_endpoint(
        OidcCallbackRequest(code="code", state="st1"),
        Response(),
        AsyncMock(),
    )
    assert result.access_token == "a"


@pytest.mark.asyncio
async def test_update_consent_returns_new_token() -> None:
    from synapsemd_platform.api.schemas import ConsentUpdateRequest
    from synapsemd_platform.auth.jwt import TokenClaims

    claims = TokenClaims(sub=uuid4(), org=uuid4(), roles=["patient"], scope=["write:own"])
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(auth, "upsert_consent", AsyncMock())
    result = await auth.update_consent_endpoint(
        ConsentUpdateRequest(purpose="llm_processing", granted=False),
        claims,
        AsyncMock(),
    )
    monkeypatch.undo()
    assert result["granted"] is False
    assert result["access_token"]


@pytest.mark.asyncio
async def test_break_glass_forbidden_for_patient() -> None:
    from synapsemd_platform.api.schemas import BreakGlassRequest
    from synapsemd_platform.core.context import RequestContext

    ctx = RequestContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=("patient",),
        scopes=("read:own", "write:own"),
    )
    with pytest.raises(HTTPException) as exc:
        await auth.break_glass_endpoint(BreakGlassRequest(reason="need access now"), Response(), ctx, AsyncMock())
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_break_glass_issues_token(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.api.schemas import BreakGlassRequest
    from synapsemd_platform.core.context import RequestContext

    ctx = RequestContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=("clinician",),
        scopes=("read:own", "write:own", "read:org"),
        amr=("mfa",),
    )
    monkeypatch.setattr(auth, "activate_break_glass", AsyncMock())
    monkeypatch.setattr(
        auth,
        "issue_token_pair",
        AsyncMock(return_value={"access_token": "bg", "refresh_token": "r", "token_type": "bearer", "expires_in": 900}),
    )
    result = await auth.break_glass_endpoint(
        BreakGlassRequest(reason="emergency review"),
        Response(),
        ctx,
        AsyncMock(),
    )
    assert result.access_token == "bg"


@pytest.mark.asyncio
async def test_oidc_token_exchange_success(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.api.schemas import OidcTokenRequest

    tenant_id = uuid4()
    user = SimpleNamespace(id=uuid4(), tenant_id=tenant_id, role="patient")

    class FakeClient:
        def enabled(self) -> bool:
            return True

        def validate_id_token(self, token: str) -> dict:
            return {"sub": "idp-2", "iss": "http://idp", "amr": ["pwd"]}

    monkeypatch.setattr(auth, "OidcClient", lambda: FakeClient())
    monkeypatch.setattr(auth, "_upsert_oidc_user", AsyncMock(return_value=user))
    monkeypatch.setattr(auth, "llm_processing_allowed", AsyncMock(return_value=True))
    monkeypatch.setattr(
        auth,
        "issue_token_pair",
        AsyncMock(return_value={"access_token": "ex", "refresh_token": "r", "token_type": "bearer", "expires_in": 900}),
    )
    result = await auth.oidc_token_exchange(
        OidcTokenRequest(id_token="idt", tenant_id=tenant_id),
        Response(),
        AsyncMock(),
    )
    assert result.access_token == "ex"


@pytest.mark.asyncio
async def test_refresh_success(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.api.schemas import RefreshRequest

    user_id = uuid4()
    tenant_id = uuid4()
    current = SimpleNamespace(user_id=user_id, tenant_id=tenant_id)
    user = SimpleNamespace(id=user_id, tenant_id=tenant_id, role="patient")
    session = AsyncMock()
    session.execute = AsyncMock(return_value=SimpleNamespace(scalar_one_or_none=lambda: user))
    monkeypatch.setattr(auth, "rotate_refresh_token", AsyncMock(return_value=current))
    monkeypatch.setattr(auth, "llm_processing_allowed", AsyncMock(return_value=True))
    monkeypatch.setattr(auth, "create_session", AsyncMock(return_value=(None, "newref")))
    monkeypatch.setattr(auth, "create_access_token", lambda **kwargs: "newaccess")
    monkeypatch.setattr(auth, "scopes_for_role", lambda role: ["read:own"])
    result = await auth.refresh_endpoint(RefreshRequest(refresh_token="old"), Response(), session)
    assert result.refresh_token == "newref"


@pytest.mark.asyncio
async def test_refresh_invalid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.api.schemas import RefreshRequest

    monkeypatch.setattr(auth, "rotate_refresh_token", AsyncMock(return_value=None))
    with pytest.raises(HTTPException) as exc:
        await auth.refresh_endpoint(RefreshRequest(refresh_token="nope"), Response(), AsyncMock())
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_oidc_login_returns_url(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.api.schemas import OidcLoginRequest
    from synapsemd_platform.core.config import Settings, get_settings

    monkeypatch.setenv("OIDC_ISSUER", "http://localhost:8082/realms/synapsemd")
    monkeypatch.setenv("OIDC_CLIENT_ID", "synapsemd-api")
    get_settings.cache_clear()
    monkeypatch.setattr(auth, "get_settings", lambda: Settings())
    result = await auth.oidc_login_endpoint(OidcLoginRequest(tenant_id=uuid4()))
    assert "code_challenge" in result["authorization_url"]
    assert result["state"]
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_upsert_oidc_user_creates_identity() -> None:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from synapsemd_platform.core.database import Base

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        tenant_id = uuid4()
        user = await auth._upsert_oidc_user(
            session,
            tenant_id=tenant_id,
            claims={"sub": "idp-sub", "iss": "http://idp", "email": "c@example.com", "groups": ["clinician"]},
        )
        assert user.role == "clinician"
        again = await auth._upsert_oidc_user(
            session,
            tenant_id=tenant_id,
            claims={"sub": "idp-sub", "iss": "http://idp", "email": "c@example.com"},
        )
        assert again.id == user.id
    await engine.dispose()
