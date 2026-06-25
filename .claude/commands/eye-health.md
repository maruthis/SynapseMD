---
description: Record vision exams, eye examinations, eye disease screenings, and eye habit management
arguments:
  - name: action
    description: "Action type: vision (vision record) / iop (eye pressure record) / fundus (fundus exam) / screening (eye disease screening) / habit (eye habits) / status (eye health status) / trend (vision trend) / checkup (exam reminder) / medication (ophthalmic medication)"
    required: true
  - name: info
    description: Detailed information (vision values, exam results, etc., in natural language)
    required: false
---

# Eye Health Management

Comprehensive vision monitoring, eye examination, and eye disease screening management.

## ⚠️ Medical Safety Disclaimer

**Important: This system is for health monitoring and record-keeping only and cannot replace professional medical diagnosis and treatment.**

- ❌ Does not provide specific ophthalmic treatment plans
- ❌ Does not recommend prescription medications or surgical plans
- ❌ Does not diagnose eye diseases or determine prognosis
- ❌ Does not replace professional examination by an ophthalmologist
- ✅ Provides vision monitoring records and trend analysis
- ✅ Provides eye exam records and reminders
- ✅ Provides eye disease screening records (for reference only)
- ✅ Provides eye habit recommendations and medical visit reminders

All ophthalmic diagnoses and treatments should follow the guidance of an ophthalmologist.

## Action Types

### 1. Record Vision Exam - `vision`

Record uncorrected vision, corrected vision, and refractive prescription.

**Parameter description:**
- `info`: Vision information (required), described in natural language

**Examples:**
```
/eye vision left 1.0 right 0.8
/eye vision uncorrected left 0.5 right 0.4
/eye vision corrected left 1.2 right 1.0
/eye vision sphere -3.5 cylinder -0.5 axis 180
/eye vision left sphere -3.5 cylinder -0.5 axis 180 right sphere -4.0
```

**Supported information:**
- Uncorrected visual acuity: 0.1–2.0
- Corrected visual acuity: 0.1–2.0
- Sphere (sphere): −20.0 to +20.0 (negative = myopia, positive = hyperopia)
- Cylinder (cylinder): 0 to −6.0 (astigmatism power)
- Axis: 0–180 degrees

**Execution steps:**
1. Parse vision values and refractive prescription
2. Generate record ID and timestamp
3. Save to `data/eye-health-tracker.json`
4. Update average vision calculation
5. Output confirmation message

### 2. Record Eye Pressure - `iop`

Record intraocular pressure measurements.

**Examples:**
```
/eye iop left 15 right 16
/eye iop 15 16
/eye iop left 15 right 16 Goldman 2025-01-15
/eye iop 14 15 morning
```

**Supported information:**
- Left eye IOP (mmHg)
- Right eye IOP (mmHg)
- Measurement method: Goldmann (gold standard) / non-contact / handheld
- Measurement time: morning / afternoon / evening
- Reference range: 10–21 mmHg

**Execution steps:**
1. Parse IOP values
2. Generate record ID and timestamp
3. Save to `data/eye-health-tracker.json`
4. Update average IOP calculation
5. If IOP > 21, prompt medical advice
6. Output confirmation message

### 3. Record Fundus Exam - `fundus`

Record fundus examination findings.

**Examples:**
```
/eye fundus normal
/eye fundus diabetic_mild
/eye fundus hypertensive_grade_1
/eye fundus amd_drusen
/eye fundus left_normal right_suspect
```

**Supported findings:**
- Normal (normal)
- Diabetic retinopathy (diabetic_mild/moderate/severe/proliferative)
- Hypertensive retinopathy (hypertensive_grade_0/1/2/3/4)
- Age-related macular degeneration (amd_drusen/amd_atrophic/amd_exudative)
- Retinal vein occlusion (vessel_occlusion)
- Other lesion descriptions

**Exam types:**
- Dilated fundus exam (dilated)
- Non-dilated fundus photography (non-dilated)
- OCT examination
- Fluorescein angiography

**Execution steps:**
1. Parse fundus exam results
2. Generate record ID and timestamp
3. Save to `data/eye-health-tracker.json`
4. If abnormalities found, provide medical visit advice
5. Output confirmation message

### 4. Eye Disease Screening - `screening`

Record results of various eye disease screenings.

**Examples:**
```
/eye screening glaucoma negative
/eye screening cataract grade_1
/eye screening amd early
/eye screening diabetic_retinopathy mild
/eye screening dry_eye moderate
```

**Screening types:**

#### Glaucoma (glaucoma)
- negative: Negative
- suspect: Suspected
- early: Early stage
- moderate: Moderate stage
- advanced: Advanced stage

#### Cataract (cataract)
- none: No cataract
- grade_1: Mild
- grade_2: Moderate
- grade_3: Severe
- mature: Mature stage

#### Macular Degeneration (AMD)
- none: No lesion
- early: Early stage (drusen)
- intermediate: Intermediate stage
- late: Late stage (geographic atrophy or neovascularization)

#### Diabetic Retinopathy
- none: No lesion
- mild: Mild non-proliferative
- moderate: Moderate non-proliferative
- severe: Severe non-proliferative
- proliferative: Proliferative

#### Dry Eye (dry_eye)
- none: No dry eye
- mild: Mild
- moderate: Moderate
- severe: Severe

**Execution steps:**
1. Parse screening type and result
2. Update corresponding screening status
3. Calculate next screening date
4. Save to `data/eye-health-tracker.json`
5. If screening is positive, provide medical visit advice
6. Output confirmation message

### 5. Record Eye Habits - `habit`

Record daily eye habits and environment.

**Examples:**
```
/eye habit screen 4hours outdoor 1hour
/eye habit break_20_20_20 yes
/eye habit distance 50cm lighting good
/eye habit screen_6hours outdoor_30min distance_40cm
```

**Supported records:**
- Screen usage time (screen): hours per day
- Outdoor activity time (outdoor): hours per day
- 20-20-20 rule compliance (break_20_20_20): yes / no / partial
- Viewing distance (distance): centimeters (recommended ≥ 40 cm)
- Lighting conditions (lighting): good / adequate / poor
- Other habit descriptions

**The 20-20-20 Rule:**
- Every 20 minutes of screen use
- Look at something 20 feet (~6 meters) away
- For 20 seconds

**Execution steps:**
1. Parse eye habit information
2. Update eye habit records
3. Provide personalized recommendations
4. Save to `data/eye-health-tracker.json`
5. Output confirmation message and recommendations

### 6. View Eye Health Status - `status`

View a comprehensive eye health assessment report.

**Examples:**
```
/eye status
```

**Output includes:**
- Most recent vision exam results
- Most recent IOP measurement
- Fundus exam status
- Screening completion status
- Eye habit assessment
- Overall health score
- Priority improvement recommendations

### 7. View Vision Trend - `trend`

View vision change trends.

**Examples:**
```
/eye trend
/eye trend 6months
/eye trend 1year
```

**Output includes:**
- Vision change trend chart (text description)
- Myopia prescription changes
- IOP change trend
- Visual acuity progression speed assessment
- Warning signs requiring medical attention

### 8. Exam Reminders - `checkup`

View and set ophthalmic exam reminders.

**Examples:**
```
/eye checkup
/eye checkup set routine 2025-06-15
/eye checkup set glaucoma 2025-12-15
```

**Exam types and recommended frequency:**

#### Routine Eye Exam
- **Adults (18–40 years)**: Every 2 years
- **Adults (40–60 years)**: Every 1–2 years
- **Adults (> 60 years)**: Every year
- **Children/adolescents**: Every year

#### Glaucoma Screening
- **High-risk individuals** (family history, high myopia): Every year
- **General population**: Every 2–3 years after age 40; every year after age 60

#### Diabetic Retinopathy Exam
- **Type 1 diabetes**: Starting 5 years after onset, every year
- **Type 2 diabetes**: Immediately after diagnosis, every year
- **Gestational diabetes**: During or before pregnancy

**Output includes:**
- Next exam date
- Exam checklist
- Overdue exam reminders
- Appointment recommendations

### 9. Ophthalmic Medication Management - `medication`

Manage ophthalmic medications (integrated with the medication management system).

**Examples:**
```
/eye medication add artificial_tears 3_times_daily
/eye medication add sodium_hyaluronate_eye_drops morning_and_evening
/eye medication add atropine_eye_drops once_nightly (myopia_control)
/eye medication list
/eye medication interaction
```

**Execution flow:**
1. Parse medication information
2. Call `/medication add` command to add medication
3. Add reference record in eye-health-tracker.json
4. Output confirmation message

**Reference format:**
```json
{
  "medication_id": "med_xxx",
  "added_from": "eye_health_management",
  "added_date": "2025-01-02",
  "indication": "dry_eye"
}
```

## Data Structure

### Vision Record Structure
```json
{
  "id": "vision_20250102000001",
  "date": "2025-01-02",
  "left_eye": {
    "uncorrected_va": 0.5,
    "corrected_va": 1.0,
    "sphere": -3.50,
    "cylinder": -0.50,
    "axis": 180
  },
  "right_eye": {
    "uncorrected_va": 0.4,
    "corrected_va": 1.0,
    "sphere": -4.00,
    "cylinder": -0.75,
    "axis": 175
  },
  "exam_type": "routine",
  "exam_method": "snellen_chart",
  "notes": "",
  "created_at": "2025-01-02T00:00:00.000Z"
}
```

### IOP Record Structure
```json
{
  "id": "iop_20250102000001",
  "date": "2025-01-02",
  "time": "10:00",
  "left_iop": 15,
  "right_iop": 16,
  "measurement_method": "goldmann_applanation_tonometer",
  "reference_range": "10-21",
  "notes": "",
  "created_at": "2025-01-02T10:00:00.000Z"
}
```

### Fundus Exam Structure
```json
{
  "id": "fundus_20250102000001",
  "date": "2025-01-02",
  "exam_type": "dilated_fundus_exam",
  "findings": {
    "left_eye": "normal",
    "right_eye": "normal",
    "overall": "normal"
  },
  "specific_findings": {
    "optic_disc": "normal",
    "retina": "normal",
    "vessels": "normal",
    "macula": "normal"
  },
  "comments": "",
  "examined_by": "",
  "created_at": "2025-01-02T00:00:00.000Z"
}
```

## Visual Acuity Classification Reference

| Uncorrected VA | Assessment | Estimated Myopia (Reference) |
|----------------|------------|------------------------------|
| 1.0–1.5 | Normal | 0 ~ −0.5D |
| 0.8–0.9 | Mild decrease | −0.5D ~ −1.5D |
| 0.4–0.7 | Moderate decrease | −1.5D ~ −3.0D |
| 0.1–0.3 | Severe decrease | −3.0D ~ −6.0D |
| < 0.1 | Very severe decrease | > −6.0D (high myopia) |

## IOP Reference Values

| Category | IOP (mmHg) |
|----------|------------|
| Normal IOP | 10–21 |
| Elevated IOP | 22–25 |
| Suspected glaucoma | 26–30 |
| Likely glaucoma | > 30 |

## Recommended Screening Frequency

### Routine Adult Exams
- Age 18–40: Every 2 years
- Age 40–60: Every 1–2 years
- Age > 60: Every year

### High-Risk Individuals
- Diabetic patients: Annual fundus exam
- Hypertensive patients: Annual fundus exam
- High myopia (> −6.0D): Annual fundus exam
- Family history of glaucoma: Annual IOP and visual field exam
- Adults over 40: Annual IOP exam

## Eye Care Recommendations

### Screen Usage Recommendations
- Limit daily screen time to 4–6 hours
- Follow the 20-20-20 rule
- Maintain appropriate viewing distance (≥ 40 cm)
- Screen top should be slightly below eye level

### Outdoor Activity
- At least 1–2 hours of outdoor activity per day
- Natural light helps prevent myopia progression
- Avoid direct strong light into eyes

### Lighting Environment
- Use soft, even lighting
- Avoid glare and reflections
- Match ambient light to screen brightness
- When reading, light should come from the non-dominant hand side

### Dietary Recommendations
- Foods rich in vitamin A (carrots, spinach)
- Foods rich in omega-3 (deep-sea fish)
- Foods rich in lutein (kale, broccoli)
- Foods rich in vitamin C (citrus fruits)

## When to Seek Medical Attention

### Emergency (Seek care immediately)
- Sudden vision loss or visual field defect
- Severe eye pain
- Sudden onset of flashing lights or increased floaters
- Vision changes after eye trauma
- Acute loss of visual field

### Seek Care Promptly (Within 48 hours)
- Persistent vision decline
- IOP persistently > 25 mmHg
- Abnormal fundus exam findings
- Positive eye disease screening
- Persistent red eye or eye pain

### Regular Follow-Up
- Routine exams: Follow frequency recommendations above
- After new glasses: Follow up in 1–2 weeks
- After starting medication: Follow up per doctor's instructions
- After surgery: Follow up per doctor's orders

## Error Handling

- **Invalid vision value**: "Vision value should be in the range 0.1–2.0"
- **Invalid IOP value**: "IOP value should be in the range 5–50 mmHg"
- **Invalid refractive value**: "Prescription should be within reasonable range (sphere −20 to +20, cylinder 0 to −6)"
- **Incomplete information**: "Please provide complete exam information"
- **No data**: "No relevant records found; please record data first"
- **File read failure**: "Unable to read eye health data; please check the data file"

## Example Usage

```
# Record vision exam
/eye vision left 1.0 right 0.8
/eye vision sphere -3.5 cylinder -0.5 axis 180

# Record eye pressure
/eye iop left 15 right 16

# Record fundus exam
/eye fundus normal

# Eye disease screening
/eye screening glaucoma negative
/eye screening cataract grade_1

# Record eye habits
/eye habit screen 4hours outdoor 1hour

# View status and trends
/eye status
/eye trend

# Exam reminders
/eye checkup

# Ophthalmic medication
/eye medication add artificial_tears 3_times_daily
```

## Notes

- Vision exams should be performed under good lighting
- IOP measurement should not be taken immediately after pressure on the eyeball
- Fundus exam is recommended with pupil dilation (except for suspected angle-closure glaucoma)
- Screening results are for reference only and cannot replace a full ophthalmic exam
- Eye habits must be maintained consistently over time to be effective
- Children's and adolescents' vision requires special attention

## Integration with Other Systems

### Hypertension Fundus Assessment
```bash
# Record fundus assessment in the hypertension system
/bp retina grade-0
# Can be linked to detailed exam records in the eye health system
```

### Diabetic Retinopathy
```bash
# Record retinopathy in the diabetes system
/diabetes retinopathy mild
# Can be linked to fundus exam in the eye health system
```

---

**Command version**: v1.0
**Creation date**: 2026-01-06
**Maintainer**: SynapseMD
