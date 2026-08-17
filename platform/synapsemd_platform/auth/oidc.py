"""OIDC authorization-code + PKCE client and ID-token validation."""

from __future__ import annotations

import base64
import hashlib
import secrets
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx
from jose import JWTError, jwt

from synapsemd_platform.core.config import Settings, get_settings

_pending_states: dict[str, dict[str, Any]] = {}
STATE_TTL_SECONDS = 600


def generate_pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


def put_oidc_state(*, state: str, code_verifier: str, tenant_id: str, redirect_uri: str) -> None:
    _pending_states[state] = {
        "code_verifier": code_verifier,
        "tenant_id": tenant_id,
        "redirect_uri": redirect_uri,
        "exp": time.time() + STATE_TTL_SECONDS,
    }


def pop_oidc_state(state: str) -> dict[str, Any] | None:
    record = _pending_states.pop(state, None)
    if record is None:
        return None
    if record["exp"] < time.time():
        return None
    return record


def clear_oidc_states() -> None:
    _pending_states.clear()


@dataclass
class OidcTokens:
    access_token: str | None
    id_token: str
    refresh_token: str | None
    claims: dict[str, Any]


class OidcClient:
    def __init__(self, settings: Settings | None = None, http: httpx.AsyncClient | None = None) -> None:
        self.settings = settings or get_settings()
        self._http = http

    def enabled(self) -> bool:
        return bool(self.settings.oidc_issuer and self.settings.oidc_client_id)

    def authorization_url(
        self,
        *,
        state: str,
        code_challenge: str,
        redirect_uri: str,
        tenant_id: str,
    ) -> str:
        issuer = self.settings.oidc_issuer.rstrip("/")
        params = {
            "response_type": "code",
            "client_id": self.settings.oidc_client_id,
            "redirect_uri": redirect_uri,
            "scope": "openid profile email groups",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "audience": self.settings.oidc_audience,
            "tenant_id": tenant_id,
        }
        return f"{issuer}/protocol/openid-connect/auth?{urlencode(params)}"

    async def exchange_code(self, *, code: str, code_verifier: str, redirect_uri: str) -> dict[str, Any]:
        issuer = self.settings.oidc_issuer.rstrip("/")
        token_url = f"{issuer}/protocol/openid-connect/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.settings.oidc_client_id,
            "client_secret": self.settings.oidc_client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
        }
        client = self._http or httpx.AsyncClient(timeout=10.0)
        close = self._http is None
        try:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            return response.json()
        finally:
            if close:
                await client.aclose()

    def validate_id_token(self, id_token: str) -> dict[str, Any]:
        """Validate an IdP ID token. Dev/tests may use the platform HS256 secret."""
        settings = self.settings
        try:
            return jwt.decode(
                id_token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
                audience=settings.oidc_audience,
                issuer=settings.oidc_issuer or None,
                options={
                    "verify_aud": bool(settings.oidc_audience),
                    "verify_iss": bool(settings.oidc_issuer),
                },
            )
        except JWTError as exc:
            raise ValueError("Invalid ID token") from exc
