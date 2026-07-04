"""Release gate tests for PHI safety."""

from synapsemd_platform.anonymization.engine import AnonymizationEngine
from synapsemd_platform.anonymization.scrubber import scrub_audit_payload, scrub_phi_from_text
from synapsemd_platform.audit.events import AuditEventPayload, audit_producer
from synapsemd_platform.core.config import get_settings


GOLDEN_PHI_STRINGS = [
    "Contact john.doe@example.com for results",
    "Call 555-123-4567 after hours",
    "SSN 123-45-6789 on file",
    "Dr. Jane Smith reviewed the chart",
]


def test_phi_not_present_in_anonymized_output() -> None:
    engine = AnonymizationEngine()
    text = "Contact john.doe@example.com or call 555-123-4567"
    result = engine.anonymize_for_llm(text, "user-1")
    assert "john.doe@example.com" not in result.anonymized_text
    assert "555-123-4567" not in result.anonymized_text


def test_validate_no_phi_detects_email() -> None:
    engine = AnonymizationEngine()
    assert engine.validate_no_phi("email me at test@example.com") is False


def test_phi_block_on_failure_default_enabled() -> None:
    settings = get_settings()
    assert settings.phi_block_on_failure is True


def test_golden_phi_strings_scrubbed() -> None:
    for sample in GOLDEN_PHI_STRINGS:
        scrubbed = scrub_phi_from_text(sample)
        assert "@" not in scrubbed or "[REDACTED]" in scrubbed
        assert "555-123-4567" not in scrubbed
        assert "123-45-6789" not in scrubbed


def test_audit_payload_stores_hashes_only_in_ai_section() -> None:
    scrubbed = scrub_audit_payload(
        {
            "event_type": "ai.command.executed",
            "tenant_id": "t1",
            "user_id": "u1",
            "resource": {"command": "goal", "note": "email test@example.com"},
            "ai": {
                "model": "mock",
                "prompt_hash": "abc123",
                "response_hash": "def456",
                "prompt": "raw prompt with PHI",
            },
            "outcome": "success",
        }
    )
    assert "prompt" not in scrubbed["ai"]
    assert scrubbed["ai"]["prompt_hash"] == "abc123"
    assert "test@example.com" not in scrubbed["resource"]["note"]


async def test_audit_emit_scrubs_phi_from_resource() -> None:
    audit_producer._memory_events.clear()
    await audit_producer.emit(
        AuditEventPayload(
            event_type="test.phi.scrub",
            tenant_id="tenant-1",
            user_id="user-1",
            resource={"context": "reach me at leak@example.com"},
            ai={"prompt_hash": "hash1", "response_hash": "hash2", "raw": "secret"},
            outcome="success",
        )
    )
    event = audit_producer.get_events()[-1]
    assert "leak@example.com" not in str(event)
    assert "raw" not in event.get("ai", {})
    assert event["ai"]["prompt_hash"] == "hash1"
