from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from synapsemd_platform.auth.jwt import create_access_token
from synapsemd_platform.auth.middleware import get_current_claims
from synapsemd_platform.core.config import get_settings
from tests.helpers import make_token


@pytest.mark.asyncio
async def test_privileged_role_without_mfa_denied_in_production(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    token = create_access_token(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["clinician"],
        amr=["pwd"],
    )
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    with pytest.raises(HTTPException) as exc:
        await get_current_claims(creds)
    assert exc.value.status_code == 401
    assert "MFA" in exc.value.detail
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_privileged_role_with_mfa_allowed_in_production(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    token = create_access_token(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["clinician"],
        amr=["pwd", "mfa"],
    )
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    claims = await get_current_claims(creds)
    assert "clinician" in claims.roles
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_patient_without_mfa_allowed_in_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    token = make_token(roles=["patient"], amr=["pwd"])
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    claims = await get_current_claims(creds)
    assert "patient" in claims.roles
    get_settings.cache_clear()


def test_access_token_default_ttl_is_15_minutes() -> None:
    from jose import jwt as jose_jwt

    from synapsemd_platform.core.config import get_settings as gs

    token = make_token()
    payload = jose_jwt.decode(
        token,
        gs().jwt_secret,
        algorithms=[gs().jwt_algorithm],
        audience=gs().oidc_audience,
    )
    exp = datetime.fromtimestamp(payload["exp"], tz=UTC)
    delta = exp - datetime.now(UTC)
    assert timedelta(minutes=10) < delta < timedelta(minutes=16)
