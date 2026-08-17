---
name: gout-analyzer
description: Analyze gout flare diary for frequency, severity trends, trigger patterns, and non-prescriptive monitoring suggestions. Use when the user runs /gout analyze or asks about gout flare patterns.
allowed-tools: Read, Grep, Glob, Write
---

# Gout Analyzer Skill

Analyze `data/gout-tracker.json` (and optional related nutrition/profile/lab context) to surface patterns for discussion with a clinician. This skill owns analysis only — it does not create or delete diary records (CRUD stays in `/gout`).

## Features

### 1. Flare frequency and severity

- Count flares in the requested window (default: last 6 months if unspecified)
- Severity mix (mild / moderate / severe)
- Joints most often involved (laterality when available)
- Active vs resolved flare counts

### 2. Trigger signals

- Recurring dietary or lifestyle triggers from `triggers[]` and notes
- Cluster detection (multiple flares within 14 days)
- Observational language only — do not claim proven causation

### 3. Lab / context cross-checks (if files exist)

| Domain | Path | Why |
|--------|------|-----|
| Gout diary | `data/gout-tracker.json` | Primary source |
| Profile | `data/profile.json` | Age/sex context only when present |
| Nutrition | `data/nutrition-tracker.json` | Optional diet context |
| Hypertension / diabetes trackers | `data/hypertension-tracker.json`, `data/diabetes-tracker.json` | Comorbid context if present |
| Exam / report JSON under `data/` | Glob as needed | Uric acid mentions only if present |

Never invent uric acid or other lab values. If missing, state “not available in supplied data.”

## Analysis Steps

1. Load `data/gout-tracker.json` via Read (create guidance: if missing, report empty diary — do not invent flares).
2. Parse date window or focus from the invoking command (`last 6 months`, `triggers`, etc.).
3. Aggregate frequency, severity, joints, laterality, and trigger keywords.
4. Detect clusters (≥2 flares within 14 days).
5. Optionally correlate with nutrition/profile/chronic trackers **only if readable**.
6. Produce the report format below.
7. Stay within medical safety boundaries.

## Output Format

```markdown
## Gout Pattern Analysis

### Summary
- Window: …
- Flare count: …
- Active / resolved: …
- Predominant joints / severity: …
- Last flare: …

### Possible trigger patterns
- … (observational; not proven causation)

### Clusters / escalation signals
- … (e.g. increasing frequency, new joints) or “none noted”

### Lab / comorbidity context
- Uric acid notes from diary: …
- Other available context: … or “not available”

### Monitoring suggestions (non-prescriptive)
- What to log next time (joint, severity, triggers, timing)
- When to discuss with a clinician (e.g. accelerating flares, new joints, inability to bear weight)

### Disclaimer
Personal reference only — not a diagnosis or treatment plan. Does not replace physician assessment.
```

## Medical Safety Boundaries

1. Does not provide specific medication dosages
2. Does not directly prescribe prescription drugs
3. Does not predict life prognosis
4. Does not replace physician diagnosis

Output is for reference only.

## Cross-Module Correlation

| Domain | Path |
|--------|------|
| Profile | `data/profile.json` |
| Nutrition | `data/nutrition-tracker.json` |
| Hypertension | `data/hypertension-tracker.json` |
| Diabetes | `data/diabetes-tracker.json` |
