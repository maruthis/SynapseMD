"""Logical backup dump/restore for CI and staging drills (E-5)."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.models.tenant import Tenant, User


async def dump_identity(session: AsyncSession) -> dict[str, Any]:
    tenants = (await session.execute(select(Tenant))).scalars().all()
    users = (await session.execute(select(User))).scalars().all()
    return {
        "tenants": [
            {"id": str(row.id), "name": row.name, "plan": row.plan} for row in tenants
        ],
        "users": [
            {
                "id": str(row.id),
                "tenant_id": str(row.tenant_id),
                "email_hash": row.email_hash,
                "role": row.role,
            }
            for row in users
        ],
    }


async def restore_identity(session: AsyncSession, payload: dict[str, Any]) -> dict[str, int]:
    from uuid import UUID

    tenant_count = 0
    for item in payload.get("tenants") or []:
        session.add(
            Tenant(
                id=UUID(item["id"]),
                name=item["name"],
                plan=item.get("plan") or "starter",
            )
        )
        tenant_count += 1
    user_count = 0
    for item in payload.get("users") or []:
        session.add(
            User(
                id=UUID(item["id"]),
                tenant_id=UUID(item["tenant_id"]),
                email_hash=item["email_hash"],
                role=item.get("role") or "patient",
            )
        )
        user_count += 1
    await session.commit()
    return {"tenants": tenant_count, "users": user_count}
