"""Dual-read adapter: Postgres first, JSON fallback. Writes go to Postgres only."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from synapsemd_platform.adapters.legacy_json import LegacyJsonAdapter
from synapsemd_platform.adapters.postgres import PostgresHealthAdapter


class DualHealthAdapter:
    def __init__(
        self,
        postgres: PostgresHealthAdapter,
        json_store: LegacyJsonAdapter,
    ) -> None:
        self.postgres = postgres
        self.json_store = json_store

    async def get_profile(self, tenant_id: UUID, user_id: UUID) -> dict[str, Any] | None:
        row = await self.postgres.get_profile(tenant_id, user_id)
        if row:
            return row
        return await self.json_store.get_profile(tenant_id, user_id)

    async def upsert_profile(
        self, tenant_id: UUID, user_id: UUID, profile: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.postgres.upsert_profile(tenant_id, user_id, profile)

    async def list_allergies(
        self, tenant_id: UUID, user_id: UUID, *, status: str | None = None
    ) -> list[dict[str, Any]]:
        rows = await self.postgres.list_allergies(tenant_id, user_id, status=status)
        if rows:
            return rows
        return await self.json_store.list_allergies(tenant_id, user_id, status=status)

    async def add_allergy(
        self, tenant_id: UUID, user_id: UUID, record: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.postgres.add_allergy(tenant_id, user_id, record)

    async def update_allergy(
        self, tenant_id: UUID, user_id: UUID, record_id: str, patch: dict[str, Any]
    ) -> dict[str, Any] | None:
        return await self.postgres.update_allergy(tenant_id, user_id, record_id, patch)

    async def delete_allergy(self, tenant_id: UUID, user_id: UUID, record_id: str) -> bool:
        return await self.postgres.delete_allergy(tenant_id, user_id, record_id)

    async def list_gout_flares(
        self, tenant_id: UUID, user_id: UUID, *, status: str | None = None
    ) -> list[dict[str, Any]]:
        rows = await self.postgres.list_gout_flares(tenant_id, user_id, status=status)
        if rows:
            return rows
        return await self.json_store.list_gout_flares(tenant_id, user_id, status=status)

    async def add_gout_flare(
        self, tenant_id: UUID, user_id: UUID, record: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.postgres.add_gout_flare(tenant_id, user_id, record)

    async def update_gout_flare(
        self, tenant_id: UUID, user_id: UUID, record_id: str, patch: dict[str, Any]
    ) -> dict[str, Any] | None:
        return await self.postgres.update_gout_flare(tenant_id, user_id, record_id, patch)

    async def delete_gout_flare(self, tenant_id: UUID, user_id: UUID, record_id: str) -> bool:
        return await self.postgres.delete_gout_flare(tenant_id, user_id, record_id)
