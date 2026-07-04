#!/usr/bin/env bash
# Initialize live data/ from data-example templates and reference databases.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$ROOT/data"
EXAMPLE_DIR="$ROOT/data-example"
REFERENCE_DIR="$ROOT/data/reference"

echo "Setting up SynapseMD data directory..."

mkdir -p "$DATA_DIR" "$REFERENCE_DIR"

# Reference databases (committed, read-only lookups)
for f in food-database.json vaccine-database.json food-categories.json nutritional-reference.json; do
  if [[ -f "$REFERENCE_DIR/$f" ]]; then
    echo "  reference: $f (already in data/reference/)"
  fi
done

# Copy example tracker templates into data/ (skip if data already has content)
if [[ ! -f "$DATA_DIR/profile.json" ]]; then
  echo "  copying example trackers from data-example/ → data/"
  rsync -a --exclude='*.backup' \
    --exclude='food-database.json' \
    --exclude='vaccine-database.json' \
    --exclude='food-categories.json' \
    --exclude='nutritional-reference.json' \
    "$EXAMPLE_DIR/" "$DATA_DIR/"
else
  echo "  data/profile.json exists — skipping template copy"
fi

# Symlink reference databases into data/ for commands that expect data/*.json paths
ln -sf reference/food-database.json "$DATA_DIR/food-database.json" 2>/dev/null || \
  cp "$REFERENCE_DIR/food-database.json" "$DATA_DIR/food-database.json"
ln -sf reference/vaccine-database.json "$DATA_DIR/vaccine-database.json" 2>/dev/null || \
  cp "$REFERENCE_DIR/vaccine-database.json" "$DATA_DIR/vaccine-database.json"

# AI config template (optional local dev)
mkdir -p "$DATA_DIR/ai-config"
if [[ ! -f "$DATA_DIR/ai-config.json" ]]; then
  cp "$ROOT/data/templates/ai-config.json" "$DATA_DIR/ai-config.json"
  echo "  seeded: data/ai-config.json"
fi

echo "Done. Live data: $DATA_DIR | Reference DBs: $REFERENCE_DIR"
