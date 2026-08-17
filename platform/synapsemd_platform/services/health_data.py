"""HealthDataService — command/MCP/AI facade over JSON or Postgres adapters."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from synapsemd_platform.adapters.base import HealthStoreAdapter
from synapsemd_platform.adapters.dual import DualHealthAdapter
from synapsemd_platform.adapters.legacy_json import LegacyJsonAdapter
from synapsemd_platform.adapters.postgres import PostgresHealthAdapter
from synapsemd_platform.core.config import get_settings

HEALTH_COMMANDS = frozenset({"profile", "allergy", "gout"})


class HealthDataService:
    def __init__(self, adapter: HealthStoreAdapter) -> None:
        self.adapter = adapter

    async def execute(
        self,
        command: str,
        payload: dict[str, Any],
        tenant_id: UUID,
        user_id: UUID,
    ) -> dict[str, Any]:
        if command == "profile":
            return await self._profile(payload, tenant_id, user_id)
        if command == "allergy":
            return await self._allergy(payload, tenant_id, user_id)
        if command == "gout":
            return await self._gout(payload, tenant_id, user_id)
        raise ValueError(f"Unsupported health command: {command}")

    async def _profile(
        self, payload: dict[str, Any], tenant_id: UUID, user_id: UUID
    ) -> dict[str, Any]:
        action = payload.get("action") or "get"
        if action in {"get", "view", "list"}:
            profile = await self.adapter.get_profile(tenant_id, user_id)
            return {"action": "get", "profile": profile or {}}
        if action in {"upsert", "add", "update", "set"}:
            profile = payload.get("profile")
            if profile is None and payload.get("basic_info"):
                profile = {"basic_info": payload["basic_info"]}
            if not isinstance(profile, dict):
                profile = {k: v for k, v in payload.items() if k != "action"}
            stored = await self.adapter.upsert_profile(tenant_id, user_id, profile)
            return {"action": "upsert", "profile": stored}
        raise ValueError(f"Unknown profile action: {action}")

    async def _allergy(
        self, payload: dict[str, Any], tenant_id: UUID, user_id: UUID
    ) -> dict[str, Any]:
        action = payload.get("action") or "list"
        if action == "list":
            rows = await self.adapter.list_allergies(
                tenant_id, user_id, status=payload.get("status")
            )
            return {"action": "list", "allergies": rows, "count": len(rows)}
        if action == "add":
            record = payload.get("record") or _allergy_from_payload(payload)
            stored = await self.adapter.add_allergy(tenant_id, user_id, record)
            return {"action": "add", "allergy": stored}
        if action == "update":
            record_id = str(payload.get("id") or "")
            if not record_id:
                raise ValueError("Allergy update requires id")
            patch = payload.get("record") or {
                k: v for k, v in payload.items() if k not in {"action", "id"}
            }
            stored = await self.adapter.update_allergy(tenant_id, user_id, record_id, patch)
            if stored is None:
                raise ValueError("Allergy not found")
            return {"action": "update", "allergy": stored}
        if action == "delete":
            record_id = str(payload.get("id") or "")
            if not record_id:
                raise ValueError("Allergy delete requires id")
            deleted = await self.adapter.delete_allergy(tenant_id, user_id, record_id)
            if not deleted:
                raise ValueError("Allergy not found")
            return {"action": "delete", "id": record_id}
        raise ValueError(f"Unknown allergy action: {action}")

    async def _gout(
        self, payload: dict[str, Any], tenant_id: UUID, user_id: UUID
    ) -> dict[str, Any]:
        action = payload.get("action") or "list"
        if action in {"list", "status"}:
            rows = await self.adapter.list_gout_flares(
                tenant_id, user_id, status=payload.get("status")
            )
            return {"action": "list", "flares": rows, "count": len(rows)}
        if action == "add":
            record = payload.get("record") or _gout_from_payload(payload)
            stored = await self.adapter.add_gout_flare(tenant_id, user_id, record)
            return {"action": "add", "flare": stored}
        if action == "update":
            record_id = str(payload.get("id") or "")
            if not record_id:
                raise ValueError("Gout update requires id")
            patch = payload.get("record") or {
                k: v for k, v in payload.items() if k not in {"action", "id"}
            }
            stored = await self.adapter.update_gout_flare(
                tenant_id, user_id, record_id, patch
            )
            if stored is None:
                raise ValueError("Gout flare not found")
            return {"action": "update", "flare": stored}
        if action == "delete":
            record_id = str(payload.get("id") or "")
            if not record_id:
                raise ValueError("Gout delete requires id")
            deleted = await self.adapter.delete_gout_flare(tenant_id, user_id, record_id)
            if not deleted:
                raise ValueError("Gout flare not found")
            return {"action": "delete", "id": record_id}
        raise ValueError(f"Unknown gout action: {action}")


def _allergy_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    name = payload.get("allergen") or payload.get("allergen_name") or "unknown"
    allergen_type = payload.get("type") or payload.get("allergen_type") or "other"
    severity = payload.get("severity") or "unknown"
    return {
        "id": payload.get("id"),
        "allergen": {"name": name, "type": allergen_type},
        "severity": {"level": severity} if not isinstance(severity, dict) else severity,
        "current_status": {"status": payload.get("status") or "active"},
        "notes": payload.get("notes") or "",
    }


def _gout_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": payload.get("id"),
        "onset": payload.get("onset"),
        "joint": payload.get("joint"),
        "side": payload.get("side"),
        "severity": payload.get("severity") or "unknown",
        "triggers": payload.get("triggers") or [],
        "uric_acid_mg_dl": payload.get("uric_acid_mg_dl"),
        "status": payload.get("status") or "active",
        "notes": payload.get("notes") or "",
        "recorded_at": payload.get("recorded_at"),
    }


def build_health_adapter() -> HealthStoreAdapter:
    settings = get_settings()
    mode = (settings.health_store or "json").lower()
    json_adapter = LegacyJsonAdapter(settings.legacy_data_root)
    if mode == "json":
        return json_adapter
    postgres = PostgresHealthAdapter()
    if mode == "postgres":
        return postgres
    if mode == "dual":
        return DualHealthAdapter(postgres, json_adapter)
    raise ValueError(f"Unknown HEALTH_STORE: {settings.health_store}")


def get_health_data_service() -> HealthDataService:
    return HealthDataService(build_health_adapter())
