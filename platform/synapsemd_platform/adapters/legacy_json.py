"""Legacy JSON vault adapter — local IDE/CLI and HEALTH_STORE=json."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class LegacyJsonAdapter:
    def __init__(self, data_root: str | Path = "./data") -> None:
        self.data_root = Path(data_root)

    def _user_dir(self, tenant_id: UUID, user_id: UUID) -> Path:
        path = self.data_root / str(tenant_id) / str(user_id)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.is_file():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_json(self, path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    async def get_profile(self, tenant_id: UUID, user_id: UUID) -> dict[str, Any] | None:
        data = self._read_json(self._user_dir(tenant_id, user_id) / "profile.json")
        return data or None

    async def upsert_profile(
        self, tenant_id: UUID, user_id: UUID, profile: dict[str, Any]
    ) -> dict[str, Any]:
        path = self._user_dir(tenant_id, user_id) / "profile.json"
        existing = self._read_json(path)
        merged = {**existing, **profile}
        merged["last_updated"] = _now_iso()
        self._write_json(path, merged)
        return merged

    async def list_allergies(
        self, tenant_id: UUID, user_id: UUID, *, status: str | None = None
    ) -> list[dict[str, Any]]:
        data = self._read_json(self._user_dir(tenant_id, user_id) / "allergies.json")
        rows = list(data.get("allergies") or [])
        if status:
            rows = [r for r in rows if (r.get("current_status") or {}).get("status") == status]
        return rows

    async def add_allergy(
        self, tenant_id: UUID, user_id: UUID, record: dict[str, Any]
    ) -> dict[str, Any]:
        path = self._user_dir(tenant_id, user_id) / "allergies.json"
        data = self._read_json(path)
        allergies = list(data.get("allergies") or [])
        record.setdefault("id", f"allergy_{uuid4().hex[:16]}")
        record.setdefault("metadata", {})["last_updated"] = _now_iso()
        allergies.append(record)
        data["allergies"] = allergies
        data["statistics"] = _allergy_stats(allergies)
        self._write_json(path, data)
        return record

    async def update_allergy(
        self, tenant_id: UUID, user_id: UUID, record_id: str, patch: dict[str, Any]
    ) -> dict[str, Any] | None:
        path = self._user_dir(tenant_id, user_id) / "allergies.json"
        data = self._read_json(path)
        allergies = list(data.get("allergies") or [])
        for idx, row in enumerate(allergies):
            if row.get("id") == record_id:
                updated = {**row, **patch}
                updated.setdefault("metadata", {})["last_updated"] = _now_iso()
                allergies[idx] = updated
                data["allergies"] = allergies
                data["statistics"] = _allergy_stats(allergies)
                self._write_json(path, data)
                return updated
        return None

    async def delete_allergy(self, tenant_id: UUID, user_id: UUID, record_id: str) -> bool:
        path = self._user_dir(tenant_id, user_id) / "allergies.json"
        data = self._read_json(path)
        allergies = list(data.get("allergies") or [])
        kept = [r for r in allergies if r.get("id") != record_id]
        if len(kept) == len(allergies):
            return False
        data["allergies"] = kept
        data["statistics"] = _allergy_stats(kept)
        self._write_json(path, data)
        return True

    async def list_gout_flares(
        self, tenant_id: UUID, user_id: UUID, *, status: str | None = None
    ) -> list[dict[str, Any]]:
        data = self._read_json(self._user_dir(tenant_id, user_id) / "gout-tracker.json")
        rows = list(data.get("flares") or [])
        if status:
            rows = [r for r in rows if r.get("status") == status]
        return rows

    async def add_gout_flare(
        self, tenant_id: UUID, user_id: UUID, record: dict[str, Any]
    ) -> dict[str, Any]:
        path = self._user_dir(tenant_id, user_id) / "gout-tracker.json"
        data = self._read_json(path)
        flares = list(data.get("flares") or [])
        record.setdefault("id", f"gout-{uuid4().hex[:12]}")
        record["last_updated"] = _now_iso()
        flares.append(record)
        data["flares"] = flares
        data["statistics"] = _gout_stats(flares)
        data.setdefault("metadata", {"schema_version": "1.0", "domain": "gout"})
        self._write_json(path, data)
        return record

    async def update_gout_flare(
        self, tenant_id: UUID, user_id: UUID, record_id: str, patch: dict[str, Any]
    ) -> dict[str, Any] | None:
        path = self._user_dir(tenant_id, user_id) / "gout-tracker.json"
        data = self._read_json(path)
        flares = list(data.get("flares") or [])
        for idx, row in enumerate(flares):
            if row.get("id") == record_id:
                updated = {**row, **patch, "last_updated": _now_iso()}
                flares[idx] = updated
                data["flares"] = flares
                data["statistics"] = _gout_stats(flares)
                self._write_json(path, data)
                return updated
        return None

    async def delete_gout_flare(self, tenant_id: UUID, user_id: UUID, record_id: str) -> bool:
        path = self._user_dir(tenant_id, user_id) / "gout-tracker.json"
        data = self._read_json(path)
        flares = list(data.get("flares") or [])
        kept = [r for r in flares if r.get("id") != record_id]
        if len(kept) == len(flares):
            return False
        data["flares"] = kept
        data["statistics"] = _gout_stats(kept)
        self._write_json(path, data)
        return True


def _allergy_stats(allergies: list[dict[str, Any]]) -> dict[str, Any]:
    def _type(row: dict[str, Any]) -> str:
        return (row.get("allergen") or {}).get("type") or row.get("allergen_type") or "other"

    def _status(row: dict[str, Any]) -> str:
        return (row.get("current_status") or {}).get("status") or row.get("status") or "active"

    def _severity(row: dict[str, Any]) -> str:
        sev = row.get("severity")
        if isinstance(sev, dict):
            return str(sev.get("level") or "")
        return str(sev or "")

    return {
        "total_allergies": len(allergies),
        "active_allergies": sum(1 for r in allergies if _status(r) == "active"),
        "drug_allergies": sum(1 for r in allergies if _type(r) == "drug"),
        "food_allergies": sum(1 for r in allergies if _type(r) == "food"),
        "environmental_allergies": sum(1 for r in allergies if _type(r) == "environmental"),
        "other_allergies": sum(
            1 for r in allergies if _type(r) not in {"drug", "food", "environmental"}
        ),
        "severe_count": sum(1 for r in allergies if _severity(r) == "severe"),
        "last_updated": _now_iso(),
    }


def _gout_stats(flares: list[dict[str, Any]]) -> dict[str, Any]:
    onsets = [str(f.get("onset") or "") for f in flares if f.get("onset")]
    return {
        "total_flares": len(flares),
        "active_flares": sum(1 for f in flares if f.get("status") == "active"),
        "severe_count": sum(1 for f in flares if f.get("severity") == "severe"),
        "last_flare_date": max(onsets) if onsets else None,
        "last_updated": _now_iso(),
    }

