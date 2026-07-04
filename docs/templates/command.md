---
description: Short one-line description of what this command does
arguments:
  - name: action
    description: "Action type: add/list/update/delete/analyze"
    required: true
  - name: info
    description: Natural language payload or filter (optional)
    required: false
---

# My Feature Command

Brief description of the command purpose and the health domain it manages.

## Action Types

### 1. Add Record — `add`

Add a new record.

**Examples:**
```
/my-feature add example natural language input
```

### 2. List Records — `list`

View all records.

**Examples:**
```
/my-feature list
```

## Data Contract

| Operation | Path |
|-----------|------|
| Read/Write | `data/my-feature-tracker.json` |
| Logs | `data/my-feature-logs/YYYY-MM/YYYY-MM-DD.json` |

## Execution Steps

### Add (add)

1. Parse natural language from `info` into structured fields
2. Read `data/my-feature-tracker.json`
3. Append the new record with a unique `id` and ISO timestamp
4. Write updated JSON back to `data/my-feature-tracker.json`
5. Render output using the format below

### List (list)

1. Read `data/my-feature-tracker.json`
2. Apply filters based on `info` if provided
3. Render output using the format below

## Analyze (optional)

For deep analysis, delegate to a skill — do not embed algorithms here:

1. Read current data from `data/my-feature-tracker.json`
2. Invoke Skill("my-feature-analyzer")
3. Render the skill output

## Output Format

```markdown
## My Feature — [Action Result]

- **Summary**: ...
- **Records**: ...
```

## Safety (required for clinical modules)

This command is for personal health management only. It:

1. Does not provide specific medication dosages
2. Does not directly prescribe prescription drugs
3. Does not predict life prognosis
4. Does not replace physician diagnosis

All output is for reference only. Consult a qualified healthcare professional for medical decisions.

## Platform Integration (optional)

If this command is registered in `AVAILABLE_COMMANDS`:

```bash
curl -X POST http://localhost:8000/api/v1/commands/execute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command":"my-feature","context_text":"list all records"}'
```

See [developer-guide.md](../developer-guide.md#11-recipe-wire-to-the-platform).
