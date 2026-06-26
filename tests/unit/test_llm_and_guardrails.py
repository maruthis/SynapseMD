import pytest

from synapsemd_platform.governance.guardrails import (
    Citation,
    MedicalGuardrails,
    ReasoningSummary,
    requires_human_review,
)
from synapsemd_platform.llm.router import DataSensitivity, HealthLLMRouter, TaskComplexity
from synapsemd_platform.llm.providers import LLMOrchestrator, hash_prompt


def test_router_complexity_levels() -> None:
    router = HealthLLMRouter()
    assert router.assess_complexity("consult", 100) == TaskComplexity.CRITICAL
    assert router.assess_complexity("goal", 100) == TaskComplexity.COMPLEX
    assert router.assess_complexity("profile", 100) == TaskComplexity.SIMPLE
    assert router.assess_complexity("nutrition", 5000) == TaskComplexity.MODERATE
    assert router.assess_complexity("nutrition", 20_000) == TaskComplexity.COMPLEX


def test_router_all_table_entries() -> None:
    router = HealthLLMRouter()
    for key in router.ROUTING_TABLE:
        complexity, sensitivity = key
        decision = router.route("goal", DataSensitivity(sensitivity), 5000)
        assert decision.model


def test_router_default_fallback() -> None:
    router = HealthLLMRouter()
    decision = router.route("profile", DataSensitivity.PSEUDONYMIZED, 100)
    assert decision.require_human_review is True
    assert decision.model == "claude-sonnet-4-6"


@pytest.mark.asyncio
async def test_llm_orchestrator_mock() -> None:
    from synapsemd_platform.llm.router import RoutingDecision

    orchestrator = LLMOrchestrator()
    decision = RoutingDecision("test-model", "mock", 100, 0.1, False, "fallback")
    response = await orchestrator.execute("hello", decision)
    assert "test-model" in response.content


def test_hash_prompt() -> None:
    assert len(hash_prompt("prompt")) == 64


def test_guardrail_hard_block() -> None:
    guardrails = MedicalGuardrails()
    reasoning = ReasoningSummary(interaction_id="x", command="consult", confidence_level=0.9)
    result = guardrails.validate("You have diabetes", "consult", reasoning)
    assert result.blocked is True
    assert "consult" in result.safe_fallback


def test_guardrail_low_confidence() -> None:
    guardrails = MedicalGuardrails()
    reasoning = ReasoningSummary(interaction_id="x", command="goal", confidence_level=0.5)
    result = guardrails.validate("General wellness tips", "goal", reasoning)
    assert result.requires_disclaimer is True
    assert result.human_review_queued is True


def test_guardrail_clinical_claim_without_citation() -> None:
    guardrails = MedicalGuardrails()
    reasoning = ReasoningSummary(interaction_id="x", command="goal", confidence_level=0.9)
    result = guardrails.validate("A study shows benefits", "goal", reasoning)
    assert result.requires_disclaimer is True


def test_guardrail_pass() -> None:
    guardrails = MedicalGuardrails()
    reasoning = ReasoningSummary(
        interaction_id="x",
        command="goal",
        confidence_level=0.9,
        rag_sources_retrieved=[Citation(source="AHA", url="http://example.com")],
    )
    result = guardrails.validate("Healthy habits matter", "goal", reasoning)
    assert result.blocked is False


def test_reasoning_summary_to_dict() -> None:
    summary = ReasoningSummary(
        interaction_id="int-1",
        command="goal",
        conclusion="ok",
        confidence_level=0.8,
        rag_sources_retrieved=[Citation(source="KB", url="http://x.com")],
    )
    data = summary.to_dict()
    assert data["interaction_id"] == "int-1"
    assert len(data["rag_sources_retrieved"]) == 1


def test_requires_human_review_matrix() -> None:
    assert requires_human_review("consult", 0.9) is True
    assert requires_human_review("goal", 0.5) is True
    assert requires_human_review("goal", 0.9, "X") is True
    assert requires_human_review("goal", 0.9) is False
