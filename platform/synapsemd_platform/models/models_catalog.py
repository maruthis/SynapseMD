"""Model catalog, tenant routing policy, and routing decision log (D-5–D-8)."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from synapsemd_platform.core.database import Base


class ModelCatalogEntry(Base):
    __tablename__ = "model_catalog"

    model_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    residency: Mapped[str] = mapped_column(String(32), nullable=False, default="any")
    baa_required: Mapped[bool] = mapped_column(Boolean, default=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    max_tokens: Mapped[int] = mapped_column(Integer, default=4096)
    cost_per_1k: Mapped[float] = mapped_column(Float, default=0.0)
    safety_tier: Mapped[str] = mapped_column(String(32), default="standard")
    capabilities: Mapped[list] = mapped_column(JSON, default=list)


class TenantModelPolicy(Base):
    __tablename__ = "tenant_model_policies"

    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    allowlist: Mapped[list | None] = mapped_column(JSON, nullable=True)
    residency: Mapped[str | None] = mapped_column(String(32), nullable=True)
    baa_required: Mapped[bool] = mapped_column(Boolean, default=False)
    budget_tokens_per_day: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pinned_commands: Mapped[dict] = mapped_column(JSON, default=dict)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RoutingDecisionLog(Base):
    __tablename__ = "routing_decisions_log"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    command: Mapped[str] = mapped_column(String(128), nullable=False)
    model_id: Mapped[str] = mapped_column(String(128), nullable=False)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    reason_codes: Mapped[list] = mapped_column(JSON, default=list)
    prompt_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
