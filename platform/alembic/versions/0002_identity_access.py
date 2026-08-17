"""Phase B identity tables + RLS refresh.

Revision ID: 0002_identity_access
Revises: 0001_data_plane
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
    review,
    tenant,
    trackers,
)

revision: str = "0002_identity_access"
down_revision: str | None = "0001_data_plane"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind)
    if bind.dialect.name == "postgresql":
        op.execute(sa.text(RLS_SQL))


def downgrade() -> None:
    op.drop_table("break_glass_grants")
    op.drop_table("sessions")
    op.drop_table("identities")
