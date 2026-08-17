"""Health store adapter protocol (JSON vault vs Postgres SoR)."""

from __future__ import annotations

from typing import Any, Protocol
from uuid import UUID


class HealthStoreAdapter(Protocol):
    async def get_profile(self, tenant_id: UUID, user_id: UUID) -> dict[str, Any] | None: ...

    async def upsert_profile(
        self, tenant_id: UUID, user_id: UUID, profile: dict[str, Any]
    ) -> dict[str, Any]: ...

    async def list_allergies(
        self, tenant_id: UUID, user_id: UUID, *, status: str | None = None
    ) -> list[dict[str, Any]]: ...

    async def add_allergy(
        self, tenant_id: UUID, user_id: UUID, record: dict[str, Any]
    ) -> dict[str, Any]: ...

    async def update_allergy(
        self, tenant_id: UUID, user_id: UUID, record_id: str, patch: dict[str, Any]
    ) -> dict[str, Any] | None: ...

    async def delete_allergy(self, tenant_id: UUID, user_id: UUID, record_id: str) -> bool: ...

    async def list_gout_flares(
        self, tenant_id: UUID, user_id: UUID, *, status: str | None = None
    ) -> list[dict[str, Any]]: ...

    async def add_gout_flare(
        self, tenant_id: UUID, user_id: UUID, record: dict[str, Any]
    ) -> dict[str, Any]: ...

    async def update_gout_flare(
        self, tenant_id: UUID, user_id: UUID, record_id: str, patch: dict[str, Any]
    ) -> dict[str, Any] | None: ...

    async def delete_gout_flare(self, tenant_id: UUID, user_id: UUID, record_id: str) -> bool: ...
