"""Release negative tests: planted PHI must not appear in application logs (C-3)."""

import logging

from synapsemd_platform.observability.log_filter import install_phi_log_filter

PLANTED_PHI = [
    "john.doe@example.com",
    "555-123-4567",
    "123-45-6789",
    "Dr. Jane Smith",
    "MRN:ABC12345",
    "126 mg/dL",
]


def test_planted_phi_does_not_appear_in_captured_logs(caplog) -> None:
    logger = logging.getLogger("synapsemd.release.phi")
    install_phi_log_filter(logger)
    message = (
        "Patient Dr. Jane Smith MRN:ABC12345 glucose 126 mg/dL "
        "email john.doe@example.com phone 555-123-4567 SSN 123-45-6789"
    )
    with caplog.at_level(logging.INFO, logger="synapsemd.release.phi"):
        logger.info(message)
    captured = caplog.text
    for sample in PLANTED_PHI:
        assert sample not in captured, f"PHI leaked in logs: {sample}"
    assert "[REDACTED]" in captured
