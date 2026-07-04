"""Unit tests for Vault-backed PHI token storage."""

from unittest.mock import MagicMock, patch

import pytest

from synapsemd_platform.anonymization.engine import AnonymizationEngine, TokenVault
from synapsemd_platform.anonymization.vault_store import VaultTokenVault


def test_vault_token_store_roundtrip() -> None:
    vault = VaultTokenVault("http://vault:8200", "test-token")
    vault._memory_cache["user-1"] = {}

    with patch.object(vault, "_write_map") as mock_write:
        vault.store_tokens("user-1", {"TOKEN_EMAIL_abc": "test@example.com"})
        mock_write.assert_called_once()
        stored = mock_write.call_args[0][1]
        assert stored["TOKEN_EMAIL_abc"] == "test@example.com"

    with patch.object(vault, "_read_map", return_value={"TOKEN_EMAIL_abc": "test@example.com"}):
        assert vault.resolve("user-1", "TOKEN_EMAIL_abc") == "test@example.com"


def test_vault_read_map_from_http() -> None:
    vault = VaultTokenVault("http://vault:8200", "test-token")
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"data": {"data": {"TOKEN_PHONE_x": "555-0000"}}}
    response.raise_for_status = MagicMock()

    with patch("synapsemd_platform.anonymization.vault_store.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = response
        assert vault._read_map("user-2") == {"TOKEN_PHONE_x": "555-0000"}


def test_vault_read_map_404_returns_empty() -> None:
    vault = VaultTokenVault("http://vault:8200", "test-token")
    response = MagicMock()
    response.status_code = 404

    with patch("synapsemd_platform.anonymization.vault_store.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = response
        assert vault._read_map("user-3") == {}


def test_vault_write_map_http() -> None:
    vault = VaultTokenVault("http://vault:8200", "test-token")
    response = MagicMock()
    response.raise_for_status = MagicMock()

    with patch("synapsemd_platform.anonymization.vault_store.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.post.return_value = response
        vault._write_map("user-4", {"TOKEN_EMAIL_a": "a@b.com"})
        assert vault._memory_cache["user-4"]["TOKEN_EMAIL_a"] == "a@b.com"


def test_engine_uses_vault_when_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VAULT_ENABLED", "true")
    monkeypatch.setenv("VAULT_URL", "http://vault:8200")
    monkeypatch.setenv("VAULT_TOKEN", "dev-token")
    from synapsemd_platform.core.config import get_settings

    get_settings.cache_clear()
    engine = AnonymizationEngine()
    assert isinstance(engine.vault, VaultTokenVault)
    get_settings.cache_clear()


def test_token_vault_deanonymize() -> None:
    base = TokenVault()
    base.store_tokens("user-1", {"TOKEN_EMAIL_abc": "test@example.com"})
    result = base.deanonymize("user-1", "Email: TOKEN_EMAIL_abc", {"TOKEN_EMAIL_abc": "x"})
    assert "test@example.com" in result
