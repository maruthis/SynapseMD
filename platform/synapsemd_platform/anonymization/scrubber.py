"""PHI scrubbing utilities for logs and audit payloads."""

from __future__ import annotations

import re
from typing import Any

from synapsemd_platform.anonymization.engine import EMAIL_PATTERN, PHONE_PATTERN, SSN_PATTERN

PHI_PATTERNS: list[re.Pattern[str]] = [EMAIL_PATTERN, PHONE_PATTERN, SSN_PATTERN]
HASH_ONLY_AI_KEYS = frozenset({"prompt_hash", "response_hash", "model", "latency_ms", "confidence"})


def scrub_phi_from_text(text: str) -> str:
    result = text
    for pattern in PHI_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def scrub_audit_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Remove raw PHI from audit resource/ai sections; preserve hashes only in ai."""
    scrubbed: dict[str, Any] = {}
    for key, value in payload.items():
        if key == "ai" and isinstance(value, dict):
            scrubbed[key] = {k: v for k, v in value.items() if k in HASH_ONLY_AI_KEYS}
        elif key == "resource" and isinstance(value, dict):
            scrubbed[key] = {
                k: scrub_phi_from_text(v) if isinstance(v, str) else v
                for k, v in value.items()
            }
        elif isinstance(value, str):
            scrubbed[key] = scrub_phi_from_text(value)
        else:
            scrubbed[key] = value
    return scrubbed
