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


def test_unknown_provider_raises() -> None:
    with pytest.raises(ValueError, match="Unknown LLM provider"):
        create_provider("not-a-provider")


def test_openai_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("OPENAI_BAA_SIGNED", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "")
    get_settings.cache_clear()
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        create_provider("openai")
    get_settings.cache_clear()


def test_google_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("GOOGLE_BAA_SIGNED", "true")
    monkeypatch.setenv("GOOGLE_API_KEY", "")
    get_settings.cache_clear()
    with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
        create_provider("google")
    get_settings.cache_clear()


def test_vllm_provider_created() -> None:
    provider = create_provider("vllm")
    assert provider is not None


@pytest.mark.asyncio
async def test_vllm_provider_complete_mocked() -> None:
    from unittest.mock import AsyncMock, MagicMock, patch

    from synapsemd_platform.llm.providers import VllmProvider
    from synapsemd_platform.llm.router import RoutingDecision

    provider = VllmProvider("http://vllm.local/v1", "local-model", cert="c.pem", key="k.pem")
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {
        "choices": [{"message": {"content": "ok"}}],
        "usage": {"prompt_tokens": 2, "completion_tokens": 1},
    }
    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = AsyncMock(return_value=response)
    with patch("synapsemd_platform.llm.providers.httpx.AsyncClient", return_value=mock_client):
        result = await provider.complete(
            "hello",
            RoutingDecision("vllm-local", "vllm", 128, 0.1, False, "vllm-local"),
        )
    assert result.provider == "vllm"
    assert result.content == "ok"
    mock_client.post.assert_awaited_once()
