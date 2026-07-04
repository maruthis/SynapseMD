#!/usr/bin/env bash
# Validate a slash command markdown file against SynapseMD conventions.
# Usage: ./scripts/validate-command.sh <command-name>
# Example: ./scripts/validate-command.sh allergy
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="${1:-}"

if [[ -z "$NAME" ]]; then
  echo "Usage: $0 <command-name>" >&2
  exit 1
fi

CMD_FILE="$ROOT/commands/${NAME}.md"
ERRORS=0

fail() {
  echo "FAIL: $1" >&2
  ERRORS=$((ERRORS + 1))
}

pass() {
  echo "OK:   $1"
}

if [[ ! -f "$CMD_FILE" ]]; then
  echo "Command file not found: $CMD_FILE" >&2
  exit 1
fi

CONTENT="$(cat "$CMD_FILE")"

# YAML frontmatter
if [[ "$CONTENT" != ---* ]]; then
  fail "Missing YAML frontmatter (file must start with ---)"
else
  pass "YAML frontmatter present"
fi

if ! echo "$CONTENT" | head -20 | grep -q '^description:'; then
  fail "Frontmatter missing 'description:'"
else
  pass "description field present"
fi

if ! echo "$CONTENT" | head -30 | grep -q 'name: action'; then
  fail "Frontmatter missing 'action' argument (recommended convention)"
else
  pass "action argument present"
fi

# Data contract hints
if echo "$CONTENT" | grep -q 'data/'; then
  pass "References data/ paths"
else
  fail "No data/ path references — declare read/write paths explicitly"
fi

# Execution steps
if echo "$CONTENT" | grep -qi 'execution step'; then
  pass "Execution steps section found"
else
  fail "No execution steps section — add numbered steps for each action"
fi

# Output format
if echo "$CONTENT" | grep -qi 'output format'; then
  pass "Output format section found"
else
  fail "No output format section"
fi

# Symlink visibility
if [[ -L "$ROOT/.claude/commands" ]]; then
  RESOLVED="$(readlink "$ROOT/.claude/commands")"
  if [[ "$RESOLVED" == "../commands" ]]; then
    pass ".claude/commands symlink OK"
  else
    fail ".claude/commands symlink points to '$RESOLVED', expected '../commands'"
  fi
else
  fail ".claude/commands is not a symlink — run ./scripts/link-claude-workspace.sh"
fi

# Example data (warn only)
if [[ -f "$ROOT/data-example/${NAME}.json" ]] || \
   ls "$ROOT/data-example/"*"${NAME}"* 1>/dev/null 2>&1; then
  pass "Matching data-example template found"
else
  echo "WARN: No obvious data-example template for '$NAME' — add one if command uses JSON storage"
fi

# Platform registration (info only)
if grep -q "\"${NAME}\"" "$ROOT/platform/synapsemd_platform/api/routes/commands.py" 2>/dev/null; then
  pass "Registered in platform AVAILABLE_COMMANDS"
else
  echo "INFO: '$NAME' not in AVAILABLE_COMMANDS — OK for CLI-only commands"
fi

if [[ "$ERRORS" -gt 0 ]]; then
  echo ""
  echo "$ERRORS validation error(s). See docs/developer-guide.md for conventions."
  exit 1
fi

echo ""
echo "Command '$NAME' passed validation."
