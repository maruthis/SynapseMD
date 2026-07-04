# Contributing to SynapseMD

Thank you for extending SynapseMD. This project grows through commands, skills, specialists, data schemas, and optional platform integrations — not only through Python code.

## Before you start

1. Read the **[Developer Guide](docs/developer-guide.md)** — extension recipes, checklists, and architecture rules.
2. Edit source-of-truth directories at the repo root:
   - `commands/` — not `.claude/commands/` directly
   - `skills/` — not `.claude/skills/` directly
   - `specialists/` — not `.claude/specialists/` directly
3. Verify symlinks after clone:

   ```bash
   ./scripts/link-claude-workspace.sh
   ls -la .claude/commands .claude/skills .claude/specialists
   ```

## Development setup

```bash
git clone https://github.com/maruthis/SynapseMD.git
cd SynapseMD
./scripts/setup-data.sh
./scripts/link-claude-workspace.sh
```

Platform work (optional):

```bash
cd platform && pip install -e ".[dev]"
pytest -v   # from repo root
```

See [docs/local-development.md](docs/local-development.md).

## What to update for each change type

| Change | Required updates |
|--------|------------------|
| New command | `commands/<name>.md`, `data-example/` template, `docs/data-structures.md`, `docs/user-guide.md` |
| New skill | `skills/<name>/SKILL.md`, owning command updated to invoke skill |
| New specialist | `specialists/<name>.md`, `commands/consult.md` routing if MDT-relevant |
| Platform exposure | `AVAILABLE_COMMANDS`, router complexity, tests |
| Clinical / mental-health | Safety disclaimers per [docs/safety-guidelines.md](docs/safety-guidelines.md) |

Templates: [docs/templates/](docs/templates/)

## Validation

```bash
./scripts/validate-command.sh <command-name>   # structure lint
pytest -v                                       # platform tests (if platform touched)
./scripts/test-<domain>.sh                      # domain scripts when available
```

## Pull request checklist

- [ ] Edited root `commands/`, `skills/`, or `specialists/` (not copies in `.claude/`)
- [ ] New JSON schemas have `data-example/` templates and `data-structures.md` entries
- [ ] Clinical modules include safety disclaimers
- [ ] `docs/user-guide.md` updated for user-facing command changes
- [ ] Platform commands added to `AVAILABLE_COMMANDS` with router complexity set
- [ ] Tests added or updated for platform/Python changes
- [ ] No live user data committed (`data/` is gitignored)
- [ ] `./scripts/validate-command.sh` passes for new/changed commands

## Code of conduct for health content

- Output is informational only — never present as diagnosis or prescription
- Do not commit PHI or personal health records
- Follow [docs/clinical-safety-policy.md](docs/clinical-safety-policy.md) for platform changes

## Questions

- Architecture: [docs/architecture.md](docs/architecture.md)
- Extension how-to: [docs/developer-guide.md](docs/developer-guide.md)
- Platform API: [platform/README.md](platform/README.md)

Open an issue on GitHub for questions or propose changes via pull request.
