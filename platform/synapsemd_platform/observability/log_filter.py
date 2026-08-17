"""PHI-free log redaction for application logs (C-3)."""

from __future__ import annotations

import logging
import re

from synapsemd_platform.anonymization.engine import (
    DATE_PATTERN,
    EMAIL_PATTERN,
    NAME_PATTERN,
    PHONE_PATTERN,
    SSN_PATTERN,
)

MRN_PATTERN = re.compile(r"\b(?:MRN|mrn|medical[\s_-]?record)[:\s#]*[A-Z0-9-]{4,}\b")
LAB_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:mg/dL|mmol/L|mmHg|IU/L|uIU/mL|ng/mL|g/dL|mEq/L)\b",
    re.IGNORECASE,
)
# Bare lab-like numbers next to common analyte names
ANALYTE_PATTERN = re.compile(
    r"\b(?:glucose|creatinine|hemoglobin|a1c|uric acid|cholesterol)\s*[:=]?\s*\d+(?:\.\d+)?\b",
    re.IGNORECASE,
)

_PATTERNS: tuple[re.Pattern[str], ...] = (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    SSN_PATTERN,
    NAME_PATTERN,
    MRN_PATTERN,
    LAB_PATTERN,
    ANALYTE_PATTERN,
    DATE_PATTERN,
)


def redact_log_message(message: str) -> str:
    result = message
    for pattern in _PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


class PhiLogFilter(logging.Filter):
    """Deny names, emails, MRN, and lab-like values in log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            record.msg = redact_log_message(str(record.msg))
            if record.args:
                if isinstance(record.args, dict):
                    record.args = {k: _redact_arg(v) for k, v in record.args.items()}
                else:
                    record.args = tuple(_redact_arg(arg) for arg in record.args)
        except Exception:
            record.msg = "[REDACTED]"
            record.args = ()
        return True


def _redact_arg(value: object) -> object:
    if isinstance(value, str):
        return redact_log_message(value)
    return value


def install_phi_log_filter(logger: logging.Logger | None = None) -> PhiLogFilter:
    phi_filter = PhiLogFilter()
    target = logger or logging.getLogger()
    if not any(isinstance(existing, PhiLogFilter) for existing in target.filters):
        target.addFilter(phi_filter)
    return phi_filter
