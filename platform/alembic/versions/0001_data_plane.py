"""Initial data plane schema + RLS.

Revision ID: 0001_data_plane
Revises:
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

revision: str = "0001_data_plane"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind)
    if bind.dialect.name == "postgresql":
        op.execute(sa.text(RLS_SQL))


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind)
