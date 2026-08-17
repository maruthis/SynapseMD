"""In-process specialist worker pool for platform MDT (E-8)."""

from __future__ import annotations

import asyncio
from pathlib import Path

from synapsemd_platform.llm.providers import LLMOrchestrator
from synapsemd_platform.llm.router import RoutingDecision

DEFAULT_CONSULT_SPECIALTIES = ("cardiology", "endocrinology", "rheumatology")


def specialist_root() -> Path:
    repo = Path(__file__).resolve().parents[3]
    path = repo / "specialists"
    if path.is_dir():
        return path
    return Path(__file__).resolve().parent / "prompts"


def load_specialist_prompt(specialty: str) -> str:
    root = specialist_root()
    name = specialty.strip().lower().replace(" ", "-")
    path = root / f"{name}.md"
    if path.is_file():
        return path.read_text(encoding="utf-8")[:4000]
    return f"You are a {specialty} specialist. Review the anonymized case. Do not prescribe."


def _specialties_for(command: str, payload: dict) -> tuple[str, ...]:
    raw = payload.get("specialties") or payload.get("specialty")
    if isinstance(raw, str) and raw.strip():
        return (raw.strip().lower(),)
    if isinstance(raw, list) and raw:
        return tuple(str(item).strip().lower() for item in raw if str(item).strip())
    if command == "specialist":
        return ("general",)
    return DEFAULT_CONSULT_SPECIALTIES


async def run_one(
    specialty: str,
    anonymized_text: str,
    llm: LLMOrchestrator,
    decision: RoutingDecision,
) -> dict[str, str]:
    prompt = (
        f"{load_specialist_prompt(specialty)}\n\n"
        f"Anonymized case:\n{anonymized_text}\n\n"
        "Write a short specialty opinion. Do not diagnose or prescribe."
    )
    response = await llm.execute(prompt, decision)
    return {"specialty": specialty, "opinion": response.content}


def merge_sections(sections: list[dict[str, str]]) -> str:
    coordinator = load_specialist_prompt("consultation-coordinator")
    parts = ["# Multidisciplinary Team (MDT) Consultation Report", "", "## Specialist sections"]
    for section in sections:
        parts.append(f"### {section['specialty']}")
        parts.append(section["opinion"])
        parts.append("")
    parts.append("## Coordinator notes")
    parts.append(coordinator.split("## Workflow", 1)[0].strip()[:500])
    return "\n".join(parts)


async def run_mdt(
    *,
    command: str,
    anonymized_text: str,
    payload: dict,
    llm: LLMOrchestrator,
    decision: RoutingDecision,
) -> dict:
    specialties = _specialties_for(command, payload)
    sections = list(
        await asyncio.gather(
            *[run_one(name, anonymized_text, llm, decision) for name in specialties]
        )
    )
    merged = merge_sections(sections)
    return {
        "specialties": list(specialties),
        "sections": sections,
        "merged": merged,
    }
