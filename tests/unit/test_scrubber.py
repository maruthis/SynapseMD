from synapsemd_platform.anonymization.scrubber import scrub_audit_payload, scrub_phi_from_text


def test_scrub_audit_preserves_numeric_fields() -> None:
    scrubbed = scrub_audit_payload(
        {
            "event_type": "test",
            "tenant_id": "t1",
            "user_id": "u1",
            "resource": {"count": 3},
            "ai": {"prompt_hash": "abc", "latency_ms": 120},
            "outcome": "success",
        }
    )
    assert scrubbed["resource"]["count"] == 3
    assert scrubbed["ai"]["latency_ms"] == 120


def test_scrub_audit_passes_through_other_fields() -> None:
    scrubbed = scrub_audit_payload(
        {
            "event_type": "test",
            "tenant_id": "t1",
            "outcome": "success",
            "count": 5,
        }
    )
    assert scrubbed["count"] == 5
