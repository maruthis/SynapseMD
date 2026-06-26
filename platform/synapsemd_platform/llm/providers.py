import hashlib
import time
from dataclasses import dataclass

from synapsemd_platform.llm.router import RoutingDecision


@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    tokens_in: int
    tokens_out: int
    latency_ms: int


class MockLLMProvider:
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


class LLMOrchestrator:
    def __init__(self, provider: MockLLMProvider | None = None) -> None:
        self.provider = provider or MockLLMProvider()

    async def execute(self, prompt: str, decision: RoutingDecision) -> LLMResponse:
        return await self.provider.complete(prompt, decision)


def hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()
