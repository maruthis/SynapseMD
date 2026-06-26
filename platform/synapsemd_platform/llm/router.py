from dataclasses import dataclass
from enum import Enum


class TaskComplexity(str, Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    CRITICAL = "critical"


class DataSensitivity(str, Enum):
    ANONYMIZED = "anonymized"
    PSEUDONYMIZED = "pseudonymized"


@dataclass
class RoutingDecision:
    model: str
    provider: str
    max_tokens: int
    temperature: float
    require_human_review: bool
    fallback_model: str


CRITICAL_COMMANDS = {"consult", "specialist", "mental-health", "psych-assess"}
COMPLEX_COMMANDS = {"report", "ai", "health-trend-analyzer", "interaction", "goal"}
SIMPLE_COMMANDS = {"profile", "query", "get-profile"}


class HealthLLMRouter:
    ROUTING_TABLE: dict[tuple[str, str], RoutingDecision] = {
        ("simple", "anonymized"): RoutingDecision("claude-haiku-4-5", "anthropic", 1024, 0.1, False, "gpt-4o-mini"),
        ("moderate", "anonymized"): RoutingDecision("claude-sonnet-4-6", "anthropic", 4096, 0.2, False, "gpt-4o"),
        ("complex", "anonymized"): RoutingDecision("claude-opus-4-8", "anthropic", 8192, 0.3, False, "gpt-4o"),
        ("critical", "anonymized"): RoutingDecision("claude-opus-4-8", "anthropic", 8192, 0.1, True, "med-palm-2"),
        ("moderate", "pseudonymized"): RoutingDecision("med-palm-2", "google-health", 4096, 0.2, False, "meditron-70b"),
        ("complex", "pseudonymized"): RoutingDecision("med-palm-2", "google-health", 8192, 0.1, True, "meditron-70b"),
    }

    def assess_complexity(self, command: str, context_size: int) -> TaskComplexity:
        if command in CRITICAL_COMMANDS:
            return TaskComplexity.CRITICAL
        if command in COMPLEX_COMMANDS or context_size > 10_000:
            return TaskComplexity.COMPLEX
        if command in SIMPLE_COMMANDS and context_size < 2_000:
            return TaskComplexity.SIMPLE
        return TaskComplexity.MODERATE

    def route(
        self,
        command: str,
        data_sensitivity: DataSensitivity,
        context_size: int,
    ) -> RoutingDecision:
        complexity = self.assess_complexity(command, context_size)
        key = (complexity.value, data_sensitivity.value)
        return self.ROUTING_TABLE.get(
            key,
            RoutingDecision("claude-sonnet-4-6", "anthropic", 4096, 0.2, True, "gpt-4o"),
        )
