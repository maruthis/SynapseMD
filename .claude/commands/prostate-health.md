---
description: Prostate health management and PSA monitoring
arguments:
  - name: action
    description: "Action type: psa (PSA test) / ipss (IPSS score) / dre (digital rectal exam) / ultrasound (ultrasound) / status (status) / screening (screening plan) / risk (risk assessment)"
    required: true
  - name: info
    description: Prostate health information (PSA value, symptoms, exam results, etc., in natural language)
    required: false
---

# Prostate Health Management

Prostate health tracking and management, including PSA monitoring, IPSS symptom scoring, prostate examination planning, and risk assessment.

## Action Types

### 1. Record PSA Test - `psa`

Record prostate-specific antigen (PSA) test results, including total PSA and free PSA.

**Parameter description:**
- `info`: PSA test results (required)
  - Total PSA value: number (e.g. 2.5)
  - Free PSA value: number (optional, e.g. 0.8)
  - Test date: YYYY-MM-DD (optional, defaults to today)

**Examples:**
```
/prostate psa 2.5
/prostate psa 2.5 free 0.8
/prostate psa total 2.5 free 0.8
/prostate psa 2.5 2025-06-15
/prostate psa 4.2 free 0.9
```

**Execution steps:**

#### 1. Parse PSA Information

**PSA value recognition:**
```javascript
// User input: "PSA 2.5" or "total PSA 2.5 ng/mL"
patterns = [
  /psa[:\s]*(\d+\.?\d*)/i,
  /total\s*psa[:\s]*(\d+\.?\d*)/i,
  /prostate.specific.antigen[:\s]*(\d+\.?\d*)/i
]
```

**Free PSA recognition:**
- "free 0.8", "free PSA 0.8", "fpsa 0.8"

#### 2. Validate Input

**Checks:**
- PSA value should be within a reasonable range (0–100 ng/mL)
- Free PSA cannot be greater than total PSA
- Date cannot be a future date

#### 3. PSA Risk Assessment

**PSA value classification:**
```javascript
if (psa > 10) {
  risk = "high"
  message = "Recommend immediate urology consultation"
} else if (psa > 4) {
  risk = "moderate"
  message = "Recommend follow-up in 3 months"
} else if (psa > 2.5 && age > 50) {
  risk = "low-moderate"
  message = "Recommend regular monitoring"
} else {
  risk = "low"
  message = "Continue routine screening"
}
```

**Free-to-total PSA ratio:**
```javascript
f_psa_ratio = free_psa / total_psa

if (f_psa_ratio > 0.25) {
  interpretation = "Suggests benign"
} else if (f_psa_ratio < 0.10) {
  interpretation = "Malignancy cannot be excluded"
} else {
  interpretation = "Gray zone; comprehensive evaluation needed"
}
```

#### 4. Calculate PSA Velocity (PSAV)

If historical PSA data is available:
```javascript
psav = (current_psa - previous_psa) / months_between

if (psav > 0.75) {
  alert = "PSA rising too fast; further evaluation needed"
}
```

#### 5. Update PSA Record

**PSA data structure:**
```json
{
  "psa_history": [
    {
      "date": "2025-06-15",
      "total_psa": 2.5,
      "free_psa": 0.8,
      "ratio": 0.32,
      "reference": "<4.0",
      "unit": "ng/mL",
      "trend": "stable",
      "risk_level": "low",
      "interpretation": "Normal"
    }
  ]
}
```

#### 6. Output Confirmation

**Normal PSA:**
```
✅ PSA test recorded

PSA information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test date: June 15, 2025
Total PSA: 2.5 ng/mL ✓
Free PSA: 0.8 ng/mL
Free / Total ratio: 32% ✓

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk level: Low ✅
Reference value: < 4.0 ng/mL

Interpretation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
PSA value is within the normal range.
Free / Total ratio > 25%, suggesting benign.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue routine screening
✅ Next test: in 1 year
✅ Maintain a healthy lifestyle

⚠️ Important note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is for reference only and cannot replace professional medical advice.
If you have a family history of prostate cancer, consult a urologist
to develop a personalized screening plan.

Data saved to: data/prostate-records/2025-06/2025-06-15_PSA-test.json
```

**Elevated PSA warning:**
```
⚠️ Elevated PSA Alert

PSA information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total PSA: 5.2 ng/mL ⚠️
Free PSA: 0.9 ng/mL
Free / Total ratio: 17% ⚠️

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
PSA value above reference (4.0 ng/mL)
Free / Total ratio < 25%; further evaluation advised

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏥 Consult a urologist
📋 Repeat PSA in 3 months
📋 Include free PSA at follow-up
📋 Prostate ultrasound may be needed

🚨 Do not panic:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Elevated PSA does not mean prostate cancer.
Benign prostatic hyperplasia (BPH), prostatitis,
and urinary tract infections can all raise PSA.

Please consult a urologist for a thorough evaluation.

Data saved
```

---

### 2. IPSS Symptom Score - `ipss`

Complete the International Prostate Symptom Score (IPSS) to assess the severity of prostate symptoms.

**Parameter description:**
- No parameters (interactive scoring)

**Examples:**
```
/prostate ipss
```

**Execution steps:**

#### 1. IPSS Questionnaire System

The IPSS includes 7 questions, each scored 0–5:

**1. Incomplete emptying:**
- 0: Not at all
- 1: Less than 1 in 5 times
- 2: Less than half the time
- 3: About half the time
- 4: More than half the time
- 5: Almost always

**2. Frequency:**
- 0: Not at all
- 1: Less than 1 in 5 times
- 2: Less than half the time
- 3: About half the time
- 4: More than half the time
- 5: Almost always

**3. Intermittency:**
- Same scoring as above

**4. Urgency:**
- Same scoring as above

**5. Weak stream:**
- Same scoring as above

**6. Straining:**
- Same scoring as above

**7. Nocturia:**
- 0: None
- 1: 1 time
- 2: 2 times
- 3: 3 times
- 4: 4 times
- 5: ≥5 times

#### 2. Symptom Severity Classification

| Total score | Severity | Management recommendation |
|------------|----------|--------------------------|
| 0–7 | Mild | Watchful waiting |
| 8–19 | Moderate | Consider medical therapy |
| 20–35 | Severe | Urology evaluation recommended |

#### 3. Update IPSS Record

**IPSS data structure:**
```json
{
  "ipss_score": {
    "date": "2025-06-20",
    "incomplete_emptying": 1,
    "frequency": 2,
    "intermittency": 1,
    "urgency": 2,
    "weak_stream": 1,
    "straining": 0,
    "nocturia": 2,
    "total_score": 9,
    "severity": "moderate",
    "quality_of_life_score": 2
  }
}
```

#### 4. Output Confirmation

```
✅ IPSS score completed

IPSS score results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Scoring date: June 20, 2025

Symptom scores:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Incomplete emptying: 1 point
Frequency: 2 points
Intermittency: 1 point
Urgency: 1 point
Weak stream: 1 point
Straining: 0 points
Nocturia: 2 times (2 points)

Total score: 9 / 35 points
Severity: Moderate ⚠️

Quality of life score: 2 / 6 points
(Mostly satisfied overall)

Symptom analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Moderate prostate symptoms,
main manifestations:
- Increased urinary frequency
- Nocturia 2 times
- Mild difficulty urinating

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Watchful waiting
✅ Avoid drinking fluids before bedtime
✅ Reduce caffeine and alcohol
✅ Double-voiding technique

⚠️ Consider seeing a doctor:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If symptoms persist or worsen,
consult a urologist to evaluate whether medication is needed.

Available medications (prescription required):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Alpha-blockers (tamsulosin, etc.)
• 5-alpha reductase inhibitors (finasteride, etc.)
• Herbal extracts (saw palmetto, etc.)

⚠️ Important note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Medications must be used under physician guidance.
This system is for reference only and cannot replace a prescription.

Data saved to: data/prostate-records/2025-06/2025-06-20_IPSS-score.json
```

---

### 3. Record Digital Rectal Exam - `dre`

Record digital rectal examination (DRE) results.

**Parameter description:**
- `info`: DRE examination results (required)
  - Prostate size: normal, enlarged
  - Texture: soft, firm, nodular
  - Nodule: none, present
  - Tenderness: none, present

**Examples:**
```
/prostate dre normal
/prostate dre enlarged firm
/prostate dre nodule present
/prostate dre enlarged firm nodule present
```

**Execution steps:**

#### 1. Parse DRE Information

**Examination result recognition:**
```javascript
// Size
size_keywords = {
  "normal": "normal",
  "enlarged": "enlarged",
  "swollen": "enlarged"
}

// Texture
texture_keywords = {
  "soft": "soft",
  "firm": "firm",
  "nodular": "nodular",
  "smooth": "smooth"
}

// Nodule
nodule_keywords = {
  "no nodule": false,
  "none": false,
  "nodule present": true,
  "present": true,
  "nodule": true
}
```

#### 2. DRE Result Assessment

**Normal DRE:**
- Prostate size normal
- Uniform, soft texture
- No nodules
- No tenderness

**Abnormal warning signs:**
- Prostate nodule
- Firm texture
- Fixed, immobile
- Marked tenderness

#### 3. Update DRE Record

**DRE data structure:**
```json
{
  "dre": {
    "last_exam": "2025-06-15",
    "findings": "enlarged_firm",
    "size": "enlarged",
    "texture": "firm",
    "nodule": true,
    "tenderness": false,
    "mobility": "normal",
    "notes": ""
  }
}
```

#### 4. Output Confirmation

**Normal DRE:**
```
✅ Digital rectal exam recorded

DRE examination information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Exam date: June 15, 2025

Findings:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Prostate size: Normal ✓
Texture: Soft, uniform ✓
Nodule: None ✓
Tenderness: None ✓

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Digital rectal exam is normal; no abnormalities found.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue routine screening
✅ Next DRE: in 1 year
✅ Evaluate together with PSA results

⚠️ Important note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
A normal DRE cannot rule out prostate cancer.
Comprehensive evaluation with PSA and prostate
ultrasound is needed.

Data saved
```

**Abnormal DRE warning:**
```
⚠️ Abnormal Digital Rectal Exam Alert

DRE examination information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Exam date: June 15, 2025

Findings:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Prostate size: Enlarged
Texture: Firm ⚠️
Nodule: Present ⚠️
Tenderness: None

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Abnormalities found on digital rectal exam:
• Prostate texture has become firm
• Palpable nodule

🚨 Seek medical attention promptly:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Consult a urologist immediately!

Further evaluation may include:
• PSA test (if not already done)
• Prostate ultrasound
• Prostate MRI
• Prostate biopsy

⚠️ Do not delay:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Abnormal DRE requires further urology evaluation.
Early detection and early treatment are very important.

Please seek medical attention promptly!

Data saved
```

---

### 4. Record Prostate Ultrasound - `ultrasound`

Record prostate ultrasound examination results.

**Parameter description:**
- `info`: Ultrasound results (required)
  - Prostate volume: number + ml (e.g. 32ml)
  - Inner gland size: number + cm (e.g. 2.5cm)
  - Post-void residual urine: number + ml (optional)
  - Nodule: none, present

**Examples:**
```
/prostate ultrasound 32ml
/prostate ultrasound volume 32ml inner gland 2.5cm
/prostate ultrasound 45ml nodule present
/prostate ultrasound volume 45ml nodule present
```

**Execution steps:**

#### 1. Parse Ultrasound Information

**Volume recognition:**
- "32ml", "32 ml", "volume 32ml"
- "45ml"

**Inner gland size recognition:**
- "inner gland 2.5cm", "transition zone 2.5cm"

**Post-void residual urine recognition:**
- "residual urine 20ml", "PVR 20ml"

#### 2. Prostate Volume Assessment

**Prostate volume classification:**
| Volume | Classification |
|--------|---------------|
| < 20 mL | Small |
| 20–30 mL | Normal |
| 30–50 mL | Mildly enlarged |
| 50–80 mL | Moderately enlarged |
| > 80 mL | Severely enlarged |

**Prostate weight estimation:**
```
Prostate weight (g) = Prostate volume (mL) × 1.05
```

#### 3. Update Ultrasound Record

**Ultrasound data structure:**
```json
{
  "prostate_volume": {
    "date": "2025-06-15",
    "volume_ml": 32,
    "weight_g": 33.6,
    "inner_gland_cm": 2.5,
    "residual_urine_ml": 20,
    "nodule": false,
    "calcification": false,
    "interpretation": "mild_enlargement"
  }
}
```

#### 4. Output Confirmation

```
✅ Prostate ultrasound recorded

Ultrasound examination information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Exam date: June 15, 2025

Prostate parameters:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Volume: 32 mL ⚠️
Estimated weight: 33.6 g
Inner gland size: 2.5 cm
Post-void residual urine: 20 mL

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Mild prostate enlargement (BPH Grade I)
Enlarged inner gland proportion

Mildly increased post-void residual urine;
possible bladder outlet obstruction.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Monitor prostate volume regularly
✅ Monitor IPSS symptom changes
✅ Avoid holding urine
✅ Void at regular intervals

⚠️ Consider seeing a doctor:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Consult a urologist to evaluate:
• Whether medication is needed
• Monitor the rate of prostate growth
• Assess bladder function

Available medications (prescription required):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Alpha-blockers: improve urinary symptoms
• 5-alpha reductase inhibitors: shrink prostate

⚠️ Important note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Medications require a prescription and physician guidance.

Data saved
```

---

### 5. View Status - `status`

Display prostate health tracking status.

**Parameter description:**
- No parameters

**Examples:**
```
/prostate status
```

**Execution steps:**

#### 1. Read Prostate Data

#### 2. Generate Status Report

```
📍 Prostate Health Status

Basic information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Age: 55 years old
Family history: Father had prostate cancer (diagnosed at age 62)

PSA test history:
━━━━━━━━━━━━━━━━━━━━━━━━━━
2025-06-15: 2.5 ng/mL (Normal) ✓
2024-06-15: 2.4 ng/mL (Normal) ✓
2023-06-15: 2.3 ng/mL (Normal) ✓

PSA trend: Stable ✅
PSA velocity: 0.1 ng/mL/year (Normal) ✅

IPSS score:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Most recent score: 2025-06-20
Total: 9 / 35 points (Moderate)
Main symptoms: Nocturia 2 times, mild urinary difficulty

Prostate examinations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Digital rectal exam (2025-06-15): Enlarged, uniform texture, no nodules
Prostate volume (2025-03-15): 32 mL (mildly enlarged)

Current status assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PSA normal and stable
⚠️ Mild benign prostatic hyperplasia (BPH Grade I)
⚠️ Moderate urinary symptoms

Risk factors:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Family history: Father had prostate cancer
• Age: 55 years (increased risk)
• Prostate enlargement: Mild

Screening plan:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PSA test: annually
  Next: 2026-06-15
✅ Digital rectal exam: annually
  Next: 2026-06-15

Recommended actions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue annual PSA screening
✅ Monitor changes in urinary symptoms
✅ Consider consulting a urologist:
  - Evaluate whether BPH medication is needed
  - Discuss screening strategy given family history

💡 This week's focus:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Keep a urinary diary
• Avoid drinking fluids before bedtime
• Reduce caffeine and alcohol
• Double-voiding technique

⚠️ Important notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is for prostate health tracking only and cannot replace professional medical advice.

If symptoms worsen or PSA continues to rise, seek medical attention promptly.
```

---

### 6. View Screening Plan - `screening`

Display a prostate cancer screening plan and recommendations.

**Parameter description:**
- No parameters

**Examples:**
```
/prostate screening
```

**Execution steps:**

#### 1. Risk-Based Screening Plan

**Risk stratification:**

**Average risk:**
- No family history
- No symptoms
- Normal PSA

**High risk:**
- Family history (father or brother)
- African descent
- Age > 50

**Screening plan:**

| Risk category | Starting age | PSA test frequency | DRE frequency |
|--------------|-------------|-------------------|---------------|
| Average risk | 50 years | Annually | Every 2 years |
| High risk | 45 years | Annually | Annually |

#### 2. Generate Screening Plan

```
📋 Prostate Cancer Screening Plan

Personal information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Age: 55 years old
Risk category: High risk (family history)

Screening recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PSA test: annually
  Starting age: 45 years (10 years completed)
  Next test: 2026-06-15 (362 days away)

✅ Digital rectal exam (DRE): annually
  Next exam: 2026-06-15 (362 days away)

Optional tests:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Prostate ultrasound: when PSA is abnormal
📋 Prostate MRI: when PSA is persistently elevated
📋 Prostate biopsy: when recommended by urologist

Test preparation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
PSA test:
• 24–48 hours after ejaculation
• 48 hours after prostate massage
• 7 days after cystoscopy
• No acute urinary tract infection
• No urinary retention

Digital rectal exam:
• No special preparation needed
• Empty bladder before exam

Screening goals:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Early detection of prostate cancer
• Timely treatment to improve prognosis
• Monitor prostate health status

Benefits of early detection:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• 5-year survival rate for localized prostate cancer > 98%
• More treatment options available
• Better functional outcomes

Screening reminder settings:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Next test: 2026-06-15
Reminder time: 7 days before test
Reminder method: /prostate screening

⚠️ Important note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Screening cannot prevent prostate cancer,
but early detection can improve cure rates.

Discuss with a urologist:
• Benefits and risks of screening
• Personalized screening strategy
• Further tests when PSA is abnormal

Data saved
```

---

### 7. Risk Assessment - `risk`

Display a comprehensive prostate cancer risk assessment.

**Parameter description:**
- No parameters

**Examples:**
```
/prostate risk
```

**Execution steps:**

#### 1. Comprehensive Risk Assessment

**Risk factors:**
- Age
- Family history
- Ethnicity
- PSA level
- PSA velocity
- Abnormal DRE

**Risk calculation:**
```javascript
risk_score = 0

// Age
if (age >= 60) risk_score += 1
if (age >= 70) risk_score += 1

// Family history
if (family_history.father) risk_score += 2
if (family_history.brother) risk_score += 2

// PSA
if (psa > 4) risk_score += 2
if (psa > 10) risk_score += 3

// PSAV
if (psav > 0.75) risk_score += 2

// DRE
if (dre.nodule) risk_score += 3
if (dre.firm) risk_score += 1

if (risk_score >= 6) risk = "high"
else if (risk_score >= 3) risk = "moderate"
else risk = "low"
```

#### 2. Generate Risk Assessment Report

```
📊 Prostate Cancer Risk Assessment

Assessment date: December 31, 2025

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk level: Moderate 🟡

Risk factor analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Age 55 years: +1 point
⚠️ Family history (father): +2 points
✅ PSA 2.5 ng/mL: +0 points
✅ PSAV 0.1 ng/mL/year: +0 points
✅ DRE no nodules: +0 points

Total: 3 points
Risk level: Moderate risk

Risk interpretation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary risk factor:
• Father has a history of prostate cancer

Protective factors:
• PSA normal and stable
• Normal DRE findings
• No significant symptoms

Screening recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue annual PSA screening
✅ Continue annual digital rectal exam
✅ Monitor PSA changes closely

⚠️ Be alert when:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• PSA is persistently rising
• Nodule found on DRE
• Urinary difficulty develops

Risk-reduction measures:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Healthy diet
  • More tomatoes (lycopene)
  • Cruciferous vegetables
  • Green tea
  • Less red meat

✅ Regular exercise
  • 150 minutes of moderate-intensity exercise per week
  • Aerobic exercise

✅ Weight control
  • BMI < 25

✅ Quit smoking; limit alcohol
  • No smoking
  • Limit alcohol intake

Genetic counseling recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Those with a family history may consider:
• Genetic testing (BRCA2, etc.)
• Starting screening earlier (ages 40–45)
• More frequent monitoring

⚠️ Important note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This risk assessment is for reference only and cannot replace a professional medical evaluation.

Those with a family history are advised to consult a urologist or oncologist
to develop a personalized screening and prevention strategy.

Annual risk assessment updates are recommended.

Data saved
```

---

## Data Structure

### Main file: data/prostate-tracker.json

```json
{
  "created_at": null,
  "last_updated": null,

  "prostate_health": {
    "user_id": null,
    "age": null,
    "family_history": {
      "father": false,
      "brother": false,
      "age_at_diagnosis": null
    },

    "psa_history": [],
    "psa_velocity": {
      "change_per_year": null,
      "threshold": 0.75,
      "interpretation": null
    },

    "ipss_score": {
      "date": null,
      "incomplete_emptying": null,
      "frequency": null,
      "intermittency": null,
      "urgency": null,
      "weak_stream": null,
      "straining": null,
      "nocturia": null,
      "total_score": null,
      "severity": null,
      "quality_of_life_score": null
    },

    "prostate_volume": {
      "date": null,
      "volume_ml": null,
      "weight_g": null,
      "inner_gland_cm": null,
      "residual_urine_ml": null,
      "nodule": null,
      "interpretation": null
    },

    "dre": {
      "last_exam": null,
      "findings": null,
      "size": null,
      "texture": null,
      "nodule": null,
      "tenderness": null,
      "notes": null
    },

    "screening_plan": {
      "psa_frequency": null,
      "dre_frequency": null,
      "next_psa": null,
      "next_dre": null,
      "risk_category": null
    },

    "urinary_symptoms": {
      "stream_weakness": null,
      "frequency": null,
      "nocturia": null,
      "urgency": null
    }
  },

  "statistics": {
    "total_psa_tests": 0,
    "last_psa_date": null,
    "psa_trend": "stable",
    "ipss_severity": null,
    "tracking_duration_months": 0
  },

  "settings": {
    "reminder_frequency": "annual",
    "screening_reminder": true
  }
}
```

### Detailed records: data/prostate-records/YYYY-MM/YYYY-MM-DD_PSA-test.json

```json
{
  "record_id": "prostate_20250615_001",
  "record_type": "PSA test",
  "date": "2025-06-15",

  "psa_result": {
    "total_psa": 2.5,
    "free_psa": 0.8,
    "ratio": 0.32,
    "unit": "ng/mL",
    "reference": "<4.0",
    "lab": null
  },

  "interpretation": {
    "risk_level": "low",
    "trend": "stable",
    "clinical_significance": "Normal"
  },

  "notes": "",
  "metadata": {
    "created_at": "2025-06-15T10:00:00.000Z",
    "last_updated": "2025-06-15T10:00:00.000Z"
  }
}
```

---

## Intelligent Recognition Rules

### PSA Value Recognition

| User input | Extracted result |
|-----------|-----------------|
| PSA 2.5 | total_psa: 2.5 |
| total PSA 2.5 | total_psa: 2.5 |
| prostate-specific antigen 2.5 | total_psa: 2.5 |
| psa 4.2 free 0.9 | total: 4.2, free: 0.9 |

### IPSS Symptom Recognition

| Symptom | Keywords | Score |
|---------|----------|-------|
| Incomplete emptying | incomplete emptying, not empty | 1–5 |
| Frequency | urinary frequency, frequent urination | 1–5 |
| Nocturia | nocturia, nighttime urination | 0–5 |

### DRE Result Recognition

| Keyword | Result |
|---------|--------|
| normal | normal |
| enlarged, swollen | enlarged |
| firm, hard | firm |
| nodule | nodule present |
| soft | soft |

---

## Error Handling

| Scenario | Error message | Recommendation |
|---------|--------------|----------------|
| PSA value missing | PSA value cannot be empty; please provide a PSA test value | Indicate correct format |
| PSA value out of range | PSA value is outside a reasonable range; please check input | Show valid range |
| Free PSA greater than total PSA | Free PSA cannot exceed total PSA; please check data | Indicate logical error |
| Date error | Date cannot be in the future; please check the date entry | Validate current date |

---

## Notes

- This system is for prostate health tracking only and cannot replace professional medical advice
- Elevated PSA does not mean prostate cancer; a comprehensive evaluation is needed
- Regular screening is very important for early detection of prostate cancer
- Those with a family history need more frequent monitoring
- Any changes in urinary symptoms should be evaluated by a doctor promptly

**Situations requiring immediate medical attention:**
- Significantly elevated PSA (>10 ng/mL)
- Prostate nodule found on DRE
- Severe urinary difficulty or urinary retention
- Blood in urine
- Bone pain (suspected metastasis)

All data is stored locally only to ensure privacy.

---

## Example Usage

```
# Record PSA test
/prostate psa 2.5
/prostate psa 2.5 free 0.8
/prostate psa history

# IPSS score
/prostate ipss

# Record examinations
/prostate dre normal
/prostate ultrasound 32ml

# View status
/prostate status
/prostate screening
/prostate risk
```
