"""Tenant-scoped AI configuration loading."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID

from synapsemd_platform.ai.config_defaults import DEFAULT_AI_CONFIG


class TenantAIConfigStore:
    """Loads AI config per tenant from DB settings, tenant file, or defaults."""

    def __init__(self, config_dir: str | Path | None = None) -> None:
        self.config_dir = Path(config_dir) if config_dir else Path("./data/ai-config")

    def resolve(
        self,
        tenant_id: UUID,
        tenant_settings: dict | None = None,
    ) -> dict:
        if tenant_settings:
            return self._merge(DEFAULT_AI_CONFIG, tenant_settings)

        file_config = self._load_file(tenant_id)
        if file_config:
            return self._merge(DEFAULT_AI_CONFIG, file_config)

        return DEFAULT_AI_CONFIG.copy()

    def _load_file(self, tenant_id: UUID) -> dict | None:
        path = self.config_dir / f"{tenant_id}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _merge(base: dict, override: dict) -> dict:
        merged = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = TenantAIConfigStore._merge(merged[key], value)
            else:
                merged[key] = value
        return merged
