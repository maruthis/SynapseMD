from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from jose import jwt

from synapsemd_platform.auth.oidc import (
    OidcClient,
    clear_oidc_states,
    generate_pkce_pair,
    pop_oidc_state,
    put_oidc_state,
)
from synapsemd_platform.core.config import Settings, get_settings


def test_pkce_and_state_store() -> None:
    clear_oidc_states()
    verifier, challenge = generate_pkce_pair()
    assert verifier
    assert challenge
    assert verifier != challenge
    state = "abc"
    put_oidc_state(state=state, code_verifier=verifier, tenant_id=str(uuid4()), redirect_uri="http://x")
    record = pop_oidc_state(state)
    assert record is not None
    assert record["code_verifier"] == verifier
    assert pop_oidc_state(state) is None


def test_authorization_url_includes_pkce(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OIDC_ISSUER", "http://localhost:8082/realms/synapsemd")
    monkeypatch.setenv("OIDC_CLIENT_ID", "synapsemd-api")
    get_settings.cache_clear()
    client = OidcClient(Settings())
    url = client.authorization_url(
        state="st",
        code_challenge="chal",
        redirect_uri="http://localhost:8000/callback",
        tenant_id=str(uuid4()),
    )
    assert "code_challenge=chal" in url
    assert "code_challenge_method=S256" in url
    assert client.enabled() is True
    get_settings.cache_clear()


def test_validate_id_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OIDC_ISSUER", "http://localhost:8082/realms/synapsemd")
    monkeypatch.setenv("OIDC_CLIENT_ID", "synapsemd-api")
    get_settings.cache_clear()
    settings = Settings()
    tenant = uuid4()
    payload = {
        "sub": str(uuid4()),
        "iss": settings.oidc_issuer,
        "aud": settings.oidc_audience,
        "email": "clinician@example.com",
        "groups": ["synapsemd-clinicians"],
        "amr": ["pwd", "mfa"],
        "org": str(tenant),
        "exp": datetime.now(UTC) + timedelta(minutes=5),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    claims = OidcClient(settings).validate_id_token(token)
    assert claims["email"] == "clinician@example.com"
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_exchange_code_posts_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OIDC_ISSUER", "http://localhost:8082/realms/synapsemd")
    monkeypatch.setenv("OIDC_CLIENT_ID", "synapsemd-api")
    get_settings.cache_clear()

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"id_token": "abc"}

    class FakeHttp:
        async def post(self, url, data):
            assert "token" in url
            return FakeResponse()

        async def aclose(self) -> None:
            return None

    client = OidcClient(Settings(), http=FakeHttp())  # type: ignore[arg-type]
    payload = await client.exchange_code(code="c", code_verifier="v", redirect_uri="http://cb")
    assert payload["id_token"] == "abc"
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_oidc_login_404_when_unconfigured() -> None:
    from fastapi import HTTPException

    from synapsemd_platform.api.routes import auth
    from synapsemd_platform.api.schemas import OidcLoginRequest

    with pytest.raises(HTTPException) as exc:
        await auth.oidc_login_endpoint(OidcLoginRequest(tenant_id=uuid4()))
    assert exc.value.status_code == 404
