"""Persist AI interaction history to the database."""

from __future__ import annotations

import hashlib
import json
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.models.audit import AIInteraction


def _hash_payload(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(body.encode()).hexdigest()


async def record_ai_interaction(
    session: AsyncSession,
    *,
    tenant_id: UUID,
    user_id: UUID,
    command: str,
    model_used: str,
    result: dict[str, Any],
    safety_flags: dict[str, Any] | None = None,
) -> AIInteraction:
    interaction = AIInteraction(
        tenant_id=tenant_id,
        user_id=user_id,
        command=command,
        model_used=model_used,
        prompt_hash=_hash_payload({"tenant_id": str(tenant_id), "user_id": str(user_id), "command": command}),
        response_hash=_hash_payload(result),
        reasoning_trace={"result_summary": _summarize_result(result)},
        safety_flags=safety_flags or {},
    )
    session.add(interaction)
    await session.commit()
    await session.refresh(interaction)
    return interaction


def _summarize_result(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("error"):
        return {"error": True, "message": result.get("message")}
    if "risk_type" in result:
        return {
            "risk_type": result.get("risk_type"),
            "risk_level": result.get("risk_level"),
            "probability": result.get("probability"),
        }
    if isinstance(result, dict) and all(isinstance(v, dict) for v in result.values()):
        return {
            key: {
                "risk_level": value.get("risk_level"),
                "probability": value.get("probability"),
                "error": value.get("error"),
            }
            for key, value in result.items()
        }
    return {"keys": list(result.keys())}
