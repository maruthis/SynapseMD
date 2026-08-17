"""FHIR JSONB projection from domain JSON (A-6)."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

TENANT_TAG_SYSTEM = "https://synapsemd.com/tenant"


def _tenant_meta(tenant_id: str) -> dict[str, Any]:
    return {"tag": [{"system": TENANT_TAG_SYSTEM, "code": str(tenant_id)}]}


def _allergen_text(item: dict[str, Any]) -> str:
    allergen = item.get("allergen")
    if isinstance(allergen, dict):
        return str(allergen.get("name") or "unknown")
    if allergen:
        return str(allergen)
    return str(item.get("name") or item.get("allergen_name") or "unknown")


def _severity_text(item: dict[str, Any]) -> str:
    severity = item.get("severity")
    if isinstance(severity, dict):
        return str(severity.get("level") or "low")
    return str(severity or "low")


def profile_to_patient(profile: dict[str, Any], patient_id: str, tenant_id: str) -> dict[str, Any]:
    basic = profile.get("basic_info", {})
    return {
        "resourceType": "Patient",
        "id": patient_id,
        "meta": _tenant_meta(tenant_id),
        "gender": basic.get("gender") or "unknown",
        "birthDate": basic.get("birth_date"),
    }


def allergy_to_fhir(
    item: dict[str, Any],
    *,
    patient_ref: str,
    tenant_id: str,
    resource_id: str | None = None,
) -> dict[str, Any]:
    return {
        "resourceType": "AllergyIntolerance",
        "id": resource_id or item.get("id") or str(uuid4()),
        "meta": _tenant_meta(tenant_id),
        "patient": {"reference": patient_ref},
        "code": {"text": _allergen_text(item)},
        "criticality": _severity_text(item),
    }


def allergies_to_fhir(
    allergies_doc: dict[str, Any],
    patient_ref: str,
    tenant_id: str = "default",
) -> list[dict[str, Any]]:
    return [
        allergy_to_fhir(item, patient_ref=patient_ref, tenant_id=tenant_id)
        for item in allergies_doc.get("allergies", [])
    ]


def gout_flare_to_observation(
    flare: dict[str, Any],
    *,
    patient_ref: str,
    tenant_id: str,
    resource_id: str | None = None,
) -> dict[str, Any]:
    uric = flare.get("uric_acid_mg_dl")
    site = " ".join(part for part in (flare.get("side"), flare.get("joint")) if part).strip()
    resource: dict[str, Any] = {
        "resourceType": "Observation",
        "id": resource_id or flare.get("id") or str(uuid4()),
        "meta": _tenant_meta(tenant_id),
        "status": "final" if flare.get("status") == "resolved" else "preliminary",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "3084-1",
                    "display": "Urate",
                }
            ],
            "text": "Gout flare",
        },
        "subject": {"reference": patient_ref},
        "bodySite": {"text": site or "unspecified"},
    }
    if uric not in (None, ""):
        resource["valueQuantity"] = {"value": uric, "unit": "mg/dL"}
    return resource


def observation_from_tracker(
    tracker: dict[str, Any],
    *,
    patient_ref: str,
    loinc_code: str,
    display: str,
    tenant_id: str = "default",
) -> dict[str, Any]:
    return {
        "resourceType": "Observation",
        "id": str(uuid4()),
        "meta": _tenant_meta(tenant_id),
        "status": "final",
        "code": {
            "coding": [{"system": "http://loinc.org", "code": loinc_code, "display": display}],
        },
        "subject": {"reference": patient_ref},
        "valueQuantity": tracker.get("value"),
    }
