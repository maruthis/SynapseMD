"""Golden prompt regression suite for LLM routing and guardrails."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from synapsemd_platform.governance.guardrails import MedicalGuardrails, ReasoningSummary
from synapsemd_platform.llm.router import HealthLLMRouter

GOLDEN_FILE = Path(__file__).parent / "golden_prompts.json"


def _load_cases() -> list[dict]:
    return json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))["cases"]


@pytest.fixture
def golden_cases() -> list[dict]:
    return _load_cases()


def test_golden_prompt_count(golden_cases: list[dict]) -> None:
    assert len(golden_cases) >= 5


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["name"])
def test_golden_guardrail_expectations(case: dict) -> None:
    guardrails = MedicalGuardrails()
    reasoning = ReasoningSummary(
        interaction_id="eval-1",
        command=case["command"],
        confidence_level=case.get("confidence", 0.85),
        rag_sources_retrieved=[],
    )
    result = guardrails.validate(case["response"], case["command"], reasoning)
    if case["expect"] == "block":
        assert result.blocked is True
    elif case["expect"] == "disclaimer":
        assert result.requires_disclaimer is True
    else:
        assert result.blocked is False


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["name"])
def test_golden_router_complexity(case: dict) -> None:
    router = HealthLLMRouter()
    complexity = router.assess_complexity(case["command"], len(case["response"]))
    expected = case.get("complexity")
    if expected:
        assert complexity.value == expected
