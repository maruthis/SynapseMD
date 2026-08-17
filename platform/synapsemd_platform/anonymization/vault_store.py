"""HashiCorp Vault-backed PHI token store for production deployments."""

from __future__ import annotations

import httpx

from synapsemd_platform.anonymization.engine import TokenVault


class VaultTokenVault(TokenVault):
    """Persists anonymization token maps in Vault KV v2 (tenant-scoped)."""

    durable = True

    def __init__(self, url: str, token: str, *, mount: str = "secret") -> None:
        self.url = url.rstrip("/")
        self.token = token
        self.mount = mount
        self._memory_cache: dict[str, dict[str, str]] = {}

    def _secret_path(self, user_id: str, tenant_id: str | None = None) -> str:
        tenant = tenant_id or "default"
        return f"{self.mount}/data/synapsemd/tokens/{tenant}/{user_id}"

    def _cache_key(self, user_id: str, tenant_id: str | None = None) -> str:
        if tenant_id:
            return f"{tenant_id}:{user_id}"
        return user_id

    def _read_map(self, user_id: str, tenant_id: str | None = None) -> dict[str, str]:
        key = self._cache_key(user_id, tenant_id)
        if key in self._memory_cache:
            return dict(self._memory_cache[key])
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                f"{self.url}/v1/{self._secret_path(user_id, tenant_id)}",
                headers={"X-Vault-Token": self.token},
            )
            if response.status_code == 404:
                return {}
            response.raise_for_status()
            data = response.json().get("data", {}).get("data", {})
            return {str(k): str(v) for k, v in data.items() if not str(k).startswith("_")}

    def _write_map(
        self,
        user_id: str,
        token_map: dict[str, str],
        tenant_id: str | None = None,
    ) -> None:
        from synapsemd_platform.core.config import get_settings

        payload = dict(token_map)
        kms_key = get_settings().kms_master_key_id
        if kms_key:
            payload["_kms_key_id"] = kms_key
        self._memory_cache[self._cache_key(user_id, tenant_id)] = dict(token_map)
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{self.url}/v1/{self._secret_path(user_id, tenant_id)}",
                headers={"X-Vault-Token": self.token},
                json={"data": payload},
            )
            response.raise_for_status()

    def store_tokens(
        self,
        user_id: str,
        token_map: dict[str, str],
        *,
        tenant_id: str | None = None,
    ) -> None:
        existing = self._read_map(user_id, tenant_id)
        existing.update(token_map)
        self._write_map(user_id, existing, tenant_id=tenant_id)

    def resolve(self, user_id: str, token: str, tenant_id: str | None = None) -> str | None:
        return self._read_map(user_id, tenant_id).get(token)

    def delete_tokens(self, user_id: str, *, tenant_id: str | None = None) -> int:
        key = self._cache_key(user_id, tenant_id)
        cached = self._memory_cache.pop(key, {})
        with httpx.Client(timeout=10.0) as client:
            response = client.delete(
                f"{self.url}/v1/{self._secret_path(user_id, tenant_id)}",
                headers={"X-Vault-Token": self.token},
            )
            if response.status_code not in {200, 204, 404}:
                response.raise_for_status()
        return len(cached)
