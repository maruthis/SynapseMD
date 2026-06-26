"""HashiCorp Vault integration for PHI token storage."""

from typing import Any

import httpx

from synapsemd_platform.core.config import get_settings


class VaultClient:
    def __init__(self, url: str, token: str) -> None:
        self.url = url.rstrip("/")
        self.token = token

    async def read_secret(self, path: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.url}/v1/{path}",
                headers={"X-Vault-Token": self.token},
            )
            response.raise_for_status()
            return response.json().get("data", {}).get("data", {})

    async def write_secret(self, path: str, data: dict[str, Any]) -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{self.url}/v1/{path}",
                headers={"X-Vault-Token": self.token},
                json={"data": data},
            )
            response.raise_for_status()


def get_vault_client() -> VaultClient | None:
    settings = get_settings()
    if not settings.vault_enabled or not settings.vault_url or not settings.vault_token:
        return None
    return VaultClient(settings.vault_url, settings.vault_token)
