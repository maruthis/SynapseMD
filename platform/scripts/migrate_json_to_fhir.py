#!/usr/bin/env python3
"""Migrate legacy JSON health data to FHIR bundles."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from uuid import UUID

from synapsemd_platform.core.config import get_settings
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore, migrate_json_directory


async def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate JSON trackers to FHIR")
    parser.add_argument("source", type=Path, help="Directory containing profile.json, allergies.json, etc.")
    parser.add_argument("--tenant-id", required=True)
    parser.add_argument("--user-id", required=True)
    args = parser.parse_args()

    settings = get_settings()
    resources = migrate_json_directory(args.source, args.tenant_id, args.user_id)
    store = FHIRLocalStore(settings.fhir_local_store)
    dal = DataAccessLayer(store)
    await dal.upsert_resources(UUID(args.tenant_id), UUID(args.user_id), resources)
    print(f"Migrated {len(resources)} FHIR resources to {settings.fhir_local_store}")


if __name__ == "__main__":
    asyncio.run(main())
