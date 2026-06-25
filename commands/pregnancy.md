---
description: Manage pregnancy health records and prenatal care plans
arguments:
  - name: action
    description: "Action type: start/checkup/symptom/weight/vital/status/next-checkup/type(multiple pregnancy setup)/fetal(fetal information)"
    required: true
  - name: info
    description: Pregnancy information (last menstrual period date, prenatal checkup results, symptom description, etc., natural language description)
    required: false
---

# Pregnancy Management

Full-cycle pregnancy tracking and management, from pre-conception to delivery, providing comprehensive pregnancy health monitoring and management features.

**✨ New feature: Support for multiple pregnancy tracking** - Can track singleton, twin, triplet, and quadruplet pregnancies

## Action Types

### 1. Start Pregnancy Record - `start`

Initialize pregnancy records, calculate due date and prenatal care plan.

**Parameter description:**
- `info`: Last menstrual period (LMP) date (required), format YYYY-MM-DD or natural language

**Examples:**
```
/pregnancy start 2025-01-01
/pregnancy start January 1st this year
/pregnancy start last month January 1st
/pregnancy start 2025-01-01 ultrasound May 15  # Ultrasound correction
```

**Execution steps:**

#### 1. Parse input information

Extract from natural language:
- **Last menstrual period date (LMP)**: Exact date
- **Ultrasound correction date** (optional): Due date confirmed by ultrasound
- **Multiple pregnancy** (optional): twins, triplets

#### 2. Validate input

**Check items:**
- LMP date cannot be a future date
- LMP should be within the past 10 months (avoid outdated data)
- If there is an active pregnancy, prompt to end it first

**Error handling:**
```
⚠️ Active pregnancy record already exists

Current pregnancy: LMP January 1, 2025, due date October 8, 2025
Note: Please complete the current pregnancy before starting a new record
```

#### 3. Calculate due date and gestational weeks

**Due date calculation (Naegele's rule):**
- Due date = LMP + 280 days (40 weeks)
- If ultrasound correction: Use ultrasound confirmed date

**Current gestational week calculation:**
- Gestational week = floor((today - LMP) / 7)
- Gestational day = (today - LMP) % 7

**Pregnancy stages:**
- First trimester: weeks 1-13
- Second trimester: weeks 14-27
- Third trimester: weeks 28-42

**Confidence assessment:**
- High confidence: Ultrasound corrected
- Medium confidence: LMP calculation only
- Low confidence: LMP uncertain

#### 4. Generate prenatal care plan

**Standard prenatal care schedule:**

| Gestational Week | Examination | Preparation |
|-----------------|-------------|-------------|
| Week 12 | NT scan (first trimester screening) | Full bladder required |
| Week 16 | Quad screen / NIPT | Fasting blood draw |
| Week 20 | Anatomy ultrasound (anomaly scan) | Appointment required |
| Week 24 | Glucose tolerance test (GTT) | Fasting, bring glucose drink |
| Week 28 | Routine prenatal | Check blood pressure, weight |
| Week 32 | Routine prenatal | Check fetal position |
| Week 34 | Routine prenatal | Non-stress test |
| Week 36 | Routine prenatal | Non-stress test |
| Week 37 | Weekly prenatal | Until delivery |
| Week 38 | Weekly prenatal | Monitor fetal movement |
| Week 39 | Weekly prenatal | Assess delivery method |
| Week 40 | Weekly prenatal | Monitor post-term pregnancy |

#### 5. Create pregnancy record

**Generate pregnancy_id**: `pregnancy_YYYYMMDD`

**Pregnancy data structure:**
```json
{
  "pregnancy_id": "pregnancy_20250101",
  "lmp_date": "2025-01-01",
  "due_date": "2025-10-08",
  "due_date_confidence": "medium",
  "corrected_by_ultrasound": false,
  "ultrasound_correction_date": null,

  "current_week": 0,
  "current_day": 0,
  "current_trimester": "first",
  "days_passed": 0,
  "days_remaining": 280,
  "progress_percentage": 0,

  "multi_pregnancy": {
    "pregnancy_type": "singleton",
    "fetal_count": 1,
    "detection_method": "manual",
    "detection_confidence": "confirmed",
    "fetal_profiles": [
      {
        "baby_id": "A",
        "estimated_weight": null,
        "position": null,
        "heart_rate": null,
        "amniotic_fluid_index": null,
        "growth_percentile": null,
        "notes": ""
      }
    ],
    "special_considerations": [],
    "adjusted_due_date": null,
    "adjusted_delivery_week": 40
  },

  "prenatal_checks": [
    {
      "check_id": "check_001",
      "week": 12,
      "check_type": "NT scan",
      "check_type_en": "NT_scan",
      "scheduled_date": "2025-03-25",
      "completed": false,
      "results": {},
      "notes": "",
      "preparation": "Full bladder required"
    },
    {
      "check_id": "check_002",
      "week": 16,
      "check_type": "Quad screen",
      "check_type_en": "triple_test",
      "scheduled_date": "2025-04-22",
      "completed": false,
      "results": {},
      "notes": "",
      "preparation": "Fasting blood draw"
    }
    // ... other prenatal check items
  ],

  "symptoms": {
    "nausea": {
      "present": false,
      "severity": null,
      "frequency": null,
      "triggers": [],
      "relief_methods": []
    },
    "fatigue": {
      "present": false,
      "severity": null
    },
    "edema": {
      "present": false,
      "severity": null
    }
  },

  "weight_tracking": [],

  "blood_pressure": [],

  "fetal_movement": {
    "tracking_started": false,
    "start_week": 28,
    "movements": []
  },

  "contractions": [],

  "nutrition_plan": {
    "folic_acid": {
      "dose": "400μg",
      "frequency": "daily",
      "started": null,
      "adherence": null
    },
    "iron": {
      "dose": null,
      "frequency": null,
      "started": null
    },
    "calcium": {
      "dose": null,
      "frequency": null,
      "started": null
    },
    "dha": {
      "dose": null,
      "frequency": null,
      "started": null
    }
  },

  "medication_safety_checks": [],

  "risk_factors": [],

  "notes": "",
  "completed": false,
  "delivery_date": null,
  "delivery_outcome": null,

  "metadata": {
    "created_at": "2025-01-01T00:00:00.000Z",
    "last_updated": "2025-01-01T00:00:00.000Z"
  }
}
```

#### 6. Save data file

**Main file**: `data/pregnancy-tracker.json`
```json
{
  "current_pregnancy": { /* above data structure */ },
  "pregnancy_history": [],
  "statistics": {
    "total_pregnancies": 1,
    "current_pregnancy_week": 0
  }
}
```

**Detailed records**: `data/pregnancy-records/YYYY-MM/YYYY-MM-DD_pregnancy-record.json`

#### 7. Output confirmation

```
✅ Pregnancy record created

Pregnancy information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Last menstrual period: January 1, 2025
Due date: October 8, 2025
Current gestational week: 0 weeks
Pregnancy stage: First trimester

Due date confidence: Medium (based on LMP calculation)
━━━━━━━━━━━━━━━━━━━━━━━━━━

Next prenatal checkup:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 12 NT scan - March 25, 2025 (84 days away)

Preparation: Full bladder required

Prenatal care plan overview:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 12: NT scan
Week 16: Quad screen/NIPT
Week 20: Anatomy ultrasound (anomaly scan)
Week 24: Glucose tolerance test
Week 28: Routine prenatal
Weeks 32-36: Every 2 weeks
Weeks 37-40: Every week

💡 Nutritional recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Folic acid: 400-800μg/day (3 months before pregnancy to first trimester)
• Iron: Supplement in second and third trimesters (per physician's advice)
• Calcium: 1000-1200mg/day (throughout pregnancy)
• DHA: 200-300mg/day (throughout pregnancy)

⚠️ Important disclaimer:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is only for pregnancy health tracking and cannot replace professional prenatal care.

Please attend all prenatal checkups on time. Seek medical care promptly for any abnormalities:
• Vaginal bleeding
• Abdominal pain
• Severe headache
• Vision changes
• Abnormal fetal movement

Due date calculation may have errors; ultrasound examination takes precedence.

Data saved to: data/pregnancy-records/2025-01/2025-01-01_pregnancy-record.json
```

---

### 2. Record Prenatal Checkup - `checkup`

Record prenatal checkup results.

**Parameter description:**
- `info`: Prenatal checkup information (required)
  - Gestational week: week 12, 12w
  - Checkup type: NT, quad screen, anatomy scan, glucose tolerance, routine
  - Results: normal, abnormal, low risk, high risk, numerical values

**Examples:**
```
/pregnancy checkup week 12 NT normal
/pregnancy checkup week 16 quad-screen low-risk
/pregnancy checkup week 20 anatomy-scan all-normal
/pregnancy checkup week 24 glucose-tolerance 7.5 8.2 6.8  # GTT values
/pregnancy checkup week 28 routine bp 120/70 weight 65kg
```

**Execution steps:**

#### 1. Parse prenatal checkup information

**Extract information:**
- **Gestational week**: number + "week"/"w"
- **Checkup type**:
  - NT / NT scan / first trimester screening
  - Quad screen / Down syndrome screening / triple_test
  - Anatomy scan / anomaly scan / anatomy ultrasound
  - Glucose tolerance / OGTT / glucose tolerance test
  - Routine / regular
- **Results**:
  - Normal: normal, pass, low risk
  - Abnormal: abnormal, high risk
  - Numerical values: extract directly

#### 2. Validate input

**Check items:**
- Whether gestational week is in reasonable range (0-42 weeks)
- Whether checkup type is recognized
- Whether there is an active pregnancy

#### 3. Update prenatal checkup records

**Find and update the corresponding checkup item:**
```json
{
  "check_id": "check_001",
  "week": 12,
  "check_type": "NT scan",
  "scheduled_date": "2025-03-25",
  "completed": true,
  "completed_at": "2025-03-25T14:30:00.000Z",
  "results": {
    "status": "normal",
    "nt_measurement": "1.8mm",
    "notes": "NT value normal"
  },
  "notes": ""
}
```

**Glucose tolerance test result format:**
```json
{
  "check_type": "Glucose tolerance test",
  "results": {
    "fasting_glucose": 5.3,  // Fasting
    "one_hour": 7.5,         // 1 hour
    "two_hour": 6.8,         // 2 hours
    "diagnosis": "normal"    // normal/gestational diabetes
  }
}
```

**Quad screen result format:**
```json
{
  "check_type": "Quad screen",
  "results": {
    "risk_category": "low_risk",  // low_risk/high_risk
    "t21_risk": "1:1000",
    "t18_risk": "1:50000",
    "ntd_risk": "low"
  }
}
```

#### 4. Result interpretation and alerts

**Normal results:**
- Confirm record
- Remind of next prenatal checkup

**Abnormal result alerts:**
```
⚠️ Abnormal prenatal checkup result

Checkup item: Quad screen (week 16)
Result: High risk (Trisomy 21 risk 1:50)

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏥 Immediately consult prenatal physician
🔬 NIPT or amniocentesis recommended
📋 Don't panic; high risk does not mean confirmed diagnosis

Next prenatal checkup:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Please confirm next prenatal checkup time with physician
```

**Glucose tolerance abnormality (gestational diabetes):**
```
⚠️ Glucose tolerance test abnormality

Fasting glucose: 5.3 mmol/L (normal <5.1)
1-hour glucose: 10.5 mmol/L (normal <10.0)
2-hour glucose: 8.8 mmol/L (normal <8.5)

Diagnosis: Gestational diabetes

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏥 Immediately consult a dietitian
📊 Control diet, monitor blood sugar
🏃 Moderate exercise
📝 Record blood sugar values daily
```

#### 5. Output confirmation

```
✅ Prenatal checkup record updated

Checkup information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Gestational week: 12 weeks
Checkup item: NT scan
Date: March 25, 2025
Result: Normal (NT value 1.8mm)

This checkup completed ✅

Next prenatal checkup:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 16 Quad screen - April 22, 2025 (28 days away)

Preparation: Fasting blood draw

💡 Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
All prenatal checkup results are for reference only; physician's diagnosis takes precedence.
Please consult your prenatal physician if you have any questions.
```

---

### 3. Record Symptoms - `symptom`

Record pregnancy symptoms.

**Parameter description:**
- `info`: Symptom description (required)
  - Symptom type: nausea, fatigue, edema, back pain, contractions
  - Severity: mild, moderate, severe

**Examples:**
```
/pregnancy symptom nausea moderate
/pregnancy symptom edema feet mild
/pregnancy symptom back pain moderate
/pregnancy symptom contractions false 5/hour  # Braxton Hicks contractions
```

**Execution steps:**

#### 1. Parse symptom information

**Symptom type identification:**
| Keywords | Symptom type | English |
|----------|-------------|---------|
| nausea, vomiting | nausea | nausea |
| fatigue, tired | fatigue | fatigue |
| swelling, edema | edema | edema |
| back pain, lower back pain | back_pain | back pain |
| contractions | contractions | contractions |

**Severity identification:**
- Mild: mild, light
- Moderate: moderate
- Severe: severe, very severe

**Frequency identification (optional):**
- "daily", "every day"
- "occasional", "sometimes"

#### 2. Symptom assessment

**Normal pregnancy symptoms:**
- Nausea (first trimester)
- Fatigue (first and second trimesters)
- Mild swelling (third trimester)
- Back pain (second and third trimesters)

**Warning symptoms (seek immediate medical attention):**
- Vaginal bleeding
- Severe abdominal pain (cramping)
- Severe headache with vision changes
- Sudden severe swelling (face, hands)
- Significantly reduced fetal movement

#### 3. Update symptom records

**Symptom data structure:**
```json
{
  "symptoms": {
    "nausea": {
      "present": true,
      "severity": "moderate",
      "severity_level": 2,
      "frequency": "daily",
      "triggers": ["morning", "empty_stomach"],
      "relief_methods": ["crackers", "small_frequent_meals"],
      "last_updated": "2025-03-20T10:00:00.000Z"
    },
    "edema": {
      "present": true,
      "severity": "mild",
      "severity_level": 1,
      "location": "feet_ankles",
      "worse_at": "evening",
      "last_updated": "2025-03-20T10:00:00.000Z"
    }
  }
}
```

#### 4. Integrate /symptom command

**Automatically create symptom record:**
```json
// data/symptom-records/2025-03/2025-03-20_nausea.json
{
  "id": "symptom_20250320001",
  "symptom_type": "nausea",
  "description": "nausea and vomiting, moderate",
  "severity": "moderate",
  "date": "2025-03-20",
  "womens_health_context": {
    "related": true,
    "module": "pregnancy",
    "pregnancy_id": "pregnancy_20250101",
    "gestational_week": 12,
    "trimester": "first"
  }
}
```

#### 5. Provide management recommendations

**Nausea management:**
```
Symptom management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Eat small, frequent meals (6-8 small meals per day)
• Eat a few crackers before getting up in the morning
• Avoid empty stomach
• Stay hydrated with small, frequent sips
• Avoid greasy, spicy foods
• Elevate head when resting

💊 Medication note:
If severe nausea affects eating, consult physician about using vitamin B6 or anti-nausea medication.
```

**Edema management:**
```
Symptom management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Elevate legs when resting
• Avoid prolonged standing or sitting
• Sleep on left side
• Take moderate walks
• Reduce salt intake
• Wear comfortable, loose shoes

⚠️ Warning:
If face or hands suddenly swell, seek immediate medical attention to rule out pre-eclampsia.
```

#### 6. Output confirmation

```
✅ Symptom recorded

Symptom information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: Nausea
Severity: Moderate
Frequency: Daily

Current gestational week: 12 weeks (first trimester)

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Nausea is a common first trimester symptom, usually resolves by weeks 14-16.

Management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Eat small, frequent meals
• Eat crackers before getting up
• Avoid empty stomach
• Stay hydrated

⚠️ Important note:
If severe vomiting leads to dehydration (decreased urination, dizziness), seek immediate medical attention.

Data synced to symptom records
```

---

### 4. Record Weight - `weight`

Record weight gain, monitor BMI and weight gain curve.

**Parameter description:**
- `info`: Weight value (required)
  - Weight: number + kg or lbs

**Examples:**
```
/pregnancy weight 62.5
/pregnancy weight 65kg
/pregnancy weight 140 lbs
```

**Execution steps:**

#### 1. Parse weight value

**Extract weight:**
- Number + unit: 62.5kg, 65 kg, 140 lbs
- Automatic unit conversion: 1 lb = 0.453592 kg

#### 2. Read base data

Read from [`data/profile.json`](data/profile.json):
- Pre-pregnancy weight
- Height

**If pre-pregnancy weight is missing:**
```
⚠️ Missing pre-pregnancy weight

Please set pre-pregnancy weight first:
/profile weight 60  # Pre-pregnancy weight 60kg

Or:
/pregnancy weight 62.5 --pre-pregnancy  # 62.5kg is current weight, 60kg is pre-pregnancy weight
```

#### 3. Calculate metrics

**Weight gain:**
```javascript
weight_gain = current_weight - pre_pregnancy_weight
```

**BMI calculation:**
```javascript
bmi = weight / (height_meters)^2
pre_pregnancy_bmi = pre_pregnancy_weight / (height_meters)^2
```

**Recommended pregnancy weight gain (based on IOM guidelines):**

| BMI Category | BMI Range | Total Gain Recommendation | Second/Third Trimester Weekly Gain |
|-------------|-----------|--------------------------|-----------------------------------|
| Underweight | <18.5 | 12.5-18 kg | 0.51 kg (0.44-0.58) |
| Normal | 18.5-24.9 | 11.5-16 kg | 0.42 kg (0.35-0.50) |
| Overweight | 25.0-29.9 | 7-11.5 kg | 0.28 kg (0.23-0.33) |
| Obese | ≥30.0 | 5-9 kg | 0.22 kg (0.17-0.27) |

**Pregnancy weight gain distribution:**
- First trimester (weeks 1-13): 1-2 kg
- Second trimester (weeks 14-27): 0.4-0.5 kg per week
- Third trimester (weeks 28-40): 0.4-0.5 kg per week

#### 4. Analyze weight trend

**Calculate weekly weight gain:**
```javascript
if (previous_weight_record) {
  weeks_between = current_week - previous_week;
  weekly_gain = (current_weight - previous_weight) / weeks_between;
}
```

**Assess whether weight gain is appropriate:**
- Too fast: weekly gain > recommended + 0.1 kg
- Too slow: weekly gain < recommended - 0.1 kg
- Normal: within recommended range

#### 5. Update weight records

**Weight data structure:**
```json
{
  "weight_tracking": [
    {
      "date": "2025-03-20",
      "week": 12,
      "weight": 62.5,
      "weight_unit": "kg",
      "weight_gain": 2.5,
      "bmi": 23.1,
      "bmi_category": "normal",
      "pre_pregnancy_weight": 60.0,
      "pre_pregnancy_bmi": 22.2,
      "recommended_total_gain": "11.5-16kg",
      "recommended_weekly_gain": "0.35-0.50kg",
      "weekly_gain": null,
      "gain_status": "normal",
      "trimester": "first"
    }
  ]
}
```

#### 6. Output confirmation

```
✅ Weight recorded

Weight information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Record date: March 20, 2025
Current gestational week: 12 weeks

Current weight: 62.5 kg
Pre-pregnancy weight: 60.0 kg
Weight gained: 2.5 kg
Current BMI: 23.1 (normal)

Weight gain assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended pregnancy weight gain: 11.5-16 kg
Current progress: Normal ✅

Expected first trimester gain: 1-2 kg
Current gain: 2.5 kg (slightly high)

Second/third trimester recommendation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Weekly weight gain: 0.35-0.50 kg

💡 Nutritional recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Balanced diet; do not "eat for two"
• Quality protein: fish, poultry, eggs, dairy, legumes
• Complex carbohydrates: whole grains, tubers
• Vegetables and fruits: 500g or more per day
• Moderate healthy fats: nuts, avocado

⚠️ Note:
If weight gain is too rapid, control high-sugar, high-fat foods,
increase vegetable proportion, and get moderate exercise.
```

---

### 5. Record Vital Signs - `vital`

Record blood pressure and other important vital signs.

**Parameter description:**
- `info`: Vital sign information (required)
  - Blood pressure: 120/80, 120 over 80
  - Or other vital signs: temperature, blood sugar, etc.

**Examples:**
```
/pregnancy vital bp 115/75
/pregnancy vital bp 120/80
/pregnancy vital bp 140/90  # Hypertension alert
/pregnancy vital temperature 37.2
/pregnancy vital glucose 5.5
```

**Execution steps:**

#### 1. Parse vital sign information

**Blood pressure format recognition:**
- Standard format: 120/80, 120/80 mmHg
- Text format: 120 over 80

**Extract values:**
```javascript
systolic = 120  // Systolic pressure
diastolic = 80  // Diastolic pressure
```

#### 2. Blood pressure classification

**Blood pressure classification standards (ACOG):**

| Classification | Systolic | Diastolic | Action |
|---------------|----------|-----------|--------|
| Normal | <120 | <80 | Continue |
| Elevated | 120-129 | <80 | Monitor |
| Stage 1 hypertension | 130-139 | 80-89 | Close monitoring |
| Stage 2 hypertension | 140-159 | 90-109 | Medical evaluation |
| Severe hypertension | ≥160 | ≥110 | Immediate medical attention |
| Pre-eclampsia range | ≥140 | ≥90 | Assess other symptoms |

#### 3. Assess risk

**Types of hypertensive disorders of pregnancy:**

1. **Gestational hypertension**:
   - BP ≥140/90, first occurring after 20 weeks
   - No proteinuria or other organ function damage

2. **Pre-eclampsia**:
   - BP ≥140/90 + any of the following:
     - Proteinuria (≥300mg/24h)
     - Liver function damage
     - Kidney function damage
     - Neurological symptoms (severe headache, blurred vision)
     - Thrombocytopenia
     - Pulmonary edema

**Warning symptoms (pre-eclampsia):**
- Severe headache
- Vision changes (flashes, blind spots)
- Upper abdominal pain (under right ribs)
- Nausea and vomiting
- Difficulty breathing

#### 4. Update vital sign records

**Blood pressure data structure:**
```json
{
  "blood_pressure": [
    {
      "date": "2025-03-20",
      "week": 12,
      "systolic": 115,
      "diastolic": 75,
      "classification": "normal",
      "mean_arterial_pressure": 88.3,
      "notes": "",
      "measured_at": "clinic"  // clinic/home
    }
  ]
}
```

#### 5. Output confirmation

**Normal blood pressure:**
```
✅ Blood pressure recorded

Blood pressure information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Record date: March 20, 2025
Current gestational week: 12 weeks

Blood pressure: 115/75 mmHg
Classification: Normal ✅

Mean arterial pressure: 88.3 mmHg

💡 Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Blood pressure is normal, keep it up!

Recommendations:
• Monitor blood pressure regularly
• Watch for headaches, vision changes
• Seek medical attention if blood pressure rises
```

**Hypertension alert:**
```
⚠️ Elevated blood pressure alert

Blood pressure information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Blood pressure: 145/95 mmHg
Classification: Stage 2 hypertension ⚠️

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Blood pressure is high, needs close monitoring.

🚨 Seek immediate medical evaluation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Urine protein test
• Assess liver and kidney function
• Check platelet count
• Assess fetal condition

⚠️ Warning symptoms (seek immediate medical attention):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Severe headache
• Blurred vision, flashing lights
• Upper abdominal pain (under right ribs)
• Nausea and vomiting
• Difficulty breathing

Please immediately contact your prenatal physician or go to hospital emergency!
```

---

### 6. View Status - `status`

Display current pregnancy status.

**Parameter description:**
- No parameters

**Example:**
```
/pregnancy status
```

**Execution steps:**

#### 1. Read pregnancy data

#### 2. Calculate current status

**Recalculate current gestational week:**
```javascript
current_week = floor((today - lmp_date) / 7)
current_day = (today - lmp_date) % 7
days_passed = today - lmp_date
days_remaining = due_date - today
progress = (days_passed / 280) * 100
```

#### 3. Generate status report

**Output format:**
```
📍 Current pregnancy status

Basic information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Last menstrual period: January 1, 2025
Due date: October 8, 2025
Current date: March 31, 2025

Pregnancy progress:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current gestational week: 12 weeks + 6 days
Pregnancy stage: First trimester (weeks 1-13)
Days passed: 89 days
Days remaining: 191 days
Completion: 32%

Fetal development:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Size: Plum-sized (about 5-6cm)
Weight: About 14g
Important milestones:
✅ Organ development basically complete
✅ Fingers and toes differentiated
✅ External genitalia beginning to form

Weight tracking:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Pre-pregnancy weight: 60.0 kg
Current weight: 62.5 kg
Weight gained: 2.5 kg
Recommended gain: 11.5-16 kg
Status: Normal ✅

Recent symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Nausea (moderate) - daily
• Fatigue (mild) - frequent

Most recent blood pressure:
━━━━━━━━━━━━━━━━━━━━━━━━━━
March 20: 115/75 mmHg (normal)

Completed prenatal checkups:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Week 12 NT scan - March 25 (normal)

Next prenatal checkup:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 16 Quad screen - April 22, 2025
22 days away

Preparation: Fasting blood draw

This week's focus:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Continue folic acid supplementation 400μg/day
• Seek immediate medical attention for vaginal bleeding or abdominal pain
• Rest well, avoid strenuous exercise
• Schedule week 16 quad screen

💡 Nutritional notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Quality protein: 2-3 servings/day
• Folic acid: 400μg/day
• Iron: 15mg/day (food + supplement)
• Calcium: 1000mg/day

⚠️ Important disclaimer:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is only for pregnancy health tracking and cannot replace professional prenatal care.
Please attend all prenatal checkups on time. Seek medical attention promptly for any abnormalities.
```

---

### 7. Next Checkup Reminder - `next-checkup`

Display next prenatal checkup information and preparation items.

**Parameter description:**
- No parameters

**Example:**
```
/pregnancy next-checkup
```

**Execution steps:**

#### 1. Find next prenatal checkup

Find the first item with `completed: false` in the `prenatal_checks` array.

#### 2. Calculate countdown

```javascript
days_until = (scheduled_date - today)
weeks_until = floor(days_until / 7)
```

#### 3. Generate reminder

```
📅 Next prenatal checkup reminder

Next checkup information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Checkup item: Quad screen (week 16)
Scheduled date: April 22, 2025 (Tuesday)
Time: 8:00 AM - 10:00 AM
22 days away (3 weeks)

Checkup item description:
━━━━━━━━━━━━━━━━━━━━━━━━━━
The quad screen (Down syndrome screening) detects
certain markers in maternal blood serum to assess
the risk of chromosomal abnormalities such as Down syndrome.

Checkup process:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Fasting blood draw
2. Wait for results (1-2 weeks)
3. Risk assessment

Preparation items:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Fast for 8 or more hours
✅ Bring ID and insurance card
✅ Bring previous prenatal checkup records
✅ Make appointment in advance

Frequently asked questions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Q: What to do if the quad screen shows high risk?
A: High risk does not mean confirmed diagnosis. Further testing
   such as NIPT or amniocentesis can clarify the diagnosis.

Q: How long does the quad screen result take?
A: Results are usually available in 1-2 weeks.

Q: Can I drink water while fasting?
A: You can drink a small amount of plain water, not drinks.

Questions to ask your physician:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Accuracy of quad screen results
• Whether NIPT is needed
• Time of next prenatal checkup
• What to pay attention to

📍 Location:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Hospital: [Enter hospital name]
Department: Obstetrics outpatient
Address: [Enter address]
Phone: [Enter phone number]

💡 Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Please book 1-2 days in advance to avoid waiting in line.
Contact the hospital in advance if you need to reschedule.

Countdown reminder:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommend booking before April 15
```

---

### 8. Set Multiple Pregnancy Type - `type`

Manually set the multiple pregnancy type.

**Parameter description:**
- `info`: Multiple pregnancy type (required)
  - Type: singleton, twins, triplets, quadruplets

**Examples:**
```
/pregnancy type twins
/pregnancy type triplets
/pregnancy type 3
```

**Execution steps:**

#### 1. Validate input

**Check items:**
- Whether there is an active pregnancy
- Whether the number of fetuses is in reasonable range (1-4)
- Whether the same type has already been set

#### 2. Update multiple pregnancy information

**Update data structure:**
```json
{
  "multi_pregnancy": {
    "pregnancy_type": "twins",
    "fetal_count": 2,
    "detection_method": "manual",
    "detection_confidence": "confirmed",
    "fetal_profiles": [
      {
        "baby_id": "A",
        "estimated_weight": null,
        "position": null,
        "heart_rate": null,
        "amniotic_fluid_index": null,
        "growth_percentile": null,
        "notes": ""
      },
      {
        "baby_id": "B",
        "estimated_weight": null,
        "position": null,
        "heart_rate": null,
        "amniotic_fluid_index": null,
        "growth_percentile": null,
        "notes": ""
      }
    ],
    "adjusted_due_date": "2025-09-17",
    "adjusted_delivery_week": 37
  }
}
```

#### 3. Adjust due date and prenatal care plan

**Multiple pregnancy due date adjustment:**

| Pregnancy type | Standard due date (weeks) | Adjusted weeks | Day adjustment |
|---------------|--------------------------|---------------|----------------|
| Singleton | 40 weeks | 40 weeks | 280 days (unchanged) |
| Twins | 40 weeks | 37 weeks | -21 days (259 days) |
| Triplets | 40 weeks | 35 weeks | -35 days (245 days) |
| Quadruplets | 40 weeks | 32 weeks | -56 days (224 days) |

**Prenatal checkup frequency adjustment (multiple pregnancies):**
- Twins: Every 2 weeks starting from week 28, every week from week 32
- Triplets and above: Every 2 weeks starting from week 24, every week from week 28
- Add cervical length monitoring (starting from weeks 16-18)
- Add fetal growth monitoring (every 4-6 weeks)

#### 4. Adjust weight gain recommendations

**Multiple pregnancy weight gain recommendations (based on IOM):**

| Pre-pregnancy BMI | Singleton total gain | Twin total gain | Triplet total gain | Quadruplet total gain |
|-------------------|---------------------|-----------------|--------------------|-----------------------|
| <18.5 | 12.5-18 kg | 20-25 kg | 25-30 kg | 28-33 kg |
| 18.5-24.9 | 11.5-16 kg | 16-24 kg | 20-29 kg | 22-31 kg |
| 25.0-29.9 | 7-11.5 kg | 14-23 kg | 17-27 kg | 19-29 kg |
| ≥30.0 | 5-9 kg | 11-19 kg | 14-25 kg | 16-27 kg |

#### 5. Output confirmation

```
✅ Multiple pregnancy type set

Pregnancy type information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: Twin pregnancy
Number of fetuses: 2
Setting method: Manually set

Due date adjustment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Original due date: October 8, 2025 (40 weeks)
Adjusted due date: September 17, 2025 (37 weeks)
Earlier by: 3 weeks

⚠️ Important note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Multiple pregnancy is a high-risk pregnancy. Recommendations:

Prenatal checkup frequency adjustment:
• From week 28: Every 2 weeks
• From week 32: Every week
• Add cervical length monitoring (starting from weeks 16-18)
• Add fetal growth monitoring (every 4-6 weeks)

Special monitoring:
• Fetal growth discordance
• Twin-to-twin transfusion syndrome (TTTS) signs
• Cervical length shortening

Weight gain recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total weight gain recommendation: 16-24 kg
Second/third trimester weekly gain: 0.5-0.7 kg

Recommendations:
• Consult Maternal-Fetal Medicine (MFM) specialist
• Consider referral to tertiary hospital
• Develop delivery plan (discuss at weeks 32-34)

Fetal profiles created:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Fetus A - information to be completed
• Fetus B - information to be completed

Use /pregnancy fetal to add detailed fetal information
```

---

### 9. Add Fetal Information - `fetal`

Add or update detailed information for individual fetuses.

**Parameter description:**
- `info`: Fetal information (required)
  - Fetal identifier: A, B, C, D (required)
  - Information type: weight, position, heart (heart rate), afi (amniotic fluid index), growth (growth percentile)
  - Value/description

**Examples:**
```
/pregnancy fetal A weight 1200g
/pregnancy fetal B position cephalic
/pregnancy fetal A heart 145
/pregnancy fetal B afi 8.5
/pregnancy fetal A growth 50th
/pregnancy fetal A cephalic HR150 AFI9
```

**Execution steps:**

#### 1. Parse fetal information

**Extract information:**
- **Fetal identifier**: A, B, C, D (case insensitive)
- **Information type**:
  - Weight: weight, wt, 1200g
  - Position: position, pos, cephalic (head-first), breech, transverse
  - Heart rate: heart, hr, 145, 150bpm
  - Amniotic fluid index: afi, 8.5, 9.0cm
  - Growth percentile: growth, percentile, 50th, 75%

#### 2. Validate input

**Check items:**
- Whether the fetal identifier is valid (A-D)
- Whether the current multiple pregnancy settings support the fetus
- Whether values are within reasonable range

#### 3. Update fetal profiles

**Fetal data structure:**
```json
{
  "multi_pregnancy": {
    "fetal_profiles": [
      {
        "baby_id": "A",
        "estimated_weight": {
          "value": 1200,
          "unit": "g",
          "percentile": 45,
          "last_updated": "2025-06-20T10:00:00.000Z"
        },
        "position": {
          "current": "cephalic",
          "confirmed_at": "2025-06-20",
          "notes": "cephalic, fixed"
        },
        "heart_rate": {
          "value": 145,
          "unit": "bpm",
          "last_measured": "2025-06-20",
          "variability": "normal"
        },
        "amniotic_fluid_index": {
          "value": 9.0,
          "unit": "cm",
          "pocket": "normal",
          "last_measured": "2025-06-20"
        },
        "growth_percentile": {
          "value": 50,
          "trend": "stable",
          "last_updated": "2025-06-20"
        },
        "notes": "developing well"
      },
      {
        "baby_id": "B",
        "estimated_weight": {
          "value": 1150,
          "unit": "g",
          "percentile": 42,
          "last_updated": "2025-06-20T10:00:00.000Z"
        },
        "position": {
          "current": "breech",
          "confirmed_at": "2025-06-20",
          "notes": "breech, may turn naturally"
        },
        "heart_rate": {
          "value": 150,
          "unit": "bpm",
          "last_measured": "2025-06-20",
          "variability": "normal"
        },
        "amniotic_fluid_index": {
          "value": 8.5,
          "unit": "cm",
          "pocket": "normal",
          "last_measured": "2025-06-20"
        },
        "growth_percentile": {
          "value": 48,
          "trend": "stable",
          "last_updated": "2025-06-20"
        },
        "notes": "developing normally, slightly smaller than A"
      }
    ]
  }
}
```

#### 4. Fetal growth analysis

**Weight consistency analysis (twins):**
```javascript
weight_discordance = |weight_A - weight_B| / max(weight_A, weight_B) * 100

// Normal: <15%
// Warning: 15-20%
// Abnormal: >20% (requires further examination)
```

**Amniotic fluid assessment:**
- Normal: AFI 5-24 cm (singleton), 8-25 cm (twins)
- Oligohydramnios: AFI <5 cm
- Polyhydramnios: AFI >24 cm

#### 5. Output confirmation

```
✅ Fetal information updated

Fetus A information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Weight: 1200g (45th percentile)
Position: Cephalic
Heart rate: 145 bpm (normal)
Amniotic fluid index: 9.0 cm (normal)
Growth percentile: 50% (stable)

Fetus B information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Weight: 1150g (42nd percentile)
Position: Breech
Heart rate: 150 bpm (normal)
Amniotic fluid index: 8.5 cm (normal)
Growth percentile: 48% (stable)

Twin consistency analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Weight discordance: 4.3% (normal)
Amniotic fluid discordance: Normal
Growth trend: Consistent

✓ Twin development is balanced with no significant discordance

Next examination recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Follow-up ultrasound in 2 weeks
• Monitor position changes
• Assess fetal growth
• Cervical length monitoring

⚠️ Notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Fetus B is in breech position, may require c-section
• Discuss delivery method at weeks 32-34
• Seek immediate medical attention for abnormal fetal movement
• Watch for twin-to-twin transfusion syndrome signs
```

**Abnormality alerts:**

**Weight discordance >20%:**
```
⚠️ Fetal growth discordance alert

Weight discordance: 25% (abnormal)
Fetus A: 1400g (55th percentile)
Fetus B: 1050g (28th percentile)

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Possible causes:
• Twin-to-twin transfusion syndrome (TTTS)
• Umbilical cord issues
• Unequal placental distribution

🏥 Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Immediately consult Maternal-Fetal Medicine specialist
• Ultrasound: umbilical cord, placenta, blood flow
• Close monitoring (weekly or every 2 weeks)
• Consider fetal treatment options
```

---

## Intelligent Multiple Pregnancy Detection

The system automatically detects multiple pregnancies in the following situations:

### 1. Keywords in prenatal checkup records

When recording prenatal checkups, the system checks keywords in the checkup results/notes:

**Twin keywords:**
- English: twins, two fetuses, twin pregnancy, dichorionic, monochorionic

**Triplet keywords:**
- English: triplets, three fetuses, triplet pregnancy

**Quadruplet keywords:**
- English: quadruplets, four fetuses, quad pregnancy

### 2. Detection process

```javascript
// Pseudocode example
function detectMultiples(checkupNotes) {
  const keywords = {
    twins: ["twins", "twin pregnancy", "two fetuses"],
    triplets: ["triplets", "triplet pregnancy", "three fetuses"],
    quadruplets: ["quadruplets", "quad pregnancy", "four fetuses"]
  };

  for (const [type, words] of Object.entries(keywords)) {
    if (words.some(word => checkupNotes.includes(word))) {
      return {
        detected: true,
        type: type,
        confidence: "suggested",
        source: "ultrasound_notes"
      };
    }
  }

  return { detected: false };
}
```

### 3. Detection response

When multiple pregnancy is detected:

**Suggest confirmation:**
```
🔍 Possible multiple pregnancy detected

Keyword detected in prenatal records: "twins"

System suggestion:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This may be a twin pregnancy.

Set pregnancy type to twins?
• /pregnancy type twins - Confirm as twins
• /pregnancy type singleton - Keep singleton setting

⚠️ Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Please confirm based on ultrasound results:
• Number of fetuses
• Chorionicity
• Amnionicity

Recommend confirming diagnosis with prenatal physician.
```

---

## Special Monitoring for Multiple Pregnancies

### 1. Twin-to-Twin Transfusion Syndrome (TTTS) Monitoring

**High-risk indicators:**
- Monochorionic diamniotic twins (MCDA)
- Significant amniotic fluid discordance (one too much, one too little)
- Fetal growth discordance >20%
- Invisible bladder (recipient twin)

**TTTS staging (Quintero staging):**
| Stage | Criteria |
|-------|----------|
| I | One twin polyhydramnios (MVP >8cm), other oligohydramnios (MVP <2cm), bladder still visible |
| II | In addition to Stage I, recipient's bladder not visible |
| III | In addition to Stage II, Doppler abnormalities |
| IV | In addition to Stage III, one or both fetuses with hydrops/ascites |
| V | One or both fetal deaths |

**Alert:**
```
⚠️ TTTS risk alert

Monitoring results abnormal:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Amniotic fluid discordance:
  Fetus A: MVP 12.0 cm (polyhydramnios)
  Fetus B: MVP 1.5 cm (oligohydramnios)
  Bladder B: Not visible

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Suspected TTTS Stage II

🏥 Urgent recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Immediately contact Maternal-Fetal Medicine center
• Evaluation within 24 hours
• Consider fetal laser surgery
• Close monitoring (2-3 times per week)

Do not delay! TTTS progresses rapidly.
```

### 2. Cervical Length Monitoring

**Monitoring frequency:**
- Twins: Starting from weeks 16-18, every 2-4 weeks
- Triplets and above: Starting from weeks 14-16, every 2 weeks

**Cervical length thresholds:**
| Cervical Length | Risk | Action |
|----------------|------|--------|
| >25mm | Low risk | Routine monitoring |
| 20-25mm | Medium risk | Follow-up every 1-2 weeks |
| <20mm | High risk | Consider cervical cerclage |

### 3. Fetal Growth Monitoring

**Monitoring frequency:**
- Twins: Every 4-6 weeks
- Triplets and above: Every 3-4 weeks

**Assessment indicators:**
- Weight percentile
- Weight discordance
- Amniotic fluid volume
- Umbilical blood flow

---

## Data Structure

### Main file: data/pregnancy-tracker.json

```json
{
  "created_at": "2025-12-31T12:00:00.000Z",
  "last_updated": "2025-12-31T12:00:00.000Z",

  "current_pregnancy": {
    "pregnancy_id": "pregnancy_20250101",
    "lmp_date": "2025-01-01",
    "due_date": "2025-10-08",
    "due_date_confidence": "high",
    "corrected_by_ultrasound": false,
    "ultrasound_correction_date": null,

    "current_week": 12,
    "current_day": 6,
    "current_trimester": "first",
    "days_passed": 89,
    "days_remaining": 191,
    "progress_percentage": 32,

    "prenatal_checks": [
      {
        "check_id": "check_001",
        "week": 12,
        "check_type": "NT scan",
        "check_type_en": "NT_scan",
        "scheduled_date": "2025-03-25",
        "completed": false,
        "completed_at": null,
        "results": {},
        "notes": "",
        "preparation": "Full bladder required"
      }
    ],

    "symptoms": {
      "nausea": {
        "present": false,
        "severity": null,
        "frequency": null,
        "triggers": [],
        "relief_methods": [],
        "last_updated": null
      },
      "fatigue": {
        "present": false,
        "severity": null
      },
      "edema": {
        "present": false,
        "severity": null,
        "location": null
      },
      "back_pain": {
        "present": false,
        "severity": null
      },
      "contractions": {
        "present": false,
        "type": null,
        "frequency": null
      }
    },

    "weight_tracking": [
      {
        "date": "2025-01-01",
        "week": 0,
        "weight": 60.0,
        "weight_unit": "kg",
        "weight_gain": 0.0,
        "bmi": 22.2,
        "bmi_category": "normal",
        "pre_pregnancy_weight": 60.0,
        "pre_pregnancy_bmi": 22.2,
        "recommended_total_gain": "11.5-16kg",
        "recommended_weekly_gain": "0.35-0.50kg",
        "weekly_gain": null,
        "gain_status": "normal",
        "trimester": "first"
      }
    ],

    "blood_pressure": [
      {
        "date": "2025-03-15",
        "week": 10,
        "systolic": 115,
        "diastolic": 75,
        "classification": "normal",
        "mean_arterial_pressure": 88.3,
        "notes": "",
        "measured_at": "clinic"
      }
    ],

    "fetal_movement": {
      "tracking_started": false,
      "start_week": 28,
      "movements": []
    },

    "contractions": [],

    "nutrition_plan": {
      "folic_acid": {
        "dose": "400μg",
        "frequency": "daily",
        "started": null,
        "adherence": null
      },
      "iron": {
        "dose": null,
        "frequency": null,
        "started": null,
        "adherence": null
      },
      "calcium": {
        "dose": null,
        "frequency": null,
        "started": null,
        "adherence": null
      },
      "dha": {
        "dose": null,
        "frequency": null,
        "started": null,
        "adherence": null
      }
    },

    "medication_safety_checks": [],

    "risk_factors": [],

    "notes": "",

    "completed": false,
    "delivery_date": null,
    "delivery_outcome": null,

    "metadata": {
      "created_at": "2025-01-01T00:00:00.000Z",
      "last_updated": "2025-03-25T10:00:00.000Z"
    }
  },

  "pregnancy_history": [],

  "statistics": {
    "total_pregnancies": 1,
    "current_pregnancy_week": 12,
    "total_weight_gain": 2.5,
    "average_weekly_gain": 0.21,
    "checkups_completed": 1,
    "checkups_scheduled": 11
  },

  "settings": {
    "reminder_days_before": 7,
    "weight_unit": "kg",
    "preferred_checkup_time": "morning"
  }
}
```

### Detailed record file: data/pregnancy-records/YYYY-MM/YYYY-MM-DD_pregnancy-record.json

```json
{
  "pregnancy_id": "pregnancy_20250101",
  "record_date": "2025-03-31",
  "week": 12,
  "day": 6,
  "trimester": "first",

  "daily_log": {
    "symptoms": ["nausea", "fatigue"],
    "mood": "normal",
    "energy_level": "moderate",
    "notes": ""
  },

  "checkups": [],
  "vitals": [],
  "weight": {},

  "fetal_development_info": {
    "size_description": "plum-sized",
    "size_cm": "5-6cm",
    "weight_g": 14,
    "milestones": [
      "Organ development basically complete",
      "Fingers and toes differentiated",
      "External genitalia beginning to form"
    ]
  },

  "metadata": {
    "created_at": "2025-03-31T20:00:00.000Z",
    "last_updated": "2025-03-31T20:00:00.000Z"
  }
}
```

---

## Intelligent Recognition Rules

### Date recognition

| User input | Standard format | Example |
|-----------|----------------|---------|
| YYYY-MM-DD | YYYY-MM-DD | 2025-01-01 |
| January 1st this year | YYYY-MM-DD | → 2025-01-01 |
| last month | Calculate date | last month January 1st |
| X weeks ago | Calculate date | 12 weeks ago |

### Gestational week recognition

| User input | Extracted result |
|-----------|----------------|
| week 12 | 12 weeks |
| 12w | 12 weeks |
| gestational week 12 | 12 weeks |

### Checkup type recognition

| User input | Standard type |
|-----------|--------------|
| NT, NT scan | NT scan |
| Quad screen, Down syndrome screening | Quad screen |
| Anatomy scan, anomaly scan | Anatomy scan |
| Glucose tolerance, OGTT | Glucose tolerance test |
| Routine, prenatal | Routine prenatal |

### Result recognition

| Normal | Abnormal |
|--------|---------|
| normal, pass | abnormal |
| low risk | high risk |
| negative | positive |

### Symptom recognition

| Keywords | Symptom type |
|----------|-------------|
| nausea, vomiting | nausea |
| fatigue, tired | fatigue |
| swelling, edema | edema |
| back pain, lower back pain | back_pain |
| contractions | contractions |

### Severity recognition

| Mild | Moderate | Severe |
|------|---------|--------|
| mild, light | moderate | severe |

### Blood pressure format recognition

| User input | Systolic | Diastolic |
|-----------|---------|----------|
| 120/80 | 120 | 80 |
| 120 over 80 | 120 | 80 |

---

## Error Handling

| Scenario | Error message | Recommendation |
|---------|--------------|----------------|
| No active pregnancy | No active pregnancy record<br>Please use /pregnancy start first | Guide to start recording |
| Pregnancy already exists | Active pregnancy already exists<br>Please complete current pregnancy first | Show current status |
| LMP date invalid | LMP date invalid<br>Cannot be a future date | Validate date |
| Missing profile data | Missing personal information<br>Please set height/weight/birthday first | Guide to profile |
| Checkup type not recognized | Unrecognized checkup type<br>Supported: NT, quad screen, anatomy scan, glucose tolerance, routine | List supported types |
| Gestational week out of range | Gestational week must be between 0-42 weeks | Show valid range |

---

## Notes

- This system is only for pregnancy health tracking and cannot replace professional prenatal care
- Please attend all prenatal checkups on time
- Due date calculation may have errors; ultrasound takes precedence
- Seek medical attention promptly for any abnormalities
- Does not assess fetal health status
- Does not predict pregnancy outcomes
- Fetal movement monitoring cannot replace medical monitoring

**Emergency alerts:**
If any of the following occur, seek immediate medical attention:
- Vaginal bleeding
- Severe abdominal pain
- Severe headache with vision changes
- Sudden severe swelling
- Significantly reduced or absent fetal movement
- Fever above 38°C
- Persistent vomiting leading to dehydration

All data is saved locally only to ensure privacy and security.

---

## Usage Examples

```
# Start pregnancy record
/pregnancy start 2025-01-01

# Record prenatal checkup
/pregnancy checkup week 12 NT normal
/pregnancy checkup week 16 quad-screen low-risk

# Record symptoms
/pregnancy symptom nausea moderate
/pregnancy symptom edema feet mild

# Record weight
/pregnancy weight 62.5

# Record blood pressure
/pregnancy vital bp 115/75

# View status
/pregnancy status

# Next checkup
/pregnancy next-checkup
```
