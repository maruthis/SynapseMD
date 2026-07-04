"""Tenant-scoped health data loading for AI modules."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import UUID

from synapsemd_platform.fhir.migration import DataAccessLayer

TENANT_TAG_SYSTEM = "https://synapsemd.com/tenant"


class TenantIsolationError(PermissionError):
    pass


@dataclass
class HealthDataContext:
    tenant_id: UUID
    user_id: UUID
    user_profile: dict[str, Any]
    nutrition_data: dict[str, Any] | None
    sleep_data: dict[str, Any] | None
    fhir_resources: list[dict[str, Any]]
    data_sources: list[str]


class TenantHealthDataAdapter:
    """Loads health data scoped to {tenant_id, user_id} from FHIR and optional legacy JSON."""

    def __init__(
        self,
        dal: DataAccessLayer,
        *,
        legacy_data_root: str | Path = "./data",
    ) -> None:
        self.dal = dal
        self.legacy_data_root = Path(legacy_data_root)

    async def load(self, tenant_id: UUID, user_id: UUID) -> HealthDataContext:
        resources = await self.dal.get_patient_resources(tenant_id, user_id)
        self._assert_tenant_scope(resources, tenant_id)

        legacy_dir = self._legacy_user_dir(tenant_id, user_id)
        data_sources: list[str] = []

        profile = self._profile_from_fhir(resources)
        if profile:
            data_sources.append("fhir:Patient")
        else:
            profile = self._load_legacy_json(legacy_dir / "profile.json")
            if profile:
                data_sources.append("legacy:profile.json")

        nutrition_data = self._load_legacy_json(legacy_dir / "nutrition-tracker.json")
        if nutrition_data:
            data_sources.append("legacy:nutrition-tracker.json")

        sleep_data = self._load_legacy_json(legacy_dir / "sleep-tracker.json")
        if sleep_data:
            data_sources.append("legacy:sleep-tracker.json")

        if not profile:
            profile = {}

        return HealthDataContext(
            tenant_id=tenant_id,
            user_id=user_id,
            user_profile=profile,
            nutrition_data=nutrition_data,
            sleep_data=sleep_data,
            fhir_resources=resources,
            data_sources=data_sources,
        )

    def _legacy_user_dir(self, tenant_id: UUID, user_id: UUID) -> Path:
        tenant_user = self.legacy_data_root / str(tenant_id) / str(user_id)
        if tenant_user.exists():
            return tenant_user
        return self.legacy_data_root

    @staticmethod
    def _load_legacy_json(path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _profile_from_fhir(resources: list[dict[str, Any]]) -> dict[str, Any] | None:
        patient = next((r for r in resources if r.get("resourceType") == "Patient"), None)
        if not patient:
            return None

        profile: dict[str, Any] = {
            "basic_info": {
                "gender": patient.get("gender"),
                "birth_date": patient.get("birthDate"),
            },
            "calculated": {},
            "lifestyle": {},
            "family_history": {},
            "medical_history": {},
            "vitals": {"blood_pressure": []},
            "lab_results": {},
        }

        for resource in resources:
            if resource.get("resourceType") != "Observation":
                continue
            code = resource.get("code", {}).get("coding", [{}])[0].get("code")
            value = resource.get("valueQuantity")
            if not code or not value:
                continue
            if code == "8480-6":
                profile["vitals"]["blood_pressure"].append(
                    {"systolic": value.get("value"), "diastolic": None}
                )
            elif code == "2339-0":
                profile["lab_results"]["fasting_glucose"] = [{"value": value.get("value")}]

        return profile

    @staticmethod
    def _assert_tenant_scope(resources: list[dict[str, Any]], tenant_id: UUID) -> None:
        for resource in resources:
            tags = resource.get("meta", {}).get("tag", [])
            for tag in tags:
                if tag.get("system") != TENANT_TAG_SYSTEM:
                    continue
                if tag.get("code") != str(tenant_id):
                    raise TenantIsolationError(
                        f"FHIR resource tenant mismatch: expected {tenant_id}, "
                        f"found {tag.get('code')}"
                    )
