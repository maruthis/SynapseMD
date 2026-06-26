import pytest

from synapsemd_platform.core.config import Settings, get_settings
from synapsemd_platform.llm.providers import BaaGateError, create_provider


def test_baa_gate_blocks_production_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_BAA_SIGNED", "false")
    get_settings.cache_clear()
    with pytest.raises(BaaGateError):
        create_provider("anthropic")


def test_baa_gate_allows_signed_production_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_BAA_SIGNED", "true")
    get_settings.cache_clear()
    provider = create_provider("anthropic")
    assert provider is not None


def test_mock_provider_in_development() -> None:
    provider = create_provider("mock")
    assert provider is not None
