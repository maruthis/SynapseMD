"""FHIR mapping and migration from legacy JSON trackers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from synapsemd_platform.fhir.projection import (
    allergies_to_fhir,
    allergy_to_fhir,
    gout_flare_to_observation,
    observation_from_tracker,
    profile_to_patient,
)

FHIR_MAPPINGS: dict[str, str] = {
    "profile.json": "Patient",
    "allergies.json": "AllergyIntolerance",
    "gout-tracker.json": "Observation",
    "medications": "MedicationRequest",
    "fitness-logs": "Observation",
    "radiation-records.json": "ImagingStudy",
    "surgery-records": "Procedure",
    "discharge-summaries": "Composition",
    "interactions": "ClinicalUseDefinition",
}

__all__ = [
    "FHIR_MAPPINGS",
    "FHIRLocalStore",
    "DataAccessLayer",
    "allergies_to_fhir",
    "allergy_to_fhir",
    "gout_flare_to_observation",
    "migrate_json_directory",
    "observation_from_tracker",
    "profile_to_patient",
]


class FHIRLocalStore:
    """File-based FHIR bundle store for local development."""

    def __init__(self, base_path: str) -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _bundle_path(self, tenant_id: UUID, user_id: UUID) -> Path:
        return self.base_path / str(tenant_id) / f"{user_id}.json"

    async def save_bundle(
        self, tenant_id: UUID, user_id: UUID, resources: list[dict[str, Any]]
    ) -> None:
        path = self._bundle_path(tenant_id, user_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": [{"resource": r} for r in resources],
        }
        path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")

    async def load_bundle(self, tenant_id: UUID, user_id: UUID) -> list[dict[str, Any]]:
        path = self._bundle_path(tenant_id, user_id)
        if not path.exists():
            return []
        bundle = json.loads(path.read_text(encoding="utf-8"))
        return [entry["resource"] for entry in bundle.get("entry", [])]

    async def delete_bundle(self, tenant_id: UUID, user_id: UUID) -> bool:
        path = self._bundle_path(tenant_id, user_id)
        if not path.exists():
            return False
        path.unlink()
        return True


class DataAccessLayer:
    """Abstraction over FHIR storage for commands."""

    def __init__(self, store: FHIRLocalStore) -> None:
        self.store = store

    async def get_patient_resources(self, tenant_id: UUID, user_id: UUID) -> list[dict[str, Any]]:
        return await self.store.load_bundle(tenant_id, user_id)

    async def upsert_resources(
        self, tenant_id: UUID, user_id: UUID, resources: list[dict[str, Any]]
    ) -> None:
        existing = await self.store.load_bundle(tenant_id, user_id)
        by_id = {r.get("id"): r for r in existing}
        for resource in resources:
            by_id[resource.get("id", str(uuid4()))] = resource
        await self.store.save_bundle(tenant_id, user_id, list(by_id.values()))

    async def delete_patient_resources(self, tenant_id: UUID, user_id: UUID) -> bool:
        return await self.store.delete_bundle(tenant_id, user_id)


def migrate_json_directory(source_dir: Path, tenant_id: str, user_id: str) -> list[dict[str, Any]]:
    resources: list[dict[str, Any]] = []
    patient_id = user_id
    patient_ref = f"Patient/{patient_id}"

    profile_path = source_dir / "profile.json"
    if profile_path.exists():
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        resources.append(profile_to_patient(profile, patient_id, tenant_id))

    allergies_path = source_dir / "allergies.json"
    if allergies_path.exists():
        allergies = json.loads(allergies_path.read_text(encoding="utf-8"))
        resources.extend(allergies_to_fhir(allergies, patient_ref, tenant_id))

    gout_path = source_dir / "gout-tracker.json"
    if gout_path.exists():
        gout = json.loads(gout_path.read_text(encoding="utf-8"))
        for flare in gout.get("flares") or []:
            resources.append(
                gout_flare_to_observation(flare, patient_ref=patient_ref, tenant_id=tenant_id)
            )

    return resources


async def migrate_domain_tables(source_dir: Path, tenant_id: UUID, user_id: UUID) -> dict[str, int]:
    """Upsert profile / allergy / gout rows from a JSON vault directory (A-8)."""
    from synapsemd_platform.services.health_data import get_health_data_service

    service = get_health_data_service()
    counts = {"profile": 0, "allergies": 0, "gout_flares": 0}

    profile_path = source_dir / "profile.json"
    if profile_path.exists():
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        await service.execute(
            "profile",
            {"action": "upsert", "profile": profile},
            tenant_id,
            user_id,
        )
        counts["profile"] = 1

    allergies_path = source_dir / "allergies.json"
    if allergies_path.exists():
        doc = json.loads(allergies_path.read_text(encoding="utf-8"))
        for item in doc.get("allergies") or []:
            await service.execute(
                "allergy",
                {"action": "add", "record": item},
                tenant_id,
                user_id,
            )
            counts["allergies"] += 1

    gout_path = source_dir / "gout-tracker.json"
    if gout_path.exists():
        doc = json.loads(gout_path.read_text(encoding="utf-8"))
        for flare in doc.get("flares") or []:
            await service.execute(
                "gout",
                {"action": "add", "record": flare},
                tenant_id,
                user_id,
            )
            counts["gout_flares"] += 1

    return counts
