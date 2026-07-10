# User Guide

> **New to SynapseMD?** Start with the step-by-step [Getting Started Guide](getting-started.md) before using the commands below.

## Quick Start

1. Ensure Claude Code is installed
2. Open Claude Code in the current directory
3. First-time setup: `/profile set 175 70 1990-01-01`
4. Save first report: `/save-report /path/to/image.jpg`
5. Record radiation: `/radiation add CT chest`
6. Query all records: `/query all`
7. Start MDT consultation: `/consult`

## Using `data-example/` for testing

SynapseMD keeps **sample health data** in `data-example/` and your **live records** in `data/`. Commands always read and write `data/` — never edit `data-example/` for day-to-day use.

| Directory | Purpose | Committed to Git? |
|-----------|---------|-------------------|
| `data-example/` | Sample trackers, logs, and schemas for demos and testing | Yes |
| `data/` | Your live personal health records | No (gitignored) |

Use `data-example/` when you want to try commands, AI analysis, or consultations **without entering your own medical data first**.

### What is in `data-example/`

About 50 sample files covering major domains, including:

- **Profile & core:** `profile.json`, `allergies.json`, `radiation-records.json`, `index.json`
- **Chronic care:** `hypertension-tracker.json`, `diabetes-tracker.json`, `copd-tracker.json`
- **Lifestyle:** `sleep-tracker.json`, `nutrition-tracker.json`, `fitness-tracker.json` (+ dated logs under `*-logs/`)
- **Life stages:** pregnancy, postpartum, menopause, child health, men’s health trackers
- **Other modules:** mental health, travel, occupational, TCM, rehabilitation, screening, and more

Many trackers already contain **realistic sample values** (for example blood pressure readings, sleep schedules, nutrition goals). `profile.json` in the example set may still have empty fields — set them with `/profile` after seeding.

Full file list: [data-example/README.md](../data-example/README.md). Schema reference: [data-structures.md](data-structures.md).

### Seed `data/` from examples (first time)

From the repo root:

```bash
./scripts/setup-data.sh
```

This copies `data-example/` → `data/` **only if** `data/profile.json` does not already exist. It also links reference databases (food, vaccines) and seeds `data/ai-config.json`.

Then open Claude Code or Cursor in the repo and try:

```bash
/profile set 175 70 1973-01-01
/query all
/sleep status
/nutrition status
/ai analyze last_quarter
/consult recent 5
```

### Refresh sample data for a clean test (overwrite)

`setup-data.sh` will **not** overwrite an existing `data/` folder. To reset to the sample set for testing:

```bash
# Optional but recommended: back up your current live data first
cp -r data/ ~/Backups/SynapseMD-data-$(date +%Y-%m-%d)

# Replace live data with a fresh copy of the examples
rm -rf data/
./scripts/setup-data.sh
```

Or copy only the domains you need (keeps the rest of `data/` intact):

```bash
cp data-example/hypertension-tracker.json data/
cp -r data-example/sleep-logs data/
cp data-example/sleep-tracker.json data/
```

### Suggested test flows with sample data

| Goal | After seeding, try |
|------|--------------------|
| Confirm data loaded | `/query all` · `/profile view` |
| Lifestyle modules | `/sleep status` · `/nutrition status` · `/fitness status` |
| Chronic disease | `/hypertension status` · `/diabetes status` |
| Drug safety | `/medication list` · `/interaction check` |
| AI (Module 21) | `/ai status` · `/ai analyze last_quarter` · `/ai predict hypertension` |
| MDT consult | `/consult recent 5` · `/specialist cardio recent 3` |

### Rules for testing

1. **Do not commit** files under `data/` — that folder is for local use only.
2. **Do not put real PHI into `data-example/`** — keep examples synthetic or anonymized.
3. **Back up `data/`** before a force refresh if you have real records you care about.
4. Sample data is for **learning and demos** — not a substitute for your own clinical records or medical advice.

## Core Command Usage

### 0. Set User Basic Parameters (Required for First-Time Use)

Use the `/profile` command to set basic parameters:

```bash
# Set complete parameters
/profile set 175 70 1990-01-01

# Or use parameter names
/profile set height=175 weight=70 birth_date=1990-01-01

# View current parameters
/profile view
```

**Required Information:**
- Height (cm) - Used to calculate body surface area and BMI
- Weight (kg) - Used to calculate body surface area and BMI
- Birth date (YYYY-MM-DD) - Used to calculate age

**System Automatically Calculates:**
- BMI (Body Mass Index)
- Body surface area (for radiation dose calculation)
- Age

### 1. Save Medical Reports

Use the `/save-report` command to save medical examination reports:

```bash
/save-report /path/to/report-image.jpg
```

**Supported Report Types:**
- ✅ Biochemical tests: Complete blood count, urinalysis, comprehensive biochemistry panel, etc.
- ✅ Medical imaging: Ultrasound, CT, MRI, X-ray, etc.

**System Will Automatically:**
- Identify report type
- Extract examination date
- Extract test indicator data
- Identify reference ranges and abnormal markers
- Save in structured JSON format
- Backup original images

### 2. Manage Medical Radiation Exposure

Use the `/radiation` command to record and track radiation exposure from medical imaging:

```bash
# Add radiation examination records
/radiation add CT chest
/radiation add CT abdomen 2025-12-30
/radiation add X-ray chest
/radiation add PET-CT whole body

# View current cumulative status
/radiation status

# View history records
/radiation history

# Clear all records
/radiation clear
```

**Radiation Management System Features:**
- Automatically calculate radiation dose based on examination type and body part
- Adjust dose based on user's body surface area
- Track annual cumulative radiation dose
- Calculate residual radiation from previous years (50% decay/year)
- Safety assessment and risk alerts
- History records and statistical analysis

**Supported Examination Types:**
- CT scans (head, chest, abdomen, pelvis, spine, extremities)
- X-ray examinations (chest, abdomen, extremities, dental)
- PET-CT, bone scans, angiography, etc.

### 3. Query Medical Records

Use the `/query` command to query records:

```bash
# Query all records
/query all

# Query biochemical tests
/query biochemical

# Query imaging examinations
/query imaging

# Query recent N records
/query recent 5

# Query by date
/query date 2025-12
/query date 2025-12-31

# Query abnormal indicators
/query abnormal
```

### 4. Multi-Disciplinary Team Consultation (MDT)

Use the `/consult` command to start multi-disciplinary specialist consultation:

```bash
# Analyze all data for consultation
/consult all

# Analyze recent N records
/consult recent 5

# Analyze data for specified date
/consult date 2025-12-31

# Analyze specified date range
/consult date 2025-12-01 to 2025-12-31

# Automatic analysis (default: recent 3 records)
/consult
```

**Consultation System Will:**
- Automatically identify involved specialties (cardiology, endocrinology, gastroenterology, nephrology, etc.)
- Launch multiple specialist subagents in parallel for independent analysis
- Integrate opinions from all specialties to generate comprehensive consultation report
- Provide prioritized recommendations and comprehensive management suggestions

**Supported 9 Major Specialties:**
- Cardiology - Heart diseases, hypertension, lipid abnormalities
- Endocrinology - Diabetes, thyroid diseases
- Gastroenterology - Liver diseases, gastrointestinal diseases
- Nephrology - Kidney diseases, electrolyte disorders
- Hematology - Anemia, coagulation abnormalities
- Respiratory Medicine - Pulmonary infections, lung nodules
- Neurology - Cerebrovascular diseases, headaches, dizziness
- Oncology - Tumor markers, cancer screening
- General Practice - Comprehensive assessment, chronic disease management

### 5. Single Specialty Consultation

Use the `/specialist` command to consult a specific specialty:

```bash
# View list of supported specialties
/specialist list

# Consult cardiology
/specialist cardio recent 3

# Consult endocrinology
/specialist endo all

# Consult oncology
/specialist onco date 2025-12-31
```

## Important Notes

- First-time use requires setting basic parameters (height, weight, birth date)
- For demos and testing without your own records, seed from `data-example/` (see [Using data-example for testing](#using-data-example-for-testing))
- Ensure medical report images are clear and readable
- Supported image formats: JPG, PNG
- Regularly backup the `data/` directory
- Date format uses YYYY-MM-DD consistently
- Radiation doses are for reference only; please consult a doctor
- Regularly check `/radiation status` to understand cumulative exposure

## Expert Consultation System Safety Principles

This system strictly follows the following medical safety principles:

### ⚠️ Safety Red Lines
1. **Does not provide specific medication dosages**
2. **Does not directly prescribe prescription drugs**
3. **Does not predict life prognosis**
4. **Does not replace doctor diagnosis**

### ✅ What the System Can Do
- Interpret clinical significance of medical test indicators
- Identify abnormal indicators and potential risks
- Provide healthy lifestyle recommendations
- Recommend targeted examination items
- Assist in developing follow-up plans
- Integrate multi-disciplinary expert opinions

### ⚠️ Important Disclaimer
- **All analysis reports from this system are for reference only**
- **Should not be used as a basis for medical diagnosis**
- **All medical decisions require consultation with professional doctors**
- **In case of emergency, seek immediate medical attention**
