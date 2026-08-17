"""PHI models: catalog, tenant policy, routing log, BAA registry.

Revision ID: 0004_phi_models
Revises: 0003_observability_audit
Create Date: 2026-08-17
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from synapsemd_platform.core.database import Base
from synapsemd_platform.core.rls import RLS_SQL
from synapsemd_platform.llm.policy import DEFAULT_CATALOG
from synapsemd_platform.models import (  # noqa: F401
    audit,
    clinical,
    governance,
    iam,
    models_catalog,
    review,
    tenant,
    trackers,
)

revision: str = "0004_phi_models"
down_revision: str | None = "0003_observability_audit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind)
    existing = {
        row[0]
        for row in bind.execute(sa.text("SELECT model_id FROM model_catalog")).fetchall()
    }
    rows = [
        {
            "model_id": item.model_id,
            "provider": item.provider,
            "display_name": item.display_name or item.model_id,
            "residency": item.residency,
            "baa_required": item.baa_required,
            "enabled": item.enabled,
            "max_tokens": item.max_tokens,
            "cost_per_1k": item.cost_per_1k,
            "safety_tier": item.safety_tier,
            "capabilities": ["chat"],
        }
        for item in DEFAULT_CATALOG
        if item.model_id not in existing
    ]
    if rows:
        op.bulk_insert(models_catalog.ModelCatalogEntry.__table__, rows)
    if bind.dialect.name == "postgresql":
        op.execute(sa.text(RLS_SQL))


def downgrade() -> None:
    op.drop_table("routing_decisions_log")
    op.drop_table("tenant_model_policies")
    op.drop_table("baa_records")
    op.drop_table("model_catalog")
