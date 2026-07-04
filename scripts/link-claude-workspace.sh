#!/usr/bin/env bash
# Create or repair .claude/ symlinks to root commands/, skills/, specialists/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="$ROOT/.claude"

mkdir -p "$CLAUDE_DIR"

link_dir() {
  local name="$1"
  local target="../${name}"
  local link_path="$CLAUDE_DIR/${name}"

  if [[ -L "$link_path" ]]; then
    echo "  OK: $link_path -> $(readlink "$link_path")"
    return
  fi

  if [[ -e "$link_path" ]]; then
    echo "  WARN: $link_path exists and is not a symlink — remove manually, then re-run"
    return 1
  fi

  ln -s "$target" "$link_path"
  echo "  linked: $link_path -> $target"
}

echo "Linking Claude Code workspace in $CLAUDE_DIR ..."
link_dir commands
link_dir skills
link_dir specialists
echo "Done."
