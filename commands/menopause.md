---
description: Manage menopause symptoms and health records
arguments:
  - name: action
    description: "Action type: start(begin)/symptom(symptoms)/hrt(hormone therapy)/bone(bone density)/status(status)/risk(risk assessment)"
    required: true
  - name: info
    description: Menopause information (age, last menstrual period date, symptom description, test results, etc., in natural language)
    required: false
---

# Menopause Management

Perimenopause symptom tracking and management, providing menopause health assessment and management recommendations.

## Action Types

### 1. Start Menopause Tracking - `start`

Initialize menopause tracking records.

**Parameter description:**
- `info`: Basic menopause information (required)
  - Age: number
  - Last menstrual period date: YYYY-MM-DD

**Examples:**
```
/menopause start 48 2025-11-15
/menopause start age 48 last period November 15 2025
/menopause start age 50 2025-06-01
```

**Execution steps:**

#### 1. Parse input information

Extract from natural language:
- **Age**: number
- **Last Menstrual Period (LMP)**: exact date

#### 2. Validate input

**Check items:**
- Age should be between 40-65
- LMP cannot be a future date
- LMP should be within the past 12 months

#### 3. Determine menopause stage

**Menopause stage definitions:**

| Stage | Definition | Menstrual Pattern | Time Range |
|-------|-----------|-------------------|------------|
| Perimenopause | Perimenopausal | Irregular cycles | 40-55 years |
| Menopause | Menopausal | 12 months without periods | LMP + 12 months |
| Postmenopause | Postmenopausal | >12 months without periods | >12 months |

**Decision logic:**
```javascript
months_since_lmp = (today - lmp_date) / 30.44

if (months_since_lmp < 12) {
  stage = "perimenopausal"  // perimenopause
} else if (months_since_lmp >= 12 && months_since_lmp < 36) {
  stage = "menopausal"  // menopause
} else {
  stage = "postmenopausal"  // postmenopause
}
```

#### 4. Create menopause record

**Generate menopause_id**: `menopause_YYYYMMDD`

**Menopause data structure:**
```json
{
  "menopause_id": "menopause_20250101",
  "stage": "perimenopausal",
  "age": 48,
  "last_menstrual_period": "2025-11-15",
  "months_since_lmp": 0,

  "symptoms": {
    "hot_flashes": {
      "present": false,
      "frequency": null,
      "severity": null,
      "impact_on_life": null,
      "triggers": [],
      "last_updated": null
    },
    "night_sweats": {
      "present": false,
      "frequency": null,
      "severity": null
    },
    "sleep_issues": {
      "present": false,
      "type": null,
      "sleep_quality": null
    },
    "mood_changes": {
      "present": false,
      "symptoms": []
    },
    "vaginal_dryness": {
      "present": false,
      "severity": null
    },
    "joint_pain": {
      "present": false,
      "severity": null,
      "locations": []
    }
  },

  "symptom_history": [],

  "hrt": {
    "on_treatment": false,
    "considering": false,
    "medication": null,
    "type": null,
    "dose": null,
    "route": null,
    "start_date": null,
    "duration": null,
    "effectiveness": null,
    "effectiveness_rating": null,
    "side_effects": [],
    "notes": ""
  },

  "bone_density": {
    "last_check": null,
    "t_score": null,
    "z_score": null,
    "diagnosis": null,
    "diagnosis_category": null,
    "fracture_risk": null,
    "fracture_risk_level": null,
    "next_check_due": null,
    "calcium_intake": {},
    "vitamin_d": {},
    "weight_bearing_exercise": null,
    "fall_risk_factors": []
  },

  "cardiovascular_risk": {
    "last_assessment": null,
    "blood_pressure": null,
    "systolic": null,
    "diastolic": null,
    "bp_classification": null,
    "lipids": {},
    "blood_sugar": {},
    "risk_level": null,
    "risk_factors": [],
    "modifiable_factors": []
  },

  "lifestyle": {
    "exercise": {},
    "diet": {},
    "stress_management": [],
    "sleep_habits": null
  },

  "metadata": {
    "created_at": "2025-01-01T00:00:00.000Z",
    "last_updated": "2025-01-01T00:00:00.000Z"
  }
}
```

#### 5. Save data files

**Main file**: `data/menopause-tracker.json`

**Detailed records**: `data/menopause-records/YYYY-MM/YYYY-MM-DD_symptom-log.json`

#### 6. Output confirmation

```
✅ Menopause tracking created

Basic information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Age: 48
Last menstrual period: November 15, 2025
Menopause stage: Perimenopause

Stage description:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Perimenopause refers to the period from when ovarian function
begins to decline until one year after menopause,
typically lasting 4-10 years.

Common symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Irregular menstrual cycles
• Hot flashes and sweating
• Mood swings
• Sleep disturbances
• Vaginal dryness

Recommended checks:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Bone density scan (recommended every 1-2 years)
✅ Cardiovascular risk assessment (blood pressure, lipids)
✅ Gynecological exam (annually)
✅ Breast exam (annually)

💡 Lifestyle recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Regular exercise (3-5 times per week)
• Balanced diet (rich in calcium and vitamin D)
• Weight control (BMI 18.5-24.9)
• Quit smoking, limit alcohol
• Stress management
• Adequate sleep

⚠️ Important disclaimer:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is for menopause health tracking only and cannot replace professional medical advice.

For severe symptoms, please consult a gynecologic endocrinologist:
• Severe hot flashes affecting daily life
• Severe mood swings or depression
• Abnormal vaginal bleeding
• Cardiovascular symptoms

Data saved to: data/menopause-tracker.json
```

---

### 2. Record Symptoms - `symptom`

Record menopause symptoms and score them.

**Parameter description:**
- `info`: Symptom description (required)
  - Symptom type: hot-flashes, sleep, mood, vaginal-dryness, joint-pain
  - Frequency: number/day or number/night
  - Severity: mild, moderate, severe

**Examples:**
```
/menopause symptom hot-flashes 5-10 moderate
/menopause symptom hot flashes 10 times daily severe
/menopause symptom sleep insomnia
/menopause symptom mood anxiety irritability
/menopause symptom joint-pain knees mild
```

**Execution steps:**

#### 1. Parse symptom information

**Symptom type identification:**
| Keywords | Symptom type | Description |
|----------|-------------|-------------|
| hot flashes, fever, sweating | hot_flashes | hot flashes |
| night sweats, nocturnal sweating | night_sweats | night sweats |
| sleep, insomnia | sleep_issues | sleep issues |
| mood, anxiety, depression | mood_changes | mood changes |
| vaginal dryness | vaginal_dryness | vaginal dryness |
| joint pain, bone pain | joint_pain | joint pain |

**Frequency identification:**
- "5-10 times daily", "5-10/day" → hot_flashes frequency
- "3-4 times nightly", "3-4/night" → night_sweats frequency
- "often", "occasionally", "sometimes" → general frequency

**Severity identification:**
- mild, slight
- moderate, medium
- severe, serious

#### 2. Symptom scoring

**Hot flash scoring:**
```javascript
frequency_score = 0
if (frequency <= 2/day) {
  frequency_score = 1
} else if (frequency <= 5/day) {
  frequency_score = 2
} else if (frequency <= 10/day) {
  frequency_score = 3
} else {
  frequency_score = 4
}

severity_score = 0
if (severity === 'mild') severity_score = 1
else if (severity === 'moderate') severity_score = 2
else if (severity === 'severe') severity_score = 3

hot_flash_score = frequency_score * severity_score  // max 12
```

**Sleep quality score (0-10):**
```javascript
if (sleep_issues) {
  if (type === 'difficulty_falling_asleep') score -= 3
  if (type === 'difficulty_staying_asleep') score -= 3
  if (type === 'early_morning_awakening') score -= 2
  if (quality === 'poor') score -= 2
}
sleep_score = max(0, 10 + score)
```

**Mood score (0-10):**
```javascript
mood_score = 10 - (symptoms.count * 2)  // -2 points per symptom
```

**Overall symptom burden (0-100):**
```javascript
symptom_burden = (
  (hot_flash_score / 12) * 30 +    // hot flashes 30%
  (sleep_score / 10) * 25 +        // sleep 25%
  (mood_score / 10) * 20 +         // mood 20%
  other_symptoms_score * 25        // other 25%
)
```

#### 3. Update symptom records

**Symptom data structure:**
```json
{
  "symptoms": {
    "hot_flashes": {
      "present": true,
      "frequency": "5-10_per_day",
      "frequency_count": 7,
      "severity": "moderate",
      "severity_level": 2,
      "impact_on_life": "mild",
      "impact_level": 1,
      "triggers": ["stress", "hot_drinks", "warm_room"],
      "relief_methods": ["cool_compress", "layered_clothing"],
      "score": 14,
      "last_updated": "2025-12-01T10:00:00.000Z"
    },
    "night_sweats": {
      "present": true,
      "frequency": "3-4_per_night",
      "severity": "moderate",
      "impact_on_sleep": "moderate"
    },
    "sleep_issues": {
      "present": true,
      "frequency": "often",
      "type": "difficulty_falling_asleep",
      "sleep_quality": "poor",
      "sleep_duration_hours": 5,
      "score": 4
    },
    "mood_changes": {
      "present": true,
      "symptoms": ["anxiety", "irritability", "mood_swings"],
      "severity": "mild",
      "impact": "minimal",
      "score": 6
    }
  }
}
```

#### 4. Integrate /symptom command

**Automatically create symptom record:**
```json
// data/symptom-records/2025-12/2025-12-01_hot-flashes.json
{
  "id": "symptom_20251201001",
  "symptom_type": "hot_flashes",
  "description": "5-10 times daily, moderate",
  "severity": "moderate",
  "date": "2025-12-01",
  "womens_health_context": {
    "related": true,
    "module": "menopause",
    "menopause_id": "menopause_20250101",
    "stage": "perimenopausal"
  }
}
```

#### 5. Provide management recommendations

**Hot flash management:**
```
Hot flash management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Lifestyle adjustments:
• Identify and avoid triggers (hot drinks, hot environments, stress)
• Wear layered clothing for easy adjustment
• Keep room temperature cool (18-22°C)
• Use cooling pillow pads
• Regular exercise (yoga, tai chi)

• Deep breathing and relaxation techniques
• Avoid spicy foods, alcohol, caffeine

💊 Treatment options (require medical evaluation):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Hormone replacement therapy (HRT)
• Non-hormonal medications (as appropriate)
• Herbal supplements (e.g., black cohosh, with caution)

⚠️ Important:
For severe hot flashes, consult a gynecologic endocrinologist
to evaluate whether HRT is needed.
```

**Sleep improvement:**
```
Sleep improvement recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Sleep hygiene:
• Maintain a regular sleep schedule
• Avoid screen time before bed
• Keep bedroom cool, dark, and quiet
• Avoid afternoon caffeine
• Pre-sleep relaxation (meditation, warm bath)

• If hot flashes affect sleep:
  - Use breathable bedding
  - Cooling pillow pads
  - Layered blankets

💊 For severe insomnia:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Consult a doctor about sleep medications,
but prioritize non-pharmacological methods.
```

#### 6. Output confirmation

```
✅ Symptoms recorded

Symptom information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: Hot flashes
Frequency: 5-10 times daily
Severity: Moderate

Current menopause stage: Perimenopause

Symptom scores:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Hot flash score: 14/12 (severe)
Sleep score: 4/10 (poor)
Mood score: 6/10 (fair)

Overall symptom burden: 65/100 (moderate)

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Moderate symptom burden affecting quality of life.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Lifestyle adjustments (see management recommendations)
✅ Regular exercise, stress reduction
⚠️ If symptoms severely affect daily life, seek medical evaluation
   for possible HRT treatment

Management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
[Detailed management recommendations...]

⚠️ Important reminder:
If symptoms are severe or continuously worsening, consult a
gynecologic endocrinologist to evaluate whether hormone therapy is needed.

Data synced to symptom records
```

---

### 3. Record HRT Treatment - `hrt`

Record hormone replacement therapy information.

**Parameter description:**
- `info`: HRT treatment information (required)
  - action: start, stop, effectiveness (effectiveness evaluation)
  - Medication info: drug name, dosage, route of administration

**Examples:**
```
/menopause hrt start estradiol 1mg oral
/menopause hrt start estrogen 1mg + progesterone 100mg
/menopause hrt effectiveness good
/menopause hrt effectiveness moderate hot flashes reduced 50%
/menopause hrt stop due to side effects
```

**Execution steps:**

#### 1. Parse HRT information

**Identify HRT type:**
- **Estrogen only**: estrogen only (for post-hysterectomy)
- **Combined estrogen-progesterone**: estrogen + progesterone (required if uterus intact)
- **Local estrogen**: vaginal estrogen (for vaginal dryness)

**Medication identification:**
| Medication | Type | Common dosage |
|------------|------|---------------|
| Estradiol | Estrogen | 1-2mg/day (oral) |
| Estradiol valerate | Estrogen | 1-2mg/day |
| Dydrogesterone | Progesterone | 10mg/day (cyclic) |
| Progesterone capsules | Progesterone | 100-200mg/day |

#### 2. HRT treatment assessment

**HRT indications:**
- Menopause-related symptoms (hot flashes, sweating)
- Urogenital atrophy symptoms
- Osteoporosis prevention (<60 years or <10 years post-menopause)

**HRT contraindications:**
- Unexplained vaginal bleeding
- Known or suspected pregnancy
- Known breast cancer
- Known or suspected sex hormone-dependent malignancy
- Active deep vein thrombosis or pulmonary embolism
- Severe liver disease

**Relative contraindications:**
- Endometriosis
- Uterine fibroids
- Benign breast disease
- Gallbladder disease
- Hypertension
- Diabetes
- Migraine

#### 3. Update HRT records

**HRT data structure:**
```json
{
  "hrt": {
    "on_treatment": true,
    "considering": false,
    "medication": "Estradiol",
    "type": "estrogen_only",
    "dose": "1mg",
    "route": "oral",
    "frequency": "daily",
    "start_date": "2025-12-01",
    "duration_months": 0,
    "effectiveness": null,
    "effectiveness_rating": null,
    "side_effects": [],
    "notes": "",
    "prescribing_doctor": ""
  }
}
```

**Effectiveness evaluation data structure:**
```json
{
  "hrt": {
    "on_treatment": true,
    "effectiveness": "good",
    "effectiveness_rating": 8,
    "effectiveness_notes": "Hot flashes reduced 80%, sleep improved",
    "side_effects": ["breast tenderness"],
    "side_effects_severity": "mild",
    "quality_of_life_improvement": "significant"
  }
}
```

#### 4. Provide safety reminders

**HRT safety monitoring:**
```
⚠️ HRT Treatment Safety Reminder

Regular monitoring items:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Breast exam (annually)
   • Clinical breast examination
   • Breast ultrasound or mammogram

✅ Gynecological exam (annually)
   • Pelvic exam
   • Cervical smear
   • Transvaginal ultrasound (endometrial monitoring)

✅ Blood pressure monitoring (every 3-6 months)
✅ Lipid testing (annually)
✅ Liver function testing (annually)

⚠️ Watch for these symptoms (seek immediate care):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Abnormal vaginal bleeding
• Breast lump or discharge
• Leg pain or swelling (DVT symptoms)
• Sudden chest pain or difficulty breathing (PE symptoms)
• Severe headache or vision changes

HRT principles:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Lowest effective dose
• Shortest necessary duration
• Regular risk-benefit assessment
• Individualized treatment plan

💡 Note:
HRT must be used under medical supervision.
This system only records treatment status and does not replace medical advice.
```

#### 5. Output confirmation

```
✅ HRT record updated

HRT treatment information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Medication: Estradiol
Type: Estrogen therapy
Dose: 1mg
Instructions: Daily oral
Start date: December 1, 2025

Treatment duration: 1 month

💡 Important reminder:
━━━━━━━━━━━━━━━━━━━━━━━━━━
HRT treatment must be conducted under the guidance of a gynecologic endocrinologist.

Regular follow-up items:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Breast exam (annually)
✅ Gynecological exam (annually)
✅ Blood pressure monitoring (every 3-6 months)
✅ Lipid testing (annually)

⚠️ Watch for abnormal symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Abnormal vaginal bleeding
• Breast lump
• Leg pain and swelling
• Sudden chest pain

If the above symptoms occur, seek medical attention immediately!
```

---

### 4. Record Bone Density - `bone`

Record bone density test results.

**Parameter description:**
- `info`: Bone density test results (required)
  - T-score: number (e.g., -1.5)
  - Diagnosis: normal, osteopenia (low bone mass), osteoporosis

**Examples:**
```
/menopause bone -1.5 osteopenia
/menopause bone T-score -1.5 low bone mass
/menopause bone -2.8 osteoporosis
/menopause bone normal
```

**Execution steps:**

#### 1. Parse bone density information

**T-score identification:**
- "-1.5", "negative 1.5", "-1.5 SD" → T-score

**Diagnosis identification:**
| Keywords | Diagnosis | T-score range |
|----------|-----------|--------------|
| normal | Normal | T ≥ -1.0 |
| osteopenia, low bone mass | Low bone mass | -2.5 < T < -1.0 |
| osteoporosis | Osteoporosis | T ≤ -2.5 |

#### 2. Bone density classification

**WHO diagnostic criteria:**

| Classification | T-score | Fracture risk |
|----------------|---------|---------------|
| Normal | T ≥ -1.0 | Normal |
| Osteopenia | -2.5 < T < -1.0 | Increased |
| Osteoporosis | T ≤ -2.5 | High |
| Severe osteoporosis | T ≤ -2.5 + fracture | Very high |

#### 3. Fracture risk assessment

**Basic FRAX assessment (simplified):**
```javascript
fracture_risk = "low"
if (t_score <= -2.5) {
  fracture_risk = "high"
} else if (t_score <= -2.0) {
  fracture_risk = "moderate"
}

// Consider other risk factors
risk_factors = [
  "previous_fracture",        // prior fracture history
  "parent_hip_fracture",      // parental hip fracture history
  "smoking",                  // smoking
  "glucocorticoids",          // long-term glucocorticoid use
  "rheumatoid_arthritis",     // rheumatoid arthritis
  "secondary_osteoporosis",   // secondary osteoporosis
  "alcohol_3_units_daily"     // >3 alcohol units daily
]
```

#### 4. Treatment recommendations

**Osteopenia management:**
```
Osteopenia management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Nutritional supplementation:
✅ Calcium: 1200-1500mg daily
  • Dietary calcium + supplements
  • Divided doses for better absorption
✅ Vitamin D: 800-1000 IU daily
  • Maintain serum 25(OH)D >30ng/mL
  • Higher doses may be needed in winter

Lifestyle:
✅ Weight-bearing exercise: 3-4 times per week
  • Walking, jogging, dancing
  • Strength training
✅ Fall prevention measures:
  • Home safety
  • Balance training
  • Avoid sedatives

Follow-up:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended bone density recheck in 1-2 years
```

**Osteoporosis management:**
```
⚠️ Osteoporosis management recommendations

Drug treatment (requires medical prescription):
━━━━━━━━━━━━━━━━━━━━━━━━━━
Bisphosphonates:
• Alendronate (Fosamax)
• Zoledronic acid (Reclast)

Other medications:
• Denosumab (Prolia)
• Raloxifene (Evista)
• Teriparatide (Forteo)

⚠️ Warning:
Drug treatment must be conducted under medical supervision!

Nutritional supplementation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Calcium: 1200-1500mg daily
✅ Vitamin D: 1000-2000 IU daily
✅ Protein: 1.0-1.2g/kg body weight daily

Lifestyle:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Weight-bearing exercise (gradually increase intensity)
✅ Strength training
✅ Balance training (fall prevention)
✅ No smoking
✅ Limit alcohol

Follow-up:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended bone density recheck in 1 year
Monitor treatment effectiveness
```

#### 5. Update bone density records

**Bone density data structure:**
```json
{
  "bone_density": {
    "last_check": "2025-06-15",
    "t_score": -1.5,
    "z_score": -1.2,
    "diagnosis": "osteopenia",
    "diagnosis_category": "low_bone_mass",
    "fracture_risk": "low",
    "fracture_risk_level": 1,
    "next_check_due": "2026-06-15",
    "check_interval_years": 1,

    "calcium_intake": {
      "dietary": "adequate",
      "supplement": "1000mg_daily",
      "total_daily_mg": 1500,
      "adherence": "good"
    },

    "vitamin_d": {
      "supplement": "2000IU_daily",
      "level": null,
      "adherence": "good"
    },

    "weight_bearing_exercise": "3-4_per_week",
    "fall_risk_factors": [],

    "notes": "",
    "history": [
      {
        "date": "2023-06-15",
        "t_score": -1.3,
        "diagnosis": "normal"
      }
    ]
  }
}
```

#### 6. Output confirmation

```
✅ Bone density record updated

Bone density test information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test date: June 15, 2025
T-score: -1.5
Z-score: -1.2
Diagnosis: Osteopenia (Low bone mass)

Fracture risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current risk: Low

Bone density changes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
2023: T-score -1.3 (Normal)
2025: T-score -1.5 (Osteopenia)
Change: Slight decline ⚠️

Management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Calcium: 1200-1500mg daily
✅ Vitamin D: 800-1000 IU daily
✅ Weight-bearing exercise: 3-4 times per week
✅ Strength training: 2-3 times per week
✅ Quit smoking, limit alcohol

Follow-up recommendation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Next recheck: June 15, 2026 (1 year later)
Or as advised by your doctor

⚠️ Important reminder:
Osteopenia is a precursor to osteoporosis.
Active intervention can prevent or delay the progression to osteoporosis.

Recommend consulting an endocrinologist or orthopedist
to develop a personalized treatment plan.
```

---

### 5. View Status - `status`

Display menopause tracking status.

**Parameter description:**
- No parameters

**Examples:**
```
/menopause status
```

**Execution steps:**

#### 1. Read menopause data

#### 2. Generate status report

```
📍 Menopause Tracking Status

Basic information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Age: 48
Last menstrual period: November 15, 2025
Menopause stage: Perimenopause
Tracking duration: 1 month

Current symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 Hot flashes: 5-10 times daily (moderate)
💦 Night sweats: 3-4 times nightly (moderate)
😴 Sleep: Insomnia, poor sleep quality
😔 Mood: Anxiety, irritability
💪 Joint pain: Knees, fingers (mild)

Symptom burden score:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall symptom burden: 65/100 (moderate)
  • Hot flash impact: 14/12 (severe)
  • Sleep impact: 4/10 (poor)
  • Mood impact: 6/10 (fair)

Symptom trend:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Past 30 days: Stable fluctuation

HRT treatment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: Untreated
Under consideration: Yes

Bone density:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Last check: June 15, 2025
T-score: -1.5
Diagnosis: Osteopenia
Next recheck: June 15, 2026

Cardiovascular risk:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Blood pressure: 120/80 mmHg (normal)
Lipids: Not tested
Blood sugar: Not tested
Overall risk: Low

Lifestyle:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Exercise: 3-4 times per week (walking, yoga)
Diet: Balanced, adequate calcium intake
Stress management: Meditation, reading
Sleep habits: Irregular

Recommended actions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue regular exercise
✅ Maintain calcium and vitamin D supplementation
✅ Consider consulting doctor about HRT evaluation
📅 Schedule annual checkup (include lipids, blood sugar)
📅 Bone density recheck in 1 year

💡 Focus this week:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Keep a hot flash diary (identify triggers)
• Try sleep improvement techniques
• Continue exercise and stress reduction
• If symptoms worsen, consider seeking medical care

⚠️ Important disclaimer:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is for menopause health tracking only and cannot replace professional medical advice.

For severe symptoms, consult a gynecologic endocrinologist.
```

---

### 6. Risk Assessment - `risk`

Display comprehensive health risk assessment.

**Parameter description:**
- No parameters

**Examples:**
```
/menopause risk
```

**Execution steps:**

#### 1. Comprehensive risk assessment

**Osteoporosis risk assessment:**
```javascript
risk = 0
if (t_score <= -2.5) risk += 3
else if (t_score <= -2.0) risk += 2
else if (t_score <= -1.0) risk += 1

if (age >= 65) risk += 1
if (bmi < 18.5) risk += 1
if (smoking) risk += 1
if (family_history_fracture) risk += 1
if (glucocorticoids) risk += 1
if (previous_fracture) risk += 2

if (risk >= 5) osteoporosis_risk = "high"
else if (risk >= 3) osteoporosis_risk = "moderate"
else osteoporosis_risk = "low"
```

**Cardiovascular risk assessment:**
```javascript
risk = 0
if (bp_systolic >= 140 || bp_diastolic >= 90) risk += 2
else if (bp_systolic >= 130 || bp_diastolic >= 80) risk += 1

if (total_cholesterol >= 6.2) risk += 2
else if (total_cholesterol >= 5.2) risk += 1

if (ldl >= 4.1) risk += 2
else if (ldl >= 3.4) risk += 1

if (hdl < 1.0) risk += 1

if (smoking) risk += 2
if (diabetes) risk += 2
if (family_history_cvd) risk += 1
if (age >= 55) risk += 1

if (risk >= 5) cvd_risk = "high"
else if (risk >= 3) cvd_risk = "moderate"
else cvd_risk = "low"
```

#### 2. Generate risk assessment report

```
📊 Menopause Health Risk Assessment

Risk assessment date: December 31, 2025

Osteoporosis risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk level: Low-moderate 🟡

Risk factor analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ T-score -1.5 (osteopenia) +1 point
✅ Age 48 (perimenopause) +0 points
✅ BMI 22.5 (normal) +0 points
✅ No smoking history +0 points
✅ No family history +0 points
✅ No long-term steroid use +0 points

Total: 1 point
Risk level: Low risk

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue calcium and vitamin D supplementation
✅ Regular weight-bearing exercise
✅ Bone density recheck in 1-2 years
✅ Fall prevention measures

Cardiovascular risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk level: Low 🟢

Risk factor analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Blood pressure 120/80 (normal) +0 points
⚠️ Lipids not tested - supplementation needed
⚠️ Blood sugar not tested - supplementation needed
✅ No smoking history +0 points
✅ No diabetes +0 points
✅ No family history of cardiovascular disease +0 points
✅ Age <55 +0 points

Known total: 0 points
Risk level: Low risk

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Get lipid and blood sugar tests soon
✅ Maintain healthy lifestyle
✅ Regular exercise
✅ Healthy diet
✅ Weight control
✅ Quit smoking, limit alcohol

Breast cancer risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk level: Average population risk 🟢

Risk factors:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No family history
✅ Not on HRT
✅ Reproductive history (needs updating)
✅ Age at first period (needs updating)
✅ No benign breast disease

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Monthly breast self-exam
✅ Annual clinical breast examination
✅ Annual breast ultrasound or mammogram
✅ Healthy lifestyle

Comprehensive health recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Priority 1 - Immediate action:
📅 Schedule annual checkup
  • Full lipid panel
  • Fasting blood glucose
  • Liver and kidney function
  • Breast exam

Priority 2 - Continue consistently:
✅ Calcium 1000mg/day
✅ Vitamin D 2000 IU/day
✅ Exercise 3-4 times/week
✅ Healthy diet

Priority 3 - Consider consulting:
👩‍⚕️ Gynecologic endocrinologist
  • Evaluate HRT needs
  • Symptom management plan
  • Bone health assessment

⚠️ Important disclaimer:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This risk assessment is for reference only and cannot replace professional medical evaluation.

Recommended annual comprehensive health checkup,
including bone density, cardiovascular, breast, and other examinations.

If in doubt, consult your doctor.
```

---

## Data Structure

### Main file: data/menopause-tracker.json

```json
{
  "created_at": "2025-12-31T12:00:00.000Z",
  "last_updated": "2025-12-31T12:00:00.000Z",

  "menopause_tracking": {
    "menopause_id": "menopause_20250101",
    "stage": "perimenopausal",
    "age": 48,
    "last_menstrual_period": "2025-11-15",
    "months_since_lmp": 1,
    "irregular_periods": true,
    "period_frequency": "every 2-3 months",

    "symptoms": {
      "hot_flashes": {},
      "night_sweats": {},
      "sleep_issues": {},
      "mood_changes": {},
      "vaginal_dryness": {},
      "joint_pain": {}
    },

    "symptom_history": [],

    "hrt": {},

    "bone_density": {},

    "cardiovascular_risk": {},

    "lifestyle": {},

    "metadata": {
      "created_at": "2025-01-01T00:00:00.000Z",
      "last_updated": "2025-12-31T00:00:00.000Z"
    }
  },

  "statistics": {
    "tracking_duration_months": 11,
    "total_symptom_records": 25,
    "symptom_trend": "stable",
    "hrt_use": false,
    "bone_density_tests": 1
  },

  "settings": {
    "reminder_frequency": "monthly",
    "symptom_tracking_frequency": "weekly"
  }
}
```

### Detailed records file: data/menopause-records/YYYY-MM/YYYY-MM-DD_symptom-log.json

```json
{
  "menopause_id": "menopause_20250101",
  "record_date": "2025-12-01",
  "stage": "perimenopausal",

  "symptoms": {
    "hot_flashes": {
      "frequency_count": 7,
      "severity_level": 2,
      "score": 14
    },
    "sleep_issues": {
      "sleep_quality": "poor",
      "score": 4
    }
  },

  "symptom_burden_score": 65,

  "notes": "",
  "metadata": {
    "created_at": "2025-12-01T20:00:00.000Z",
    "last_updated": "2025-12-01T20:00:00.000Z"
  }
}
```

---

## Smart Recognition Rules

### Stage recognition

| User input | Extracted result |
|------------|-----------------|
| 48 years old | age: 48 |
| last period November 15 | LMP: 2025-11-15 |
| last menstrual period November 15, 2025 | LMP: 2025-11-15 |

### Symptom type recognition

| Keywords | Symptom |
|----------|---------|
| hot flashes, sweating | hot_flashes |
| night sweats | night_sweats |
| insomnia, sleep | sleep_issues |
| mood, anxiety, depression, irritability | mood_changes |
| vaginal dryness | vaginal_dryness |
| joint pain, bone pain | joint_pain |

### Severity recognition

| Mild | Moderate | Severe |
|------|----------|--------|
| mild, slight | moderate | severe, serious |
| 1-2 times | 3-5 times | >5 times |

### Frequency recognition

| User input | Standardized |
|------------|-------------|
| 5-10 times daily | 5-10_per_day |
| 3-4 times nightly | 3-4_per_night |
| often | often |
| occasionally | occasional |

### HRT medication recognition

| Keywords | Medication type |
|----------|----------------|
| estradiol, estrogen | estrogen |
| progesterone, progestogen | progesterone |
| 1mg, 2mg | dose |
| oral, patch, gel | route |

### T-score recognition

| User input | T-score |
|------------|---------|
| -1.5 | -1.5 |
| negative 1.5 | -1.5 |
| minus 1.5 | -1.5 |

---

## Error Handling

| Scenario | Error message | Suggestion |
|----------|--------------|------------|
| No menopause record | No menopause tracking record<br>Please use /menopause start first | Guide to start recording |
| Age out of range | Age should be between 40-65 | Show valid range |
| Future date | Date cannot be in the future<br>Please check date input | Validate current date |
| Unrecognized symptom | Unrecognized symptom type<br>Supported: hot flashes, sleep, mood, joint pain | List supported types |
| T-score format error | T-score format error<br>Correct format: -1.5, negative 1.5 | Provide correct format |

---

## Notes

- This system is for menopause health tracking only and cannot replace professional medical advice
- HRT treatment must be conducted under medical supervision
- Regular bone density checks (every 1-2 years)
- Monitor cardiovascular health
- Seek medical care for severe symptoms
- All data is stored locally only

**Situations requiring immediate medical attention:**
- Abnormal vaginal bleeding
- Severe depression or suicidal tendencies
- New breast lump
- Severe cardiovascular symptoms
- Fracture or severe bone pain

---

## Example Usage

```
# Start menopause tracking
/menopause start 48 2025-11-15

# Record symptoms
/menopause symptom hot-flashes 5-10 moderate
/menopause symptom sleep insomnia
/menopause symptom mood anxiety

# Record HRT
/menopause hrt start estradiol 1mg
/menopause hrt effectiveness good

# Record bone density
/menopause bone -1.5 osteopenia

# View status
/menopause status

# Risk assessment
/menopause risk
```
