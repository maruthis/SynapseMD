"""Custom health PHI recognizers (D-2): MRN, accession, Indian phone variants."""

from __future__ import annotations

import re

MRN_PATTERN = re.compile(
    r"\b(?:MRN|mrn|medical[\s_-]?record)[:\s#]*[A-Z0-9-]{4,}\b",
)
ACCESSION_PATTERN = re.compile(
    r"\b(?:ACC|accession)[:\s#/-]*[A-Z0-9-]{5,}\b",
    re.IGNORECASE,
)
# +91 98765 43210, 09876543210, 9876543210
INDIAN_PHONE_PATTERN = re.compile(
    r"\b(?:\+91[-\s]?|0)?[6-9]\d{9}\b",
)

CUSTOM_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("MRN", MRN_PATTERN),
    ("ACCESSION", ACCESSION_PATTERN),
    ("IN_PHONE", INDIAN_PHONE_PATTERN),
)


def find_custom_phi(text: str) -> list[tuple[str, str]]:
    """Return (entity_type, matched_text) for custom health identifiers."""
    found: list[tuple[str, str]] = []
    for entity_type, pattern in CUSTOM_PATTERNS:
        for match in pattern.finditer(text):
            found.append((entity_type, match.group()))
    return found


def contains_custom_phi(text: str) -> bool:
    return bool(find_custom_phi(text))


def register_presidio_recognizers(analyzer: object) -> int:
    """Attach PatternRecognizers when Presidio is available. Returns count added."""
    try:
        from presidio_analyzer import Pattern, PatternRecognizer
    except ImportError:
        return 0
    registry = getattr(analyzer, "registry", None)
    if registry is None or not hasattr(registry, "add_recognizer"):
        return 0
    added = 0
    for entity_type, pattern in CUSTOM_PATTERNS:
        recognizer = PatternRecognizer(
            supported_entity=entity_type,
            patterns=[Pattern(name=entity_type.lower(), regex=pattern.pattern, score=0.6)],
        )
        registry.add_recognizer(recognizer)
        added += 1
    return added
