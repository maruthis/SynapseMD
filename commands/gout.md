---
description: Log and review gout flare episodes (joint, severity, triggers, uric acid notes)
arguments:
  - name: action
    description: "Action type: add/list/update/delete/analyze/status"
    required: true
  - name: info
    description: Natural language flare details, filter, or update payload
    required: false
---

# Gout Flare Diary

Personal tracker for gout flares — joint involved, severity, possible triggers, optional uric acid notes, and status.
Supports quick logging and pattern analysis via the `gout-analyzer` skill. For personal health reference only; not a diagnosis or treatment plan.

## Action Types

### 1. Add flare — `add`

Add a new gout flare episode from natural language.

**Parameter Description:**
- `info`: Flare details (required) — joint, side, severity, triggers, optional uric acid, notes

**Examples:**
```
/gout add right big toe severe overnight after seafood and beer
/gout add left ankle moderate after long walk uric acid last checked 7.8
/gout add right knee mild after dehydration notes swelling overnight
```

### 2. List flares — `list`

View flares with optional filters.

**Examples:**
```
/gout list
/gout list severe
/gout list right big toe
/gout list last 90 days
/gout list active
```

### 3. Update flare — `update`

Update an existing flare (match by joint/side/date keywords in `info`).

**Examples:**
```
/gout update right big toe status resolving
/gout update left ankle notes ice helped overnight
/gout update right knee severity moderate
```

**Supported fields:**
- `severity`: mild / moderate / severe
- `status`: active / resolving / resolved
- `notes`: free text
- `triggers`: add or replace trigger keywords
- `uric_acid_mg_dl`: numeric lab note if user supplies one

### 4. Delete flare — `delete`

Remove a flare record (prefer soft guidance: confirm joint + date before deleting).

**Examples:**
```
/gout delete right big toe 2026-07-01
```

### 5. Analyze patterns — `analyze`

Delegate deep analysis to the skill (do not embed scoring algorithms in this command).

**Examples:**
```
/gout analyze
/gout analyze last 6 months
/gout analyze triggers
```

### 6. Status summary — `status`

Quick overview: flare count, last flare, open/active flares, most common joints.

**Examples:**
```
/gout status
```

## Data Contract

| Operation | Path |
|-----------|------|
| Read/Write | `data/gout-tracker.json` |
| Example schema | `data-example/gout-tracker.json` |

## Execution Steps

### Add (add)

1. Parse `info` into structured fields:
   - `joint` (e.g. first MTP, ankle, knee, wrist, elbow)
   - `side` (left / right / bilateral / unspecified)
   - `severity` (mild / moderate / severe) from keywords
   - `triggers[]` (seafood, alcohol, beer, dehydration, trauma, unknown, etc.)
   - `notes` (remaining free text)
   - optional `uric_acid_mg_dl` if a number is clearly a lab value
   - `onset` (ISO date if stated, else today's date in local context)
2. Read `data/gout-tracker.json`. If missing, initialize from `data-example/gout-tracker.json` structure (`flares: []`, zeroed statistics).
3. Append a record with unique `id` (e.g. `gout-YYYY-MM-DD-NNN`) and `recorded_at` (ISO timestamp). Default `status` to `active`.
4. Recalculate `statistics` (`total_flares`, `active_flares`, `severe_count`, `last_flare_date`, `last_updated`).
5. Write the file back to `data/gout-tracker.json`.
6. Render confirmation using the output format below.

### List (list)

1. Read `data/gout-tracker.json`.
2. Filter by keywords in `info` if provided (`severe`, `active`, joint name, side, `last N days`).
3. Sort newest-first by `onset` or `recorded_at`.
4. Render a concise list.

### Update (update)

1. Read `data/gout-tracker.json`.
2. Locate the best-matching flare from `info` (joint + side + optional date).
3. If ambiguous, list candidates and ask which `id` to update.
4. Apply field updates; set `last_updated` on the record and tracker statistics.
5. Write and confirm.

### Delete (delete)

1. Read tracker; match flare by joint/date/`id`.
2. Confirm identity in the response summary before removal if multiple matches.
3. Remove the record; refresh statistics; write file.

### Analyze (analyze)

1. Read `data/gout-tracker.json`.
2. Invoke Skill("gout-analyzer") with the tracker content and any date window or focus from `info`.
3. Present the skill report with safety disclaimers.

### Status (status)

1. Read `data/gout-tracker.json`.
2. Summarize counts, last flare, top joints, and whether any flares are still `active`.

## Severity Keyword Mapping

| Keywords | Severity |
|----------|----------|
| mild, slight, dull | mild |
| moderate, noticeable, limping | moderate |
| severe, can't walk, excruciating, unbearable | severe |

## Joint Standardization (examples)

| Colloquial | Prefer storing as |
|------------|-------------------|
| big toe, podagra | first MTP |
| ankle | ankle |
| knee | knee |
| wrist / elbow / finger / midfoot | as stated |

## Output Format

```markdown
## Gout Diary — [Action]

- **Summary**: …
- **Record / matches**: …
  - id, onset, joint, side, severity, status, triggers, uric_acid_mg_dl, notes
- **Statistics**: total / active / severe / last flare date
- **Next step suggestion**: continue logging; discuss accelerating patterns with a clinician (non-prescriptive)
```

## Safety

This command is for personal health management only. It:

1. Does not provide specific medication dosages
2. Does not directly prescribe prescription drugs
3. Does not predict life prognosis
4. Does not replace physician diagnosis

All output is for reference only. Consult a qualified healthcare professional for medical decisions.

## Related

- Skill: `gout-analyzer` (`skills/gout-analyzer/SKILL.md`)
- Specialist: Rheumatology (`specialists/rheumatology.md`) via `/specialist rheum` or `/consult`
