---
description: Manage hypertension monitoring data, assess target organ damage and cardiovascular risk
arguments:
  - name: action
    description: "Action type: record (record blood pressure) / trend (trend analysis) / average (average blood pressure) / history (history records) / status (achievement status) / risk (risk assessment) / target (blood pressure target) / heart (heart assessment) / kidney (kidney assessment) / retina (retinal assessment) / medication (medication management)"
    required: true
  - name: info
    description: Detailed information (blood pressure values, assessment results, etc., in natural language)
    required: false
---

# Hypertension Management

Comprehensive blood pressure monitoring and management to help control blood pressure and reduce cardiovascular risk.

## ⚠️ Medical Safety Statement

**Important: This system is for health monitoring records only and cannot replace professional medical diagnosis and treatment.**

- ❌ Does not provide specific medication dosage adjustment recommendations
- ❌ Does not directly prescribe medications or recommend specific drugs
- ❌ Does not replace physician diagnosis and treatment decisions
- ❌ Does not predict disease prognosis or complications
- ✅ Provides blood pressure monitoring records and trend analysis
- ✅ Provides target organ damage assessment records
- ✅ Provides cardiovascular risk calculation (for reference only)
- ✅ Provides lifestyle recommendations and medical visit reminders

All medication plans and treatment decisions should follow physician guidance.

## Action Types

### 1. Record Blood Pressure - `record`

Record blood pressure measurement data.

**Parameter Description:**
- `info`: Blood pressure information (required), describe in natural language

**Examples:**
```
/bp record 135/85 pulse 78
/bp record 130/80 morning sitting
/bp record 125/78 evening
/bp record 140/90 pulse 82 morning sitting left arm
```

**Supported Information:**
- Blood pressure value: systolic/diastolic (mmHg)
- Heart rate: pulse 78 (beats/min)
- Measurement time: morning/evening or specific time
- Measurement position: sitting/standing/lying
- Measurement arm: left/right

**Execution Steps:**
1. Parse blood pressure values and additional information
2. Generate record ID and timestamp
3. Save to `data/hypertension-tracker.json`
4. Update average blood pressure calculation
5. Output confirmation information

### 2. View Blood Pressure Trend - `trend`

View blood pressure change trends and diurnal rhythm.

**Examples:**
```
/bp trend
/bp trend 7days
/bp trend this month
```

**Output Content:**
- Blood pressure trend chart (text description)
- Diurnal rhythm pattern (dipper/non-dipper/reverse dipper)
- Blood pressure variability
- Achievement rate trend

### 3. Calculate Average Blood Pressure - `average`

Calculate average blood pressure for a specified period.

**Examples:**
```
/bp average
/bp average 7days
/bp average last week
/bp average this month
```

**Output Content:**
- Home blood pressure monitoring average (HBPM)
- Morning average blood pressure
- Evening average blood pressure
- Number of days blood pressure target achieved

### 4. View History Records - `history`

View blood pressure measurement history.

**Examples:**
```
/bp history
/bp history 7
/bp history today
/bp history 2025-06-20
```

### 5. View Achievement Status - `status`

View blood pressure achievement rate and control status.

**Examples:**
```
/bp status
```

**Output Content:**
- Current blood pressure target (<130/80 or <140/90)
- Achievement rate (last 7 days, last 30 days)
- Number of days target achieved
- Control assessment

### 6. Cardiovascular Risk Assessment - `risk`

Calculate 10-year atherosclerotic cardiovascular disease risk (ASCVD).

**Examples:**
```
/bp risk
```

**Output Content:**
- ASCVD risk score (%)
- Risk level (low/moderate/high/very high)
- Main risk factors
- Medical visit recommendations

**Note:** Risk assessment is based on standard calculation formulas, for reference only; please consult a doctor for specific risks.

### 7. View Blood Pressure Target - `target`

View individualized blood pressure management targets.

**Examples:**
```
/bp target
```

**Output Content:**
- Systolic blood pressure target
- Diastolic blood pressure target
- Target basis (age, comorbidities, etc.)
- Lifestyle recommendations

### 8. Heart Assessment Record - `heart`

Record cardiac-related target organ damage assessment.

**Examples:**
```
/bp heart echo normal
/bp heart ecg normal
/bp heart lvh none
```

**Supported Tests:**
- echo: Echocardiogram
- ecg: Electrocardiogram
- lvh: Left ventricular hypertrophy

### 9. Kidney Assessment Record - `kidney`

Record kidney-related target organ damage assessment.

**Examples:**
```
/bp kidney uacr 15
/bp kidney egfr 90
/bp kidney creatinine 85
```

**Supported Indicators:**
- uacr: Urine albumin-to-creatinine ratio (mg/g)
- egfr: Estimated glomerular filtration rate (ml/min/1.73m²)
- creatinine: Serum creatinine (μmol/L)

### 10. Retinal Assessment Record - `retina`

Record retinal hypertensive retinopathy assessment.

**Examples:**
```
/bp retina grade-0
/bp retina grade-1
/bp retina normal
```

**Grading:**
- grade-0: No retinopathy
- grade-1: Mild
- grade-2: Moderate
- grade-3: Severe
- grade-4: Exudative

### 11. Medication Management - `medication`

Manage hypertension-related medications (integrated with medication management system).

**Examples:**
```
/bp medication add amlodipine 5mg once_daily
/bp medication list
/bp medication adherence
```

**Execution Process:**
1. Parse medication information
2. Call `/medication add` command to add medication
3. Add reference record in hypertension-tracker.json
4. Output confirmation information

**Reference Format:**
```json
{
  "medication_id": "med_xxx",
  "added_from": "hypertension_management",
  "added_date": "2025-01-02",
  "indication": "Hypertension"
}
```

## Data Structure

### Blood Pressure Record Structure
```json
{
  "id": "bp_20250102080000001",
  "date": "2025-01-02",
  "time": "08:00",
  "systolic": 135,
  "diastolic": 85,
  "pulse": 78,
  "position": "sitting",
  "measurement_device": "home_monitor",
  "arm": "left",
  "created_at": "2025-01-02T08:00:00.000Z"
}
```

### Target Organ Damage Structure
```json
{
  "left_ventricular_hypertrophy": {
    "status": "none",
    "last_assessment": "2025-01-15",
    "method": "echocardiogram"
  },
  "microalbuminuria": {
    "status": "negative",
    "uacr": 15,
    "reference": "<30",
    "date": "2025-06-10"
  },
  "retinopathy": {
    "grade": "grade_0",
    "last_exam": "2025-03-20"
  },
  "arterial_stiffness": {
    "pwv": 7.5,
    "reference": "<10",
    "date": "2025-02-15"
  }
}
```

## Blood Pressure Classification Reference

| Classification | Systolic (mmHg) | Diastolic (mmHg) |
|------|---------------|---------------|
| Normal blood pressure | <120 | <80 |
| High-normal | 120-139 | 80-89 |
| Hypertension grade 1 | 140-159 | 90-99 |
| Hypertension grade 2 | 160-179 | 100-109 |
| Hypertension grade 3 | ≥180 | ≥110 |

## Blood Pressure Target Reference

**General population:** <130/80 mmHg
**Elderly aged 65 and above:** <140/90 mmHg
**Combined with diabetes/kidney disease:** <130/80 mmHg

## Recommended Frequency for Target Organ Damage Assessment

- **Cardiac ultrasound**: Once every 1-2 years
- **Urinary microalbumin**: Once per year
- **Fundus examination**: Once per year
- **Carotid ultrasound**: Once every 1-2 years

## Lifestyle Recommendations

### Dietary Adjustments
- Limit sodium intake (<5g/day)
- Increase potassium intake (fresh fruits and vegetables)
- Limit alcohol consumption
- DASH dietary pattern

### Exercise Recommendations
- Regular aerobic exercise (150 minutes per week)
- Such as: brisk walking, swimming, cycling
- Avoid strenuous exercise

### Weight Management
- BMI <24 kg/m²
- Waist circumference: men <90cm, women <85cm

### Other Recommendations
- Quit smoking
- Regular sleep schedule
- Reduce mental stress
- Regular blood pressure monitoring

## Medical Visit Recommendations

### Emergency Medical Care (Call 120 Immediately)
- Systolic ≥180 mmHg and diastolic ≥120 mmHg
- Accompanied by chest pain, difficulty breathing, difficulty speaking
- Headache, confusion, vision changes
- Numbness/weakness in face or limbs

### Prompt Medical Care (Within 48 Hours)
- Blood pressure persistently ≥160/100 mmHg
- Worsening target organ damage
- Medication intolerance or significant side effects

### Regular Follow-up
- Hypertension grade 1: Every 3 months
- Hypertension grade 2: Every 2 months
- Hypertension grade 3: Every 1 month

## Error Handling

- **Invalid blood pressure value**: "Blood pressure value should be within normal range (systolic 70-250, diastolic 40-150)"
- **Incomplete information**: "Please provide complete blood pressure information, e.g.: /bp record 135/85"
- **No data**: "No blood pressure records yet, please use /bp record to record blood pressure first"
- **File read failure**: "Unable to read blood pressure data, please check data file"

## Example Usage

```
# Record blood pressure
/bp record 135/85 pulse 78
/bp record 130/80 morning sitting
/bp record 125/78 evening

# View trends and statistics
/bp trend
/bp average
/bp status

# Assessment examinations
/bp risk
/bp heart echo normal
/bp kidney uacr 15
/bp retina grade-0

# Medication management
/bp medication add amlodipine 5mg once_daily
/bp medication list
```

## Notes

- Rest for 5 minutes before measurement
- Avoid coffee, exercise, and smoking for 30 minutes before measurement
- Maintain a quiet environment
- Measure in sitting position with arm at heart level
- Recommend measuring once in the morning and once in the evening
- Note measurement time and position when recording

---

**Disclaimer: This system is for health monitoring records only and does not replace professional medical diagnosis and treatment.**
