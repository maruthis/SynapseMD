from synapsemd_platform.anonymization.engine import AnonymizationEngine
from synapsemd_platform.governance.guardrails import MedicalGuardrails, ReasoningSummary, requires_human_review
from synapsemd_platform.llm.router import DataSensitivity, HealthLLMRouter, TaskComplexity


def test_anonymization_strips_email():
    engine = AnonymizationEngine()
    result = engine.anonymize_for_llm("Contact patient at john.doe@hospital.com", "user-1")
    assert "john.doe@hospital.com" not in result.anonymized_text
    assert result.phi_detected is True


def test_router_critical_command():
    router = HealthLLMRouter()
    decision = router.route("consult", DataSensitivity.ANONYMIZED, 5000)
    assert decision.require_human_review is True
    assert router.assess_complexity("consult", 5000) == TaskComplexity.CRITICAL


def test_guardrail_blocks_diagnosis():
    guardrails = MedicalGuardrails()
    reasoning = ReasoningSummary(interaction_id="x", command="consult", confidence_level=0.9)
    result = guardrails.validate("You have diabetes and should stop taking medication.", "consult", reasoning)
    assert result.blocked is True


def test_human_review_triggers():
    assert requires_human_review("consult", 0.9) is True
    assert requires_human_review("goal", 0.5) is True
    assert requires_human_review("goal", 0.9) is False
