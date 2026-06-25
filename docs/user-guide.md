# User Guide

## Quick Start

1. Ensure Claude Code is installed
2. Open Claude Code in the current directory
3. For first-time use, set your basic profile: `/profile set 175 70 1990-01-01`
4. Use `/save-report /path/to/image.jpg` to save your first medical report
5. Use `/radiation add CT chest` to record a radiation examination
6. Use `/query all` to view all records
7. Use `/consult` to start a multidisciplinary expert consultation

## Core Command Usage

### 0. Set Your Basic Profile (Required for First-Time Use)

Use the `/profile` command to set your basic profile:

```bash
# Set all parameters
/profile set 175 70 1990-01-01

# Or use named parameters
/profile set height=175 weight=70 birth_date=1990-01-01

# View current parameters
/profile view
```

**Information to set:**
- Height (cm) — used to calculate body surface area and BMI
- Weight (kg) — used to calculate body surface area and BMI
- Date of birth (YYYY-MM-DD) — used to calculate age

**The system will automatically calculate:**
- BMI (Body Mass Index)
- Body surface area (used for radiation dose calculations)
- Age

### 1. Save Medical Reports

Use the `/save-report` command to save medical examination reports:

```bash
/save-report /path/to/report-image.jpg
```

**Supported report types:**
- ✅ Biochemical examinations: CBC, urinalysis, comprehensive metabolic panel, etc.
- ✅ Imaging examinations: Ultrasound, CT, MRI, X-ray, etc.

**The system will automatically:**
- Identify the type of report
- Extract the examination date
- Extract indicator values
- Identify reference ranges and abnormal flags
- Save as structured JSON format
- Back up the original image

### 2. Manage Medical Radiation Exposure

Use the `/radiation` command to record and track radiation exposure from medical imaging examinations:

```bash
# Add a radiation examination record
/radiation add CT chest
/radiation add CT abdomen 2025-12-30
/radiation add X-ray chest
/radiation add PET-CT whole-body

# View current cumulative status
/radiation status

# View history
/radiation history

# Clear all records
/radiation clear
```

**Radiation management system features:**
- Automatically calculates radiation dose by examination type and body part
- Adjusts dose based on the user's body surface area
- Tracks annual cumulative radiation dose
- Calculates residual radiation from prior years (50%/year decay)
- Safety assessment and risk alerts
- Historical records and statistical analysis

**Supported examination types:**
- CT scans (head, chest, abdomen, pelvis, spine, limbs)
- X-rays (chest, abdomen, limbs, dental)
- PET-CT, bone scan, angiography, etc.

### 3. Query Medical Records

Use the `/query` command to query records:

```bash
# Query all records
/query all

# Query biochemical examinations
/query biochemical

# Query imaging examinations
/query imaging

# Query the most recent N records
/query recent 5

# Query by date
/query date 2025-12
/query date 2025-12-31

# Query abnormal indicators
/query abnormal
```

### 4. Multidisciplinary Team Consultation (MDT)

Use the `/consult` command to start a multidisciplinary expert consultation:

```bash
# Analyze all data for consultation
/consult all

# Analyze the most recent N records
/consult recent 5

# Analyze data from a specific date
/consult date 2025-12-31

# Analyze a specific date range
/consult date 2025-12-01 to 2025-12-31

# Auto-analyze (default: most recent 3 records)
/consult
```

**The consultation system will:**
- Automatically identify the relevant specialties (cardiology, endocrinology, gastroenterology, nephrology, etc.)
- Launch multiple specialist subagents in parallel for independent analysis
- Integrate opinions from all specialties and generate a comprehensive consultation report
- Provide prioritized recommendations and a comprehensive management plan

**Supports 9 major specialties:**
- Cardiology — Heart disease, hypertension, dyslipidemia
- Endocrinology — Diabetes, thyroid disease
- Gastroenterology — Liver disease, gastrointestinal disorders
- Nephrology — Kidney disease, electrolyte imbalances
- Hematology — Anemia, coagulation abnormalities
- Pulmonology — Pulmonary infection, pulmonary nodules
- Neurology — Cerebrovascular disease, headache and dizziness
- Oncology — Tumor markers, cancer screening
- General practice — Comprehensive assessment, chronic disease management

### 5. Single-Specialty Consultation

Use the `/specialist` command to consult a specific specialty:

```bash
# View the list of supported specialties
/specialist list

# Consult cardiology
/specialist cardio recent 3

# Consult endocrinology
/specialist endo all

# Consult oncology
/specialist onco date 2025-12-31
```

## Notes

- Basic profile (height, weight, date of birth) must be set before first use
- Ensure examination report images are clear and legible
- Supported image formats: JPG, PNG
- Back up the `data/` directory regularly
- Use YYYY-MM-DD format for all dates
- Radiation doses are for reference only; please consult a physician for specifics
- Check `/radiation status` regularly to stay informed of cumulative exposure

## Expert Consultation System Safety Principles

This system strictly adheres to the following medical safety principles:

### ⚠️ Safety Red Lines
1. **Does not provide specific medication dosages**
2. **Does not directly prescribe drug names**
3. **Does not make life-or-death prognoses**
4. **Does not replace physician diagnosis**

### ✅ What the System Can Do
- Interpret the clinical significance of medical test results
- Identify abnormal indicators and potential risks
- Provide healthy lifestyle advice
- Recommend targeted examinations
- Assist in developing follow-up plans
- Integrate multidisciplinary expert opinions

### ⚠️ Important Disclaimer
- **All analysis reports from this system are for reference only**
- **They do not serve as the basis for medical diagnosis**
- **All clinical decisions require consultation with a qualified physician**
- **In case of emergency, seek medical attention immediately**
