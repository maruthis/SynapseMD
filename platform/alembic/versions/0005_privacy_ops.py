"""Privacy ops: DSR requests and legal holds.

Revision ID: 0005_privacy_ops
Revises: 0004_phi_models
Create Date: 2026-08-17
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from synapsemd_platform.core.database import Base
from synapsemd_platform.core.rls import RLS_SQL
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

revision: str = "0005_privacy_ops"
down_revision: str | None = "0004_phi_models"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind)
    if bind.dialect.name == "postgresql":
        op.execute(sa.text(RLS_SQL))


def downgrade() -> None:
    op.drop_table("dsr_requests")
    op.drop_table("legal_holds")
