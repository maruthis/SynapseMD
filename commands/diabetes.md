---
description: Manage diabetes blood glucose monitoring, HbA1c tracking, and complication screening
arguments:
  - name: action
    description: "Action type: record (log blood glucose) / hba1c (glycated hemoglobin) / trend (trend analysis) / tir (time in range) / hypo (hypoglycemic events) / screening (complication screening) / target (blood glucose targets) / achievement (target attainment) / medication (medication management)"
    required: true
  - name: info
    description: Detailed information (blood glucose value, HbA1c value, assessment results, etc., in natural language)
    required: false
---

# Diabetes Management

Comprehensive blood glucose monitoring and diabetes management to help control blood sugar and prevent complications.

## ⚠️ Medical Safety Statement

**Important: This system is for health monitoring and record-keeping only. It cannot replace professional medical diagnosis and treatment.**

- ❌ Does not provide specific medication dosage adjustment recommendations
- ❌ Does not directly prescribe medications or recommend specific drugs
- ❌ Does not replace physician diagnosis and treatment decisions
- ❌ Does not predict disease prognosis or complication occurrence
- ✅ Provides blood glucose monitoring records and trend analysis (for reference only)
- ✅ Provides HbA1c tracking and target attainment status
- ✅ Provides complication screening records and reminders
- ✅ Provides hypoglycemic event records and analysis
- ✅ Provides lifestyle recommendations and medical visit reminders

All medication plans and treatment decisions should follow physician guidance.

## Action Types

### 1. Record Blood Glucose - `record`

Record blood glucose measurement data.

**Parameter description:**
- `info`: Blood glucose information (required), described in natural language

**Examples:**
```
/glucose record fasting 6.5
/glucose record postprandial 8.2
/glucose record bedtime 7.2
/glucose record random 9.5
/glucose record fasting 6.8 before breakfast
```

**Supported blood glucose types:**
- **fasting**: Fasting blood glucose (target: 4.4–7.0 mmol/L)
- **postprandial** / **postprandial_2h**: 2-hour postprandial blood glucose (target: <10.0 mmol/L)
- **bedtime**: Bedtime blood glucose (target: 6.0–9.0 mmol/L)
- **random**: Random blood glucose

**Execution steps:**
1. Parse blood glucose value and measurement type
2. Generate record ID and timestamp
3. Save to `data/diabetes-tracker.json`
4. Update blood glucose statistics
5. Output confirmation message

### 2. Record HbA1c - `hba1c`

Record glycated hemoglobin test results.

**Examples:**
```
/glucose hba1c 6.8
/glucose hba1c 7.2 2025-06-15
/glucose hba1c history
```

**Execution steps:**
1. Parse HbA1c value
2. Calculate change from previous test result
3. Save to history records
4. Determine whether target is met (target: <7.0%)
5. Output trend analysis

### 3. View Blood Glucose Trend - `trend`

View blood glucose change trends.

**Examples:**
```
/glucose trend
/glucose trend 7days
/glucose trend this month
```

**Output content:**
- Blood glucose trend chart (text description)
- Intraday blood glucose fluctuations
- Hypoglycemic / hyperglycemic events
- Target attainment status

### 4. View TIR - `tir`

View glucose Time in Range (TIR).

**Examples:**
```
/glucose tir
/glucose tir 14days
```

**Output content:**
- TIR percentage (target: >70%)
- Time within target range (hours)
- Time above range (hours)
- Time below range (hours)
- Measurement period

**TIR definitions (general diabetes patients):**
- Target range: 3.9–10.0 mmol/L
- TIR target: >70%
- Above range: <10%
- Below range: <4%

### 5. Record Hypoglycemic Events - `hypo`

Record hypoglycemic event details.

**Examples:**
```
/glucose hypo 3.4 sweating
/glucose hypo 2.8 confusion took glucose
/glucose hypo 3.0 palpitations tremor juice
/glucose hypo history
```

**Hypoglycemia classification:**
- **Level 1**: Blood glucose <3.9 mmol/L but ≥3.0 mmol/L
- **Level 2**: Blood glucose <3.0 mmol/L
- **Level 3**: Severe hypoglycemia requiring assistance from others

**Supported symptom records:**
- sweating
- palpitations
- tremor
- hunger
- confusion
- dizziness

**Treatment recommendations:**
```
⚠️ Hypoglycemia detected (<3.9 mmol/L)

Immediate treatment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Take 15g of fast-acting carbohydrates
   • 3–5 glucose tablets
   • 150 ml fruit juice or sugary drink
   • 1 tablespoon honey

2. Wait 15 minutes and retest

3. If still below 3.9 mmol/L, repeat step 1

4. Once blood glucose returns to normal, if more than 1 hour
   until the next meal, eat a small amount of long-acting carbohydrates
```

### 6. Complication Screening Records - `screening`

Record diabetes complication screening results.

**Examples:**
```
/glucose screening retina none
/glucose screening kidney uacr 45 egfr 78
/glucose screening nerve normal
/glucose screening foot normal
/glucose screening retina mild 2025-06-15
```

**Supported screening types:**

#### Retinopathy Screening - `retina`
```
/glucose screening retina none
/glucose screening retina mild
/glucose screening retina moderate
/glucose screening retina severe
/glucose screening retina proliferative
```

#### Diabetic Nephropathy Screening - `kidney`
```
/glucose screening kidney normal
/glucose screening kidney microalbuminuria uacr 45 egfr 78
/glucose screening kidney macroalbuminuria uacr 300 egfr 55
```

**CKD staging:**
- G1: eGFR ≥90 (normal)
- G2: eGFR 60–89 (mildly decreased)
- G3a: eGFR 45–59 (mildly to moderately decreased)
- G3b: eGFR 30–44 (moderately to severely decreased)
- G4: eGFR 15–29 (severely decreased)
- G5: eGFR <15 (kidney failure)

**Albuminuria staging:**
- A1: UACR <30 (normal)
- A2: UACR 30–300 (microalbuminuria)
- A3: UACR >300 (macroalbuminuria)

#### Neuropathy Screening - `nerve`
```
/glucose screening nerve normal
/glucose screening nerve abnormal
/glucose screening neuropathy monofilament normal
```

#### Diabetic Foot Screening - `foot`
```
/glucose screening foot normal
/glucose screening foot low_risk
/glucose screening foot high_risk ulcer wagner 1
```

**Wagner grading:**
- Grade 0: No ulcer
- Grade 1: Superficial ulcer
- Grade 2: Deep ulcer
- Grade 3: Deep ulcer with abscess / osteomyelitis
- Grade 4: Localized gangrene
- Grade 5: Full-foot gangrene

### 7. View Blood Glucose Targets - `target`

View individualized blood glucose management targets.

**Examples:**
```
/glucose target
```

**Output content:**
- Fasting blood glucose target
- 2-hour postprandial blood glucose target
- Bedtime blood glucose target
- HbA1c target
- TIR target
- Individualization basis

**General blood glucose targets:**
| Indicator | General adults | Elderly / frail | Gestational diabetes |
|-----------|---------------|-----------------|----------------------|
| Fasting / pre-meal | 4.4–7.0 | 5.0–8.0 | 3.3–5.3 |
| 2h postprandial | <10.0 | <11.0 | 6.7–7.8 |
| Bedtime | 6.0–9.0 | 6.0–10.0 | 6.0–7.8 |
| HbA1c | <7.0% | <8.0% | <6.0% |
| TIR | >70% | >50% | >70% |

### 8. View Target Attainment - `achievement`

View blood glucose target attainment rate and control status.

**Examples:**
```
/glucose achievement
/glucose achievement 30days
```

**Output content:**
- HbA1c target attainment
- Fasting blood glucose attainment rate
- Postprandial blood glucose attainment rate
- TIR attainment status
- Control evaluation

### 9. Medication Management - `medication`

Manage diabetes-related medications (integrated medication management system).

**Examples:**
```
/glucose medication add metformin 500mg three times daily after meals
/glucose medication list
/glucose medication adherence
```

**Execution process:**
1. Parse medication information
2. Call `/medication add` command to add medication
3. Add reference record in diabetes-tracker.json
4. Output confirmation message

## Data Structures

### Blood Glucose Record Structure
```json
{
  "id": "glu_20250620070000001",
  "date": "2025-06-20",
  "time": "07:00",
  "type": "fasting",
  "value": 6.5,
  "unit": "mmol/L",
  "notes": "",
  "created_at": "2025-06-20T07:00:00.000Z"
}
```

### HbA1c Record Structure
```json
{
  "date": "2025-06-15",
  "value": 6.8,
  "unit": "%",
  "change_from_previous": -0.3,
  "created_at": "2025-06-15T00:00:00.000Z"
}
```

### Hypoglycemic Event Structure
```json
{
  "id": "hypo_20250618153000001",
  "date": "2025-06-18",
  "time": "15:30",
  "value": 3.4,
  "severity": "level_1",
  "symptoms": ["sweating", "palpitations"],
  "treatment": "glucose_tablets",
  "resolved": true,
  "created_at": "2025-06-18T15:30:00.000Z"
}
```

### Complication Screening Structure
```json
{
  "retinopathy": {
    "status": "none",
    "last_exam": "2025-03-20",
    "next_exam": "2026-03-20"
  },
  "nephropathy": {
    "status": "microalbuminuria",
    "uacr": 45,
    "egfr": 78,
    "ckd_stage": "G2A2",
    "last_assessment": "2025-06-10"
  },
  "neuropathy": {
    "status": "none",
    "monofilament_test": "normal",
    "last_assessment": "2025-06-15"
  },
  "foot": {
    "status": "low_risk",
    "pulses_present": true,
    "ulcer": false,
    "wagner_grade": 0,
    "last_assessment": "2025-06-15"
  }
}
```

## Blood Glucose Control Targets

### Adults with Type 2 Diabetes
- **HbA1c**: <7.0%
- **Fasting blood glucose**: 4.4–7.0 mmol/L
- **2h postprandial blood glucose**: <10.0 mmol/L
- **TIR**: >70%

### Elderly / Frail Patients
- **HbA1c**: <8.0%
- **Fasting blood glucose**: 5.0–8.0 mmol/L
- **2h postprandial blood glucose**: <11.0 mmol/L
- **TIR**: >50%

### Gestational Diabetes
- **Fasting blood glucose**: 3.3–5.3 mmol/L
- **1h postprandial blood glucose**: <7.8 mmol/L
- **2h postprandial blood glucose**: 6.7–7.8 mmol/L
- **HbA1c**: <6.0%

## Complication Screening Frequency Recommendations

### Retinopathy
- **At diagnosis**: Dilated fundus examination
- **No lesions**: Every 1–2 years
- **With lesions**: Every 6–12 months

### Diabetic Nephropathy
- **Annual check**: UACR, eGFR, serum creatinine
- **Abnormal findings**: Every 3–6 months

### Neuropathy
- **Annual check**: 10g monofilament test, nerve conduction velocity

### Diabetic Foot
- **Every visit**: Foot examination
- **High risk**: Every 1–3 months

## Hypoglycemia Management Process

### Mild Hypoglycemia (Blood glucose 3.0–3.9 mmol/L)
1. Stop activity immediately
2. Take 15g of fast-acting carbohydrates
3. Retest blood glucose after 15 minutes
4. If still low, repeat step 2

### Severe Hypoglycemia (Blood glucose <3.0 mmol/L or loss of consciousness)
1. **Do not** feed orally (risk of choking)
2. Call emergency services immediately or go to hospital
3. Physician will administer intravenous glucose or glucagon injection
4. Monitor blood glucose until consciousness is restored

## Lifestyle Recommendations

### Dietary Management
- Regular meals at consistent times and portions
- Control total caloric intake, maintain ideal body weight
- Choose low glycemic index (GI) foods
- Increase dietary fiber intake
- Limit simple sugar intake

### Exercise Recommendations
- Regular exercise (150 minutes of moderate intensity per week)
- Best time to exercise: 1–2 hours after meals
- Avoid exercising on an empty stomach (to prevent hypoglycemia)
- If bedtime blood glucose <7.0 mmol/L, have a bedtime snack

### Weight Management
- BMI <24 kg/m²
- Waist circumference: men <90 cm, women <85 cm
- Weight loss of 5–10% can significantly improve blood glucose

### Other Recommendations
- Quit smoking and limit alcohol
- Maintain regular sleep schedule
- Monitor blood glucose regularly
- Daily foot care

## When to Seek Medical Attention

### Emergency (Call 911 / Emergency Services Immediately)
- Severe hypoglycemia (loss of consciousness, coma)
- Diabetic ketoacidosis (nausea, vomiting, abdominal pain, deep rapid breathing)
- Hyperosmolar hyperglycemic state (severe dehydration, altered consciousness)
- Infection with fever and blood glucose >16.7 mmol/L

### Urgent Medical Attention (Within 48 Hours)
- Blood glucose persistently >16.7 mmol/L
- Frequent hypoglycemic episodes
- Worsening complication symptoms
- Obvious medication side effects

### Regular Follow-up
- **Every 3 months**: HbA1c, lipids, kidney function
- **Annually**: Fundus examination, neuropathy screening, foot examination
- **Every 6 months**: Complication assessment

## Monitoring Frequency Recommendations

### Oral Hypoglycemic Agents
- **3–4 days per week**: Fasting + 2h postprandial (alternating)
- **Once per month**: 3-day blood glucose profile (fasting, 2h after three meals, bedtime)

### Insulin Therapy
- **Daily**: Fasting + 2h after three meals + bedtime (at least 4 times)
- **Every 2 weeks**: Full-day blood glucose profile (7 times)

### Well-Controlled Blood Glucose
- **2–3 days per week**: Fasting + 2h postprandial
- **Every 3 months**: 3 consecutive days blood glucose profile

## Error Handling

- **Invalid blood glucose value**: "Blood glucose value should be within normal range (1.0–30.0 mmol/L)"
- **Incomplete information**: "Please provide complete blood glucose information, e.g.: /glucose record fasting 6.5"
- **No data**: "No blood glucose records found. Please use /glucose record to log blood glucose first"
- **File read failure**: "Unable to read blood glucose data, please check the data file"

## Example Usage

```
# Record blood glucose
/glucose record fasting 6.5
/glucose record postprandial 8.2
/glucose record bedtime 7.2

# HbA1c management
/glucose hba1c 6.8
/glucose hba1c history

# View trends and statistics
/glucose trend
/glucose tir
/glucose achievement
/glucose target

# Hypoglycemia management
/glucose hypo 3.4 sweating
/glucose hypo history

# Complication screening
/glucose screening retina none
/glucose screening kidney uacr 45
/glucose screening nerve normal
/glucose screening foot normal

# Medication management
/glucose medication add metformin 500mg three times daily after meals
/glucose medication list
```

## Notes

- Wash and dry hands before testing blood glucose
- Avoid squeezing the finger (affects results)
- Calibrate glucometer regularly
- Record measurement time and related factors (e.g., exercise, diet)
- Note different blood glucose targets for different time periods
- Share blood glucose records with your doctor regularly

---

**Disclaimer: This system is for health monitoring and record-keeping only. It does not replace professional medical diagnosis and treatment.**
