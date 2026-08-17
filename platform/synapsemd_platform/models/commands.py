"""Command catalog seeded from platform command ids (A-11)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from synapsemd_platform.core.database import Base

# (command_id, sensitivity) — source of truth for API/MCP registration.
PLATFORM_COMMANDS: tuple[tuple[str, str], ...] = (
    ("ai", "complex"),
    ("goal", "complex"),
    ("consult", "critical"),
    ("specialist", "critical"),
    ("nutrition", "moderate"),
    ("fitness", "moderate"),
    ("sleep", "moderate"),
    ("mental-health", "critical"),
    ("interaction", "complex"),
    ("profile", "simple"),
    ("query", "simple"),
    ("health-trend-analyzer", "complex"),
    ("gout", "simple"),
    ("allergy", "simple"),
)

AVAILABLE_COMMANDS: list[str] = [item[0] for item in PLATFORM_COMMANDS]


class CommandCatalogEntry(Base):
    __tablename__ = "command_catalog"

    command_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    sensitivity: Mapped[str] = mapped_column(String(32), nullable=False, default="moderate")
    scopes: Mapped[list] = mapped_column(JSON, default=list)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


def command_seed_rows() -> list[dict]:
    return [
        {
            "command_id": command_id,
            "sensitivity": sensitivity,
            "scopes": ["read:own", "write:own"],
            "enabled": True,
        }
        for command_id, sensitivity in PLATFORM_COMMANDS
    ]
