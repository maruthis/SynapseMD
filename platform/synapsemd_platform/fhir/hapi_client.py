"""HAPI FHIR server client for staging/production clinical storage."""

from typing import Any
from uuid import UUID

import httpx

from synapsemd_platform.core.config import get_settings


class HapiFhirClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def search_resources(
        self,
        resource_type: str,
        *,
        tenant_id: UUID,
        user_id: UUID,
        count: int = 20,
    ) -> list[dict[str, Any]]:
        params = {
            "_count": count,
            "patient": str(user_id),
            "_tag": f"https://synapsemd.com/tenant|{tenant_id}",
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/{resource_type}",
                params=params,
            )
            response.raise_for_status()
            bundle = response.json()
        return [entry["resource"] for entry in bundle.get("entry", [])]

    async def upsert_bundle(self, bundle: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{self.base_url}", json=bundle)
            response.raise_for_status()
            return response.json()


def get_fhir_client() -> HapiFhirClient | None:
    settings = get_settings()
    if not settings.fhir_use_hapi:
        return None
    return HapiFhirClient(settings.fhir_base_url)
