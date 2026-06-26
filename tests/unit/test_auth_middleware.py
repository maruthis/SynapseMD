import pytest
from fastapi import HTTPException
from starlette.requests import Request

from synapsemd_platform.auth.middleware import get_current_claims, require_scope
from tests.helpers import make_token


@pytest.mark.asyncio
async def test_get_current_claims_missing_credentials() -> None:
    with pytest.raises(HTTPException) as exc:
        await get_current_claims(None)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_claims_invalid_scheme() -> None:
    from fastapi.security import HTTPAuthorizationCredentials

    creds = HTTPAuthorizationCredentials(scheme="Basic", credentials="abc")
    with pytest.raises(HTTPException) as exc:
        await get_current_claims(creds)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_claims_invalid_token() -> None:
    from fastapi.security import HTTPAuthorizationCredentials

    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="bad-token")
    with pytest.raises(HTTPException) as exc:
        await get_current_claims(creds)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_claims_valid() -> None:
    from fastapi.security import HTTPAuthorizationCredentials

    token = make_token()
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    claims = await get_current_claims(creds)
    assert claims.roles == ["patient"]


@pytest.mark.asyncio
async def test_require_scope_forbidden() -> None:
    checker = require_scope("audit")
    token = make_token(scopes=["read:own"])
    from fastapi.security import HTTPAuthorizationCredentials

    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    claims = await get_current_claims(creds)
    with pytest.raises(HTTPException) as exc:
        await checker(claims)
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_require_scope_allowed() -> None:
    checker = require_scope("read:own")
    token = make_token(scopes=["read:own", "write:own"])
    from fastapi.security import HTTPAuthorizationCredentials

    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    claims = await get_current_claims(creds)
    result = await checker(claims)
    assert result.sub == claims.sub
