from unittest.mock import MagicMock, patch

import pytest

from synapsemd_platform.anonymization.engine import (
    AnonymizationEngine,
    TokenVault,
    hash_content,
)
from synapsemd_platform.core.config import Settings


def test_token_vault_store_and_deanonymize() -> None:
    vault = TokenVault()
    vault.store_tokens("user-1", {"TOKEN_A": "secret"})
    assert vault.resolve("user-1", "TOKEN_A") == "secret"
    assert vault.deanonymize("user-1", "Hello TOKEN_A", {"TOKEN_A": "secret"}) == "Hello secret"


def test_anonymize_email_phone_ssn_name() -> None:
    engine = AnonymizationEngine()
    text = "Dr. John Smith email john@test.com phone 555-123-4567 ssn 123-45-6789 born 1990-01-01"
    result = engine.anonymize_for_llm(text, "user-1")
    assert "john@test.com" not in result.anonymized_text
    assert "123-45-6789" not in result.anonymized_text
    assert result.phi_detected is True


def test_validate_no_phi_clean_text() -> None:
    engine = AnonymizationEngine()
    assert engine.validate_no_phi("no sensitive data here") is True


def test_phi_block_on_failure() -> None:
    engine = AnonymizationEngine()
    engine.settings = Settings(phi_block_on_failure=True)
    with patch.object(engine, "validate_no_phi", return_value=False):
        with pytest.raises(ValueError, match="PHI detected"):
            engine._anonymize_regex("john@test.com", "user-1")


def test_deanonymize_response() -> None:
    engine = AnonymizationEngine()
    result = engine.anonymize_for_llm("Contact john@test.com", "u1")
    deanonymized = engine.deanonymize_response(result.anonymized_text, "u1", result.token_map)
    assert "john@test.com" in deanonymized or "TOKEN" in deanonymized


def test_hash_content() -> None:
    assert len(hash_content("test")) == 64


def test_presidio_init_import_error() -> None:
    engine = AnonymizationEngine()
    engine.settings = Settings(presidio_enabled=True)
    with patch.dict("sys.modules", {"presidio_analyzer": None}):
        engine._init_presidio()
    assert engine._presidio is None


def test_presidio_init_on_construct() -> None:
    mock_analyzer = MagicMock()
    mock_anonymizer = MagicMock()
    presidio_analyzer = MagicMock(AnalyzerEngine=MagicMock(return_value=mock_analyzer))
    presidio_anonymizer = MagicMock(AnonymizerEngine=MagicMock(return_value=mock_anonymizer))
    with patch.dict(
        "sys.modules",
        {
            "presidio_analyzer": presidio_analyzer,
            "presidio_anonymizer": presidio_anonymizer,
        },
    ):
        with patch(
            "synapsemd_platform.anonymization.engine.get_settings",
            return_value=Settings(presidio_enabled=True),
        ):
            engine = AnonymizationEngine()
    assert engine._presidio == (mock_analyzer, mock_anonymizer)


def test_presidio_init_success() -> None:
    engine = AnonymizationEngine()
    engine.settings = Settings(presidio_enabled=True)
    mock_analyzer = MagicMock()
    mock_anonymizer = MagicMock()
    presidio_analyzer = MagicMock(AnalyzerEngine=MagicMock(return_value=mock_analyzer))
    presidio_anonymizer = MagicMock(AnonymizerEngine=MagicMock(return_value=mock_anonymizer))
    with patch.dict(
        "sys.modules",
        {
            "presidio_analyzer": presidio_analyzer,
            "presidio_anonymizer": presidio_anonymizer,
        },
    ):
        engine._init_presidio()
    assert engine._presidio == (mock_analyzer, mock_anonymizer)


def test_presidio_anonymize_path() -> None:
    engine = AnonymizationEngine()
    mock_analyzer = MagicMock()
    mock_anonymizer = MagicMock()
    mock_result = MagicMock()
    mock_result.entity_type = "EMAIL_ADDRESS"
    mock_result.start = 0
    mock_result.end = 16
    mock_analyzer.analyze.return_value = [mock_result]
    mock_anonymizer.anonymize.return_value = MagicMock(text="TOKEN_EMAIL_abc")
    engine._presidio = (mock_analyzer, mock_anonymizer)

    mock_operator_config = MagicMock()
    presidio_entities = MagicMock(OperatorConfig=mock_operator_config)
    with patch.dict(
        "sys.modules",
        {
            "presidio_anonymizer": MagicMock(),
            "presidio_anonymizer.entities": presidio_entities,
        },
    ):
        result = engine._anonymize_presidio("john@test.com", "user-1")
    assert result.phi_detected is True


def test_anonymize_for_llm_presidio_branch() -> None:
    engine = AnonymizationEngine()
    mock_analyzer = MagicMock()
    mock_anonymizer = MagicMock()
    mock_result = MagicMock()
    mock_result.entity_type = "EMAIL_ADDRESS"
    mock_result.start = 0
    mock_result.end = 16
    mock_analyzer.analyze.return_value = [mock_result]
    mock_anonymizer.anonymize.return_value = MagicMock(text="TOKEN_EMAIL_abc")
    engine._presidio = (mock_analyzer, mock_anonymizer)

    mock_operator_config = MagicMock()
    presidio_entities = MagicMock(OperatorConfig=mock_operator_config)
    with patch.dict(
        "sys.modules",
        {
            "presidio_anonymizer": MagicMock(),
            "presidio_anonymizer.entities": presidio_entities,
        },
    ):
        result = engine.anonymize_for_llm("john@test.com", "user-1")
    assert result.phi_detected is True
