"""HashiCorp Vault-backed PHI token store for production deployments."""

from __future__ import annotations

import httpx

from synapsemd_platform.anonymization.engine import TokenVault


class VaultTokenVault(TokenVault):
    """Persists anonymization token maps in Vault KV v2."""

    def __init__(self, url: str, token: str, *, mount: str = "secret") -> None:
        self.url = url.rstrip("/")
        self.token = token
        self.mount = mount
        self._memory_cache: dict[str, dict[str, str]] = {}

    def _secret_path(self, user_id: str) -> str:
        return f"{self.mount}/data/synapsemd/tokens/{user_id}"

    def _read_map(self, user_id: str) -> dict[str, str]:
        if user_id in self._memory_cache:
            return dict(self._memory_cache[user_id])
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                f"{self.url}/v1/{self._secret_path(user_id)}",
                headers={"X-Vault-Token": self.token},
            )
            if response.status_code == 404:
                return {}
            response.raise_for_status()
            data = response.json().get("data", {}).get("data", {})
            return {str(k): str(v) for k, v in data.items()}

    def _write_map(self, user_id: str, token_map: dict[str, str]) -> None:
        self._memory_cache[user_id] = dict(token_map)
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{self.url}/v1/{self._secret_path(user_id)}",
                headers={"X-Vault-Token": self.token},
                json={"data": token_map},
            )
            response.raise_for_status()

    def store_tokens(self, user_id: str, token_map: dict[str, str]) -> None:
        existing = self._read_map(user_id)
        existing.update(token_map)
        self._write_map(user_id, existing)

    def resolve(self, user_id: str, token: str) -> str | None:
        return self._read_map(user_id).get(token)
