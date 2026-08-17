"""Alembic upgrade/downgrade against Postgres (skipped without POSTGRES_TEST_URL)."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from synapsemd_platform.core.config import get_settings

REPO_ROOT = Path(__file__).resolve().parents[2]


def _alembic_config(database_url: str) -> Config:
    cfg = Config(str(REPO_ROOT / "platform" / "alembic.ini"))
    cfg.set_main_option("script_location", str(REPO_ROOT / "platform" / "alembic"))
    cfg.set_main_option("sqlalchemy.url", database_url)
    return cfg


@pytest.mark.postgres
def test_alembic_upgrade_downgrade(monkeypatch: pytest.MonkeyPatch) -> None:
    url = os.environ.get("POSTGRES_TEST_URL")
    if not url:
        pytest.skip("POSTGRES_TEST_URL not set")
    monkeypatch.setenv("DATABASE_URL", url)
    get_settings.cache_clear()
    cfg = _alembic_config(url)
    command.upgrade(cfg, "head")
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    get_settings.cache_clear()
