import hashlib
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

import httpx

from synapsemd_platform.core.config import get_settings
from synapsemd_platform.llm.router import RoutingDecision


@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    tokens_in: int
    tokens_out: int
    latency_ms: int


class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str, decision: RoutingDecision) -> LLMResponse:
        pass


class MockLLMProvider(LLMProvider):
    async def complete(self, prompt: str, decision: RoutingDecision) -> LLMResponse:
        start = time.perf_counter()
        content = (
            f"[{decision.model}] Processed health command. "
            "This is a mock response for development. Consult a healthcare provider for medical decisions."
        )
        latency = int((time.perf_counter() - start) * 1000)
        return LLMResponse(
            content=content,
            model=decision.model,
            provider=decision.provider,
            tokens_in=len(prompt.split()),
            tokens_out=len(content.split()),
            latency_ms=latency,
        )


class AnthropicHealthProvider(LLMProvider):
    """Anthropic healthcare-approved deployment adapter."""

    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    async def complete(self, prompt: str, decision: RoutingDecision) -> LLMResponse:
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": decision.model,
                    "max_tokens": decision.max_tokens,
                    "temperature": decision.temperature,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            data = response.json()
        content = data["content"][0]["text"]
        usage = data.get("usage", {})
        latency = int((time.perf_counter() - start) * 1000)
        return LLMResponse(
            content=content,
            model=decision.model,
            provider="anthropic-health",
            tokens_in=usage.get("input_tokens", 0),
            tokens_out=usage.get("output_tokens", 0),
            latency_ms=latency,
        )


class OpenAIHealthProvider(LLMProvider):
    """OpenAI healthcare-approved deployment adapter."""

    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    async def complete(self, prompt: str, decision: RoutingDecision) -> LLMResponse:
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": decision.model,
                    "max_tokens": decision.max_tokens,
                    "temperature": decision.temperature,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            data = response.json()
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        latency = int((time.perf_counter() - start) * 1000)
        return LLMResponse(
            content=content,
            model=decision.model,
            provider="openai-health",
            tokens_in=usage.get("prompt_tokens", 0),
            tokens_out=usage.get("completion_tokens", 0),
            latency_ms=latency,
        )


class GoogleHealthProvider(LLMProvider):
    """Google Gemini healthcare-approved deployment adapter."""

    def __init__(self, api_key: str, base_url: str) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    async def complete(self, prompt: str, decision: RoutingDecision) -> LLMResponse:
        start = time.perf_counter()
        model_path = decision.model
        url = f"{self.base_url}/v1beta/models/{model_path}:generateContent?key={self.api_key}"
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": decision.temperature,
                        "maxOutputTokens": decision.max_tokens,
                    },
                },
            )
            response.raise_for_status()
            data = response.json()
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        latency = int((time.perf_counter() - start) * 1000)
        return LLMResponse(
            content=content,
            model=decision.model,
            provider="google-health",
            tokens_in=len(prompt.split()),
            tokens_out=len(content.split()),
            latency_ms=latency,
        )


class BaaGateError(Exception):
    pass


def _require_baa(provider_name: str, baa_signed: bool, app_env: str) -> None:
    if app_env in {"staging", "production"} and not baa_signed:
        raise BaaGateError(
            f"Provider '{provider_name}' requires a signed BAA before use in {app_env}"
        )


def create_provider(provider_name: str | None = None) -> LLMProvider:
    settings = get_settings()
    name = provider_name or settings.llm_default_provider

    if name == "mock":
        return MockLLMProvider()

    if name == "anthropic":
        _require_baa("anthropic", settings.anthropic_baa_signed, settings.app_env)
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")
        return AnthropicHealthProvider(settings.anthropic_api_key, settings.anthropic_base_url)

    if name == "openai":
        _require_baa("openai", settings.openai_baa_signed, settings.app_env)
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        return OpenAIHealthProvider(settings.openai_api_key, settings.openai_base_url)

    if name == "google":
        _require_baa("google", settings.google_baa_signed, settings.app_env)
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY is required")
        return GoogleHealthProvider(settings.google_api_key, settings.google_base_url)

    raise ValueError(f"Unknown LLM provider: {name}")


class LLMOrchestrator:
    def __init__(self, provider: LLMProvider | None = None) -> None:
        self.provider = provider or create_provider()

    async def execute(self, prompt: str, decision: RoutingDecision) -> LLMResponse:
        try:
            return await self.provider.complete(prompt, decision)
        except Exception:
            if decision.fallback_model and decision.fallback_model != decision.model:
                fallback_decision = RoutingDecision(
                    model=decision.fallback_model,
                    provider=decision.provider,
                    max_tokens=decision.max_tokens,
                    temperature=decision.temperature,
                    require_human_review=decision.require_human_review,
                    fallback_model=decision.model,
                )
                return await self.provider.complete(prompt, fallback_decision)
            raise


def hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()
