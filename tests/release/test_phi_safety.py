from synapsemd_platform.anonymization.engine import AnonymizationEngine


def test_phi_not_present_in_anonymized_output() -> None:
    engine = AnonymizationEngine()
    text = "Contact john.doe@example.com or call 555-123-4567"
    result = engine.anonymize_for_llm(text, "user-1")
    assert "john.doe@example.com" not in result.anonymized_text
    assert "555-123-4567" not in result.anonymized_text


def test_validate_no_phi_detects_email() -> None:
    engine = AnonymizationEngine()
    assert engine.validate_no_phi("email me at test@example.com") is False
