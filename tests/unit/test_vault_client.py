"""Unit tests for async HashiCorp Vault client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from synapsemd_platform.core.vault import VaultClient, get_vault_client


@pytest.mark.asyncio
async def test_vault_client_read_secret() -> None:
    client = VaultClient("http://vault:8200", "token")
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {"data": {"data": {"key": "value"}}}

    with patch("synapsemd_platform.core.vault.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=response)
        result = await client.read_secret("secret/data/test")

    assert result == {"key": "value"}


@pytest.mark.asyncio
async def test_vault_client_write_secret() -> None:
    client = VaultClient("http://vault:8200", "token")
    response = MagicMock()
    response.raise_for_status = MagicMock()

    with patch("synapsemd_platform.core.vault.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=response)
        await client.write_secret("secret/data/test", {"key": "value"})


def test_get_vault_client_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VAULT_ENABLED", "false")
    from synapsemd_platform.core.config import get_settings

    get_settings.cache_clear()
    assert get_vault_client() is None
    get_settings.cache_clear()


def test_get_vault_client_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VAULT_ENABLED", "true")
    monkeypatch.setenv("VAULT_URL", "http://vault:8200")
    monkeypatch.setenv("VAULT_TOKEN", "dev")
    from synapsemd_platform.core.config import get_settings

    get_settings.cache_clear()
    client = get_vault_client()
    assert client is not None
    assert client.url == "http://vault:8200"
    get_settings.cache_clear()
