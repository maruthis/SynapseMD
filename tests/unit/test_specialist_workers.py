"""Specialist worker pool (E-8)."""

import pytest

from synapsemd_platform.llm.providers import LLMOrchestrator
from synapsemd_platform.llm.router import HealthLLMRouter, DataSensitivity
from synapsemd_platform.services.command_orchestrator import CommandOrchestrator
from synapsemd_platform.workers.specialist import load_specialist_prompt, merge_sections, run_mdt


def test_load_and_merge_specialist_markdown() -> None:
    prompt = load_specialist_prompt("cardiology")
    assert "Cardiovascular" in prompt or "cardiology" in prompt.lower()
    merged = merge_sections(
        [
            {"specialty": "cardiology", "opinion": "Review lipids."},
            {"specialty": "endocrinology", "opinion": "Review glucose."},
        ]
    )
    assert "### cardiology" in merged
    assert "### endocrinology" in merged
    assert "MDT" in merged


@pytest.mark.asyncio
async def test_run_mdt_returns_sections() -> None:
    decision = HealthLLMRouter().route("consult", DataSensitivity.ANONYMIZED, 100)
    result = await run_mdt(
        command="consult",
        anonymized_text="TOKEN_NAME_1 has TOKEN_DATE_1 labs.",
        payload={"specialties": ["cardiology", "rheumatology"]},
        llm=LLMOrchestrator(),
        decision=decision,
    )
    assert result["specialties"] == ["cardiology", "rheumatology"]
    assert len(result["sections"]) == 2
    assert "### cardiology" in result["merged"]


@pytest.mark.asyncio
async def test_specialist_command_defaults_to_general() -> None:
    decision = HealthLLMRouter().route("specialist", DataSensitivity.ANONYMIZED, 100)
    result = await run_mdt(
        command="specialist",
        anonymized_text="case",
        payload={},
        llm=LLMOrchestrator(),
        decision=decision,
    )
    assert result["specialties"] == ["general"]
    unknown = load_specialist_prompt("not-a-real-specialty")
    assert "not-a-real-specialty" in unknown


@pytest.mark.asyncio
async def test_consult_string_specialty_and_defaults() -> None:
    decision = HealthLLMRouter().route("consult", DataSensitivity.ANONYMIZED, 100)
    named = await run_mdt(
        command="consult",
        anonymized_text="case",
        payload={"specialty": "cardiology"},
        llm=LLMOrchestrator(),
        decision=decision,
    )
    assert named["specialties"] == ["cardiology"]
    defaulted = await run_mdt(
        command="consult",
        anonymized_text="case",
        payload={},
        llm=LLMOrchestrator(),
        decision=decision,
    )
    assert "endocrinology" in defaulted["specialties"]


@pytest.mark.asyncio
async def test_consult_response_includes_merged_sections() -> None:
    orchestrator = CommandOrchestrator()
    result = await orchestrator.execute(
        command="consult",
        context_text="Anonymized case summary for MDT.",
        user_id="user-1",
        tenant_id="tenant-1",
        payload={"specialties": ["cardiology"]},
    )
    assert result["command"] == "consult"
    assert "### cardiology" in result["response"]
    assert "MDT" in result["response"]
