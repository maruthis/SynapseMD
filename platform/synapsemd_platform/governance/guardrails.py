from dataclasses import dataclass, field
import hashlib
import re
from typing import Any


@dataclass
class Citation:
    source: str
    url: str
    evidence_level: str = "B"


@dataclass
class ReasoningSummary:
    interaction_id: str
    command: str
    data_sources_read: list[str] = field(default_factory=list)
    rag_sources_retrieved: list[Citation] = field(default_factory=list)
    assumptions_made: list[str] = field(default_factory=list)
    alternatives_considered: list[str] = field(default_factory=list)
    conclusion: str = ""
    confidence_level: float = 0.0
    uncertainty_factors: list[str] = field(default_factory=list)
    safety_checks: list[dict[str, Any]] = field(default_factory=list)
    human_review_required: bool = False
    model_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "interaction_id": self.interaction_id,
            "command": self.command,
            "data_sources_read": self.data_sources_read,
            "rag_sources_retrieved": [c.__dict__ for c in self.rag_sources_retrieved],
            "assumptions_made": self.assumptions_made,
            "alternatives_considered": self.alternatives_considered,
            "conclusion": self.conclusion,
            "confidence_level": self.confidence_level,
            "uncertainty_factors": self.uncertainty_factors,
            "safety_checks": self.safety_checks,
            "human_review_required": self.human_review_required,
            "model_id": self.model_id,
        }


@dataclass
class GuardrailResult:
    blocked: bool = False
    reason: str = ""
    requires_disclaimer: bool = False
    disclaimer: str = ""
    human_review_queued: bool = False
    safe_fallback: str = ""


class MedicalGuardrails:
    HARD_BLOCKS = [
        r"prescribe|diagnose|you have|you are suffering",
        r"stop taking|discontinue your medication",
        r"guarantee|cure|100%",
    ]
    SOFT_FLAGS = [r"recommend|suggest|should", r"study shows|research found"]

    def validate(self, response: str, command: str, reasoning: ReasoningSummary) -> GuardrailResult:
        for pattern in self.HARD_BLOCKS:
            if re.search(pattern, response, re.IGNORECASE):
                return GuardrailResult(
                    blocked=True,
                    reason=f"Prohibited pattern: {pattern}",
                    safe_fallback=self._safe_fallback(command),
                )

        if reasoning.confidence_level < 0.7:
            return GuardrailResult(
                blocked=False,
                requires_disclaimer=True,
                disclaimer="Limited confidence. Please consult a healthcare provider.",
                human_review_queued=True,
            )

        if re.search(r"study|guideline|evidence", response, re.IGNORECASE):
            if not reasoning.rag_sources_retrieved:
                return GuardrailResult(
                    blocked=False,
                    requires_disclaimer=True,
                    disclaimer="Clinical claims require verification with your healthcare provider.",
                )

        return GuardrailResult(blocked=False)

    def _safe_fallback(self, command: str) -> str:
        return (
            f"The {command} request could not be completed automatically. "
            "Please consult a qualified healthcare professional."
        )


HUMAN_REVIEW_COMMANDS = {"consult", "specialist", "mental-health"}
HUMAN_REVIEW_SEVERITIES = {"D", "X"}


def requires_human_review(command: str, confidence: float, interaction_severity: str | None = None) -> bool:
    if command in HUMAN_REVIEW_COMMANDS:
        return True
    if confidence < 0.7:
        return True
    if interaction_severity in HUMAN_REVIEW_SEVERITIES:
        return True
    return False
