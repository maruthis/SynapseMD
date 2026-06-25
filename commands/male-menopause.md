---
description: Male andropause (hypogonadism) management
arguments:
  - name: action
    description: "Action type: symptom (symptoms) / testosterone (testosterone) / adam (ADAM questionnaire) / trt (TRT treatment) / monitor (monitoring) / status (status) / diagnosis (diagnosis)"
    required: true
  - name: info
    description: Andropause information (symptoms, testosterone levels, treatment status, etc., in natural language)
    required: false
---

# Male Andropause Management

Male andropause (hypogonadism) tracking and management, including symptom assessment, testosterone monitoring, and TRT treatment records.

## Action Types

### 1. Record Symptoms - `symptom`

Record male andropause symptoms.

**Parameter Description:**
- `info`: Symptom description (required)
  - Symptom types: libido (sexual desire) / erectile (erectile function) / fatigue (fatigue) / mood (mood) / memory (memory) / sleep (sleep)
  - Severity: mild / moderate / severe

**Examples:**
```
/andropause symptom libido decreased
/andropause symptom erectile mild
/andropause symptom fatigue moderate
/andropause symptom mood depressed
/andropause symptom memory poor
```

**Execution Steps:**

#### 1. Symptom Classification

**Sexual Symptoms:**
- Decreased libido
- Erectile dysfunction (ED)
- Reduced erectile quality
- Reduced or absent morning erections

**Physical Symptoms:**
- Decreased physical strength
- Easy fatigue
- Decreased muscle mass
- Increased fat (especially abdominal)
- Decreased bone density
- Hot flashes, night sweats

**Psychological Symptoms:**
- Depressed mood
- Irritability
- Anxiety
- Decreased memory
- Difficulty concentrating
- Lack of motivation

#### 2. Symptom Severity Assessment

**Mild:**
- Symptoms are minor, do not affect daily life
- Occur occasionally

**Moderate:**
- Symptoms are noticeable, affect quality of life
- Occur frequently

**Severe:**
- Symptoms are severe, significantly affect daily life
- Persistent

#### 3. Update Symptom Records

**Symptom Data Structure:**
```json
{
  "symptoms": {
    "sexual": {
      "libido": {
        "present": true,
        "severity": "moderate",
        "impact": "noticeable"
      },
      "erectile_function": {
        "present": true,
        "severity": "mild",
        "morning_erection": "reduced"
      }
    },
    "physical": {
      "fatigue": {
        "present": true,
        "severity": "moderate",
        "impact_on_activities": "some"
      },
      "muscle_mass": {
        "present": true,
        "severity": "mild",
        "changes": "slight_decrease"
      },
      "body_fat": {
        "present": true,
        "severity": "moderate",
        "distribution": "abdominal"
      },
      "hot_flashes": {
        "present": false
      }
    },
    "psychological": {
      "mood": {
        "present": true,
        "symptoms": ["depressed", "irritability"],
        "severity": "mild"
      },
      "memory": {
        "present": true,
        "severity": "mild",
        "complaints": "occasional_forgetfulness"
      },
      "concentration": {
        "present": true,
        "severity": "moderate",
        "impact": "noticeable"
      }
    }
  }
}
```

#### 4. Output Confirmation

```
✅ Symptoms Recorded

Symptom Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Record Date: December 31, 2025

Sexual Symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Decreased libido (moderate)
• Mild decline in erectile function
• Reduced morning erections

Physical Symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Easy fatigue (moderate)
• Mild decrease in muscle mass
• Increased abdominal fat (moderate)

Psychological Symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Depressed mood, irritability (mild)
• Decreased memory (mild)
• Difficulty concentrating (moderate)

Symptom Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Multi-system symptoms present,
consistent with male andropause.

Symptom Burden:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Sexual symptoms: Moderate impact
Physical symptoms: Moderate impact
Psychological symptoms: Mild impact

Overall symptom burden: Moderate

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Recommend testing testosterone levels
✅ Complete ADAM questionnaire assessment
✅ Evaluate whether TRT treatment is needed
✅ Lifestyle adjustments

Lifestyle Adjustments:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Regular exercise (strength training)
✅ Adequate sleep (7-8 hours)
✅ Healthy diet
✅ Weight management
✅ Quit smoking and limit alcohol
✅ Stress management

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Symptoms do not equal testosterone deficiency.

Recommend testing testosterone levels
combined with symptoms for comprehensive assessment.

Data synchronized to symptom records
```

---

### 2. Record Testosterone Levels - `testosterone`

Record testosterone test results.

**Parameter Description:**
- `info`: Testosterone test results (required)
  - Total testosterone value: number
  - Measurement time: HH:mm (optional, e.g., 09:00)
  - Measurement date: YYYY-MM-DD (optional)

**Examples:**
```
/andropause testosterone 7.5
/andropause testosterone 7.5 09:00
/andropause testosterone 15.3
/andropause testosterone total_testosterone 7.5 morning_9am
```

**Execution Steps:**

#### 1. Parse Testosterone Information

**Testosterone Recognition:**
```javascript
patterns = [
  /testosterone[:\s]+(\d+\.?\d*)/i,
  /total_testosterone[:\s]+(\d+\.?\d*)/i
]
```

**Measurement Time Recognition:**
- "09:00", "morning_9am", "morning"

#### 2. Testosterone Level Assessment

**Total Testosterone Reference Values:**
- Normal: 10-35 nmol/L
- Possible hypogonadism: 8-10 nmol/L
- Confirmed hypogonadism: < 8 nmol/L (requires repeated testing)

**Measurement Time Requirements:**
- Morning measurements (8-11 AM) are most accurate
- At least 2 measurements needed for confirmation
- Interval between measurements >1 week

#### 3. Testosterone Classification

**Hypogonadism Grading:**
```javascript
if (total_testosterone < 8) {
  grade = "confirmed"
  diagnosis = "Hypogonadism"
  recommendation = "Consider TRT treatment"
} else if (total_testosterone < 10) {
  grade = "possible"
  diagnosis = "Possible hypogonadism"
  recommendation = "Assess with symptoms, repeat testing"
} else if (total_testosterone < 12 && symptoms_present) {
  grade = "borderline"
  diagnosis = "Borderline hypogonadism"
  recommendation = "Monitor symptoms, regular follow-up"
} else {
  grade = "normal"
  diagnosis = "Normal testosterone levels"
  recommendation = "Look for other causes of symptoms"
}
```

#### 4. Update Testosterone Records

**Testosterone Data Structure:**
```json
{
  "testosterone_levels": {
    "total_testosterone": {
      "date": "2025-06-15",
      "time": "09:00",
      "value": 7.5,
      "reference": "10-35",
      "unit": "nmol/L",
      "result": "low",
      "confirmed": true,
      "repeat_count": 2,
      "lab": null
    },
    "free_testosterone": {
      "date": "2025-06-15",
      "value": 0.18,
      "reference": "0.22-0.65",
      "unit": "nmol/L",
      "result": "low"
    },
    "shbg": {
      "date": "2025-06-15",
      "value": 45,
      "reference": "20-50",
      "unit": "nmol/L",
      "result": "normal"
    }
  }
}
```

#### 5. Output Confirmation

**Low Testosterone:**
```
✅ Testosterone Testing Recorded

Testosterone Test Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Date: June 15, 2025
Measurement Time: 09:00 ✓ (morning)

Testosterone Levels:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Testosterone: 7.5 nmol/L ⚠️ (Reference: 10-35)
Free Testosterone: 0.18 nmol/L ⚠️ (Reference: 0.22-0.65)
SHBG: 45 nmol/L ✓ (Reference: 20-50)

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Total testosterone below normal
⚠️ Free testosterone below normal

Diagnosis: Hypogonadism (confirmed)
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total testosterone < 8 nmol/L
• Confirmed by 2 repeated measurements
• Requires comprehensive judgment combined with symptoms

TRT Treatment Recommendation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Symptoms + low testosterone = TRT treatment indication

Recommend evaluating TRT treatment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Consult endocrinology or urology
✅ Assess symptom severity
✅ Evaluate TRT benefits and risks
✅ Develop individualized treatment plan

Pre-TRT Tests:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 PSA test (prostate safety)
📋 Hematocrit (blood safety)
📋 Prostate ultrasound
📋 Cardiovascular risk assessment

TRT Treatment Methods:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Oral preparations
• Injection preparations
• Gel preparations
• Patch preparations

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
TRT treatment must be performed under physician guidance!

Regular monitoring of side effects required:
• PSA changes
• Hematocrit
• Prostate volume
• Cardiovascular events

Please consult a professional physician!

Data saved to: data/andropause-records/2025-06/2025-06-15_testosterone-test.json
```

**Normal Testosterone:**
```
✅ Testosterone Testing Recorded

Testosterone Test Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Date: June 15, 2025
Measurement Time: 09:00 ✓

Testosterone Levels:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Testosterone: 15.3 nmol/L ✓ (Reference: 10-35)
Free Testosterone: 0.35 nmol/L ✓
SHBG: 40 nmol/L ✓

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Testosterone levels normal
✅ No hypogonadism

Symptom Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If symptoms are present but testosterone is normal,
possible causes include:
• Stress/anxiety
• Depression
• Thyroid dysfunction
• Chronic fatigue
• Sleep deprivation
• Other diseases

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Testosterone normal, TRT not needed
✅ Look for other causes of symptoms
✅ Consult physician for comprehensive evaluation
✅ Lifestyle adjustments

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
TRT treatment not recommended
(when testosterone is normal)

Recommend finding the true cause of symptoms.

Data saved
```

---

### 3. ADAM Questionnaire Assessment - `adam`

Perform ADAM (Androgen Deficiency in the Aging Male) questionnaire assessment.

**Parameter Description:**
- No parameters (interactive questionnaire)

**Examples:**
```
/andropause adam
```

**Execution Steps:**

#### 1. ADAM Questionnaire (10 Questions)

Answer "Yes" or "No" for each question:

1. **Is there a decrease in sex drive?**
2. **Do you feel a lack of energy?**
3. **Have you noticed a decrease in strength or endurance?**
4. **Have you lost height?**
5. **Have you noticed a decrease in enjoyment of life?**
6. **Are you sad or grumpy?**
7. **Are your erections less strong?**
8. **Have you noticed a recent deterioration in your ability to play sports?**
9. **Are you falling asleep after dinner?**
10. **Has there been a recent deterioration in your work performance?**

#### 2. ADAM Scoring Criteria

**Positive Criteria:**
- Questions 1 or 7 positive + any other question positive
- Or ≥3 questions positive

**Result Interpretation:**
- 0-2 questions "Yes": Negative
- ≥3 questions "Yes": Positive

#### 3. Update ADAM Records

**ADAM Data Structure:**
```json
{
  "questionnaire_scores": {
    "adam": {
      "date": "2025-06-20",
      "questions": [
        {"q1": "Is there a decrease in sex drive?", "answer": true, "score": 1},
        {"q2": "Do you feel a lack of energy?", "answer": true, "score": 1},
        {"q3": "Have you noticed a decrease in strength or endurance?", "answer": true, "score": 1},
        {"q4": "Have you lost height?", "answer": false, "score": 0},
        {"q5": "Have you noticed a decrease in enjoyment of life?", "answer": true, "score": 1},
        {"q6": "Are you sad or grumpy?", "answer": true, "score": 1},
        {"q7": "Are your erections less strong?", "answer": true, "score": 1},
        {"q8": "Have you noticed a recent deterioration in your ability to play sports?", "answer": false, "score": 0},
        {"q9": "Are you falling asleep after dinner?", "answer": false, "score": 0},
        {"q10": "Has there been a recent deterioration in your work performance?", "answer": false, "score": 0}
      ],
      "total_score": 7,
      "positive": true,
      "interpretation": "Suggests possible male andropause"
    }
  }
}
```

#### 4. Output Confirmation

```
✅ ADAM Questionnaire Completed

ADAM Questionnaire Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Assessment Date: June 20, 2025

Questionnaire Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ 1. Is there a decrease in sex drive? - Yes
✓ 2. Do you feel a lack of energy? - Yes
✓ 3. Have you noticed a decrease in strength or endurance? - Yes
  4. Have you lost height? - No
✓ 5. Have you noticed a decrease in enjoyment of life? - Yes
✓ 6. Are you sad or grumpy? - Yes
✓ 7. Are your erections less strong? - Yes
  8. Have you noticed a recent deterioration in your ability to play sports? - No
  9. Are you falling asleep after dinner? - No
  10. Has there been a recent deterioration in your work performance? - No

Total: 7/10 questions positive
Result: Positive ⚠️

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Questions 1 or 7 positive: Yes
✓ Other questions positive: 5

ADAM questionnaire positive, suggests possible
male andropause (hypogonadism).

Main Symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Decreased libido ✓
• Decreased physical strength ✓
• Decreased erectile function ✓
• Mood changes ✓

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Test testosterone levels (if not done)
✅ Comprehensive assessment combining symptoms and testosterone
✅ Consult endocrinology or urology

Next Steps:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Morning measurement of total and free testosterone
📋 Repeat measurement for confirmation (interval >1 week)
📋 Assessment combined with clinical symptoms

If testosterone is low + symptoms are obvious:
━━━━━━━━━━━━━━━━━━━━━━━━━━
TRT treatment may be needed
Please consult physician for evaluation

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
ADAM questionnaire is a screening tool,
cannot diagnose hypogonadism.

Requires comprehensive judgment combining
testosterone testing and clinical evaluation.

Data saved to: data/andropause-records/2025-06/2025-06-20_ADAM-questionnaire.json
```

---

### 4. TRT Treatment Records - `trt`

Record testosterone replacement therapy (TRT) status.

**Parameter Description:**
- `info`: TRT treatment information (required)
  - action: start / stop / effectiveness (effectiveness assessment) / side-effects
  - Medication information: type / dose / route

**Examples:**
```
/andropause trt start gel 50mg
/andropause trt start injection testosterone_ester
/andropause trt effectiveness good
/andropause trt side-effects breast_tenderness
/andropause trt stop
```

**Execution Steps:**

#### 1. TRT Type Recognition

**Medication Types:**
- **Oral**: Testosterone undecanoate
- **Injection**: Testosterone esters (e.g., testosterone enanthate, testosterone cypionate)
- **Gel**: Testosterone gel (1%)
- **Patch**: Testosterone patches

#### 2. TRT Treatment Assessment

**TRT Indications:**
- Total testosterone <8 nmol/L + symptoms
- Total testosterone 8-12 nmol/L + significant symptoms

**TRT Contraindications:**
- Prostate cancer
- Male breast cancer
- Untreated benign prostatic hyperplasia obstruction
- Polycythemia (Hct>54%)
- Severe sleep apnea

**Relative Contraindications:**
- Prostatic nodules
- High cardiovascular risk
- Abnormal liver function

#### 3. Efficacy Assessment

**Improvement Timeline:**
- Libido improvement: 3-6 weeks
- Erectile function: 6-12 weeks
- Mood improvement: 4-8 weeks
- Physical strength improvement: 8-12 weeks
- Muscle mass: 6-12 months
- Bone density: 2-3 years

#### 4. Side Effect Monitoring

**Side Effects Requiring Monitoring:**
- **Polycythemia**: Hct>54% requires suspension
- **Prostate**: PSA elevation >1 ng/mL requires evaluation
- **Cardiovascular events**: Monitor
- **Liver function**: Monitor
- **Breast tenderness**: Common, may be self-limiting

#### 5. Update TRT Records

**TRT Data Structure:**
```json
{
  "trt": {
    "on_treatment": true,
    "medication": "Testosterone Gel",
    "type": "gel",
    "dose": "50mg",
    "frequency": "daily",
    "route": "transdermal",
    "start_date": "2025-12-01",
    "duration_months": 1,
    "effectiveness": "good",
    "effectiveness_rating": 8,
    "effectiveness_notes": "Significant improvement in libido, improved physical strength",
    "side_effects": ["breast_tenderness"],
    "side_effects_severity": "mild",
    "quality_of_life_improvement": "significant",
    "notes": ""
  }
}
```

#### 6. Output Confirmation

**Starting TRT:**
```
✅ TRT Treatment Recorded

TRT Treatment Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Medication: Testosterone Gel
Type: Gel
Dosage: 50mg
Administration: Daily topical use
Start Date: December 1, 2025

Treatment Duration: 1 month

⚠️ TRT Treatment Safety Reminders
━━━━━━━━━━━━━━━━━━━━━━━━━━
Regular monitoring items:

✅ Breast examination (self-examination)
  • Watch for breast lumps
  • Watch for breast tenderness

✅ Prostate monitoring
  • PSA baseline value: recorded
  • Test PSA every 6-12 months
  • If PSA rises >1 ng/mL, seek medical attention

✅ Blood monitoring
  • Hematocrit (Hct)
  • Alert value: 54%
  • If Hct>54%, suspend treatment

✅ Cardiovascular monitoring
  • Monitor blood pressure
  • Watch for chest pain, difficulty breathing

⚠️ Warning Symptoms (Seek immediate medical attention):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Breast lumps or discharge
• Lower limb pain or swelling (DVT)
• Sudden chest pain or difficulty breathing (PE)
• Severe headache or vision changes
• Worsening difficulty urinating

Efficacy Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Expected improvement timeline:

• Libido improvement: 3-6 weeks
• Erectile function: 6-12 weeks
• Mood improvement: 4-8 weeks
• Physical strength improvement: 8-12 weeks
• Muscle mass: 6-12 months

💡 Reminder:
━━━━━━━━━━━━━━━━━━━━━━━━━━
TRT treatment must be performed under physician guidance!

This system only records treatment status
and cannot replace physician prescriptions and guidance.

Please use as directed and have regular follow-ups.

Data saved
```

**Effectiveness Assessment:**
```
✅ TRT Effectiveness Recorded

Efficacy Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Assessment Time: 3 months after starting TRT

Treatment Effectiveness: Good ⭐⭐⭐⭐
Rating: 8/10

Symptom Improvement:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Libido: Significant improvement
✓ Erectile function: Improved
✓ Mood: Better
✓ Physical strength: Improved
✓ Muscle mass: Mild increase
  Body fat: Mild decrease

Side Effects:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Breast tenderness (mild) - acceptable

Monitoring Indicators:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ PSA: Stable (2.0 → 2.1)
✓ Hct: Normal (45%)
✓ Prostate volume: No significant change

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ TRT treatment effective
✅ Side effects acceptable
✅ Benefits > risks, continue treatment

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue TRT treatment
✅ Regular monitoring (every 6 months)
✅ Report any new symptoms

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Efficacy assessment is for reference only;
please consult physician to adjust treatment plan.

Data saved
```

---

### 5. TRT Monitoring Indicators - `monitor`

Record monitoring indicators during TRT treatment.

**Parameter Description:**
- `info`: Monitoring indicators (required)
  - Indicator types: psa (PSA) / hematocrit / weight / prostate-volume
  - Values: numbers

**Examples:**
```
/andropause monitor psa 2.1
/andropause monitor hematocrit 46
/andropause monitor weight 75kg
/andropause monitor prostate-volume 30ml
```

**Execution Steps:**

#### 1. Monitoring Indicator Standards

**PSA Monitoring:**
- Baseline value: Measured before treatment
- Monitoring frequency: Every 6-12 months
- Alert value: Increase >1 ng/mL
- Absolute value: >4 ng/mL requires evaluation

**Hematocrit (Hct):**
- Normal: 41-50%
- Alert value: 54%
- Action: >54% suspend or reduce dose

**Prostate Volume:**
- Monitoring frequency: Annually
- Alert: Rapid volume increase

#### 2. Update Monitoring Records

**Monitoring Data Structure:**
```json
{
  "monitoring": {
    "psa": {
      "baseline": 2.0,
      "current": 2.1,
      "change": 0.1,
      "date": "2025-06-15",
      "interpretation": "stable"
    },
    "hematocrit": {
      "baseline": 45,
      "current": 46,
      "date": "2025-06-15",
      "threshold": 54,
      "status": "normal"
    },
    "prostate_volume": {
      "baseline": 28,
      "current": 29,
      "date": "2025-06-15",
      "change": "stable"
    }
  }
}
```

#### 3. Output Confirmation

```
✅ TRT Monitoring Indicators Recorded

Monitoring Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Monitoring Date: June 15, 2025
TRT Duration: 6 months

PSA Monitoring:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Baseline: 2.0 ng/mL
Current: 2.1 ng/mL
Change: +0.1 ng/mL
Assessment: Stable ✅

Hematocrit:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Baseline: 45%
Current: 46%
Alert value: 54%
Assessment: Normal ✅

Prostate Volume:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Baseline: 28 mL
Current: 29 mL
Change: Stable ✅

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All monitoring indicators stable
✅ No obvious TRT side effects
✅ Safe to continue treatment

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue TRT treatment
✅ Next monitoring: in 6 months
✅ Continue recording side effects

⚠️ Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Seek immediate medical attention if:
• PSA rises rapidly
• Hct > 54%
• Breast lumps
• Lower limb swelling and pain

Data saved
```

---

### 6. View Status - `status`

Display male andropause tracking status.

**Parameter Description:**
- No parameters

**Examples:**
```
/andropause status
```

**Execution Steps:**

#### 1. Read Andropause Data

#### 2. Generate Status Report

```
📍 Male Andropause Status

Basic Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Age: 52 years old
Assessment Date: December 31, 2025
Tracking Duration: 6 months

Symptom Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Sexual symptoms: Moderate
• Decreased libido ✓
• Mild decline in erectile function ✓

Physical symptoms: Moderate
• Easy fatigue ✓
• Decreased muscle mass ✓
• Increased abdominal fat ✓

Psychological symptoms: Mild
• Mood fluctuations ✓
• Mild memory decline ✓

Testosterone Levels:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Testosterone: 7.5 nmol/L ⚠️ (low)
Measurement Time: 09:00 (morning)
Confirmation Count: 2 times

Free Testosterone: 0.18 nmol/L ⚠️ (low)
SHBG: 45 nmol/L ✓

Questionnaire Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
ADAM Questionnaire: Positive (7/10 questions)
AMS Score: 27 points (moderate)

Diagnostic Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Low testosterone
✓ Obvious andropause symptoms
✓ ADAM questionnaire positive

Diagnosis: Hypogonadism (confirmed)

TRT Treatment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: Under treatment
Medication: Testosterone Gel 50mg/day
Start Date: December 1, 2025
Treatment Duration: 1 month

Effectiveness: Good ⭐⭐⭐⭐ (8/10)
Side Effects: Mild breast tenderness (acceptable)

Monitoring Indicators:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ PSA: Stable (2.0 → 2.1)
✓ Hct: Normal (46%)
✓ Prostate volume: No significant change

Recommended Actions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue TRT treatment
✅ Regular monitoring (every 6 months)
✅ Record symptom changes
✅ Report new side effects

💡 This Month's Focus:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Continue regular use of gel
• Record symptom improvements
• Watch for breast changes
• Maintain healthy lifestyle

Lifestyle Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Regular exercise (strength training)
✅ Adequate sleep
✅ Healthy diet
✅ Weight management
✅ Quit smoking and limit alcohol
✅ Social activities

⚠️ Important Statement:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is for andropause health tracking only and cannot replace professional medical advice.

TRT treatment must be performed under physician guidance!

Data saved
```

---

### 7. View Diagnosis - `diagnosis`

Display male andropause diagnosis and assessment.

**Parameter Description:**
- No parameters

**Examples:**
```
/andropause diagnosis
```

**Execution Steps:**

#### 1. Diagnostic Criteria

**Hypogonadism Diagnostic Criteria:**
- **Symptoms**: Typical symptoms present
- **Testosterone**: Total testosterone <8 nmol/L (repeated measurement)
- **Or**: Total testosterone 8-12 nmol/L + significant symptoms

**Confirmation Criteria:**
- Measured in the morning (8-11 AM)
- At least 2 measurements for confirmation
- Other diseases excluded

#### 2. Generate Diagnosis Report

```
📋 Male Andropause Diagnosis Report

Assessment Date: December 31, 2025

Diagnostic Basis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Typical andropause symptoms present
✓ Reduced total testosterone (<8 nmol/L)
✓ Confirmed by 2 repeated measurements
✓ Morning measurement meets standards

Diagnosis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Male Hypogonadism
Confirmed

Severity: Moderate

Testosterone Level Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Testosterone: 7.5 nmol/L ⚠️
  (Reference: 10-35 nmol/L)
  (Diagnostic threshold: <8 nmol/L)

Free Testosterone: 0.18 nmol/L ⚠️
  (Reference: 0.22-0.65 nmol/L)

SHBG: 45 nmol/L ✓

Symptom Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Sexual symptoms: Moderate
Physical symptoms: Moderate
Psychological symptoms: Mild

ADAM Questionnaire: Positive (7/10)
AMS Score: 27 points (moderate)

TRT Treatment Indication:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Clear symptoms
✅ Confirmed low testosterone
✅ Contraindications excluded

Meets TRT treatment indication ✓

TRT Treatment Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Status: Under treatment
Treatment Duration: 1 month
Effectiveness: Good
Tolerability: Good

Expected Benefits:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Improve libido and sexual function
✓ Improve mood and cognition
✓ Increase muscle mass and bone density
✓ Improve quality of life

Risks and Monitoring:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Prostate safety monitoring
  • PSA baseline and regular testing
  • Prostate volume monitoring

⚠️ Blood safety monitoring
  • Hct monitoring (alert: 54%)
  • Avoid polycythemia

⚠️ Cardiovascular risk monitoring
  • Monitor blood pressure
  • Watch for thrombosis symptoms

Excluded Other Diseases:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Normal thyroid function
✓ Depression excluded
✓ Chronic diseases assessed

Comprehensive Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue TRT treatment
✅ Regular monitoring of side effects
✅ Lifestyle intervention
✅ Comprehensive health management

Lifestyle Prescription:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Regular exercise
  • Strength training: 3 times per week
  • Aerobic exercise: 150 minutes per week
  • Bone density-improving exercises

✅ Nutritional support
  • Adequate protein
  • Calcium and vitamin D
  • Control caloric intake

✅ Sleep management
  • 7-8 hours/night
  • Regular sleep schedule

✅ Stress management
  • Mindfulness meditation
  • Social activities
  • Hobbies

✅ Quit smoking and limit alcohol
  • Complete smoking cessation
  • Limit alcohol

Prognosis Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
TRT treatment prognosis: Good ⭐⭐⭐⭐

Expected improvements:
• Symptom relief: 3-6 months
• Quality of life: Significant improvement
• Bone density: Improved over 2-3 years
• Maintenance treatment: Long-term

Follow-up Plan:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Review symptoms and efficacy after 3 months
✓ Review PSA and Hct after 6 months
✓ Comprehensive annual assessment

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This diagnosis is for reference only and cannot replace professional medical diagnosis.

TRT treatment must be performed under physician guidance!

Please follow up regularly to monitor efficacy and side effects.

Data saved
```

---

## Data Structure

### Main File: data/andropause-tracker.json

```json
{
  "created_at": null,
  "last_updated": null,

  "andropause": {
    "user_id": null,
    "age": null,
    "assessment_date": null,

    "symptoms": {
      "sexual": {},
      "physical": {},
      "psychological": {}
    },

    "testosterone_levels": {
      "total_testosterone": {},
      "free_testosterone": {},
      "shbg": {}
    },

    "questionnaire_scores": {
      "adam": {},
      "ams": {}
    },

    "trt": {
      "on_treatment": null,
      "medication": null,
      "type": null,
      "dose": null,
      "frequency": null,
      "route": null,
      "start_date": null,
      "duration_months": null,
      "effectiveness": null,
      "effectiveness_rating": null,
      "side_effects": [],
      "notes": ""
    },

    "monitoring": {
      "psa": {},
      "hematocrit": {},
      "prostate_volume": {}
    },

    "recommendations": []
  },

  "statistics": {
    "tracking_duration_months": 0,
    "total_symptom_records": 0,
    "trt_use": false
  }
}
```

### Detailed Records: data/andropause-records/YYYY-MM/YYYY-MM-DD_symptom-record.json

```json
{
  "record_id": "andropause_20251201_001",
  "record_date": "2025-12-01",
  "symptoms": {
    "sexual": {
      "libido": "moderate",
      "erectile_function": "mild"
    },
    "physical": {
      "fatigue": "moderate",
      "muscle_mass": "mild_decrease"
    },
    "psychological": {
      "mood": "mild"
    }
  },

  "metadata": {
    "created_at": "2025-12-01T10:00:00.000Z"
  }
}
```

---

## Intelligent Recognition Rules

### Symptom Recognition

| Symptom Type | Keywords |
|---------|--------|
| Decreased libido | libido_decreased, decreased_sex_drive, low_libido |
| Erectile dysfunction | erectile_difficulty, ED, erectile_dysfunction, impotence |
| Fatigue | fatigue, tiredness, no_energy |
| Depressed mood | depression, low_mood, depressed, unhappy |

### Testosterone Recognition

| Keyword | Extraction |
|--------|------|
| testosterone, total_testosterone | Value + nmol/L |
| morning, 09:00 | Measurement time |

---

## Error Handling

| Scenario | Error Message | Suggestion |
|------|---------|------|
| Testosterone = 0 | Testosterone value is 0<br>Suggests testing error | Retest |
| Hct>54% | Hematocrit too high<br>TRT suspension needed | Seek immediate medical attention |
| PSA rises rapidly | PSA significantly elevated<br>Prostate evaluation needed | Urology visit |

---

## Notes

- This system is for andropause health tracking only and cannot replace professional medical advice
- TRT treatment must be performed under physician guidance
- Regular monitoring of side effects is very important
- Both symptoms AND low testosterone are needed for diagnosis
- Other diseases must be excluded

**Situations Requiring Immediate Medical Attention:**
- Hct > 54%
- Rapid PSA elevation
- Breast lumps
- Lower limb swelling and pain
- Severe headache

All data is stored locally only to ensure privacy.

---

## Example Usage

```
# Record symptoms
/andropause symptom libido decreased
/andropause symptom fatigue moderate

# Record testosterone
/andropause testosterone 7.5 09:00

# ADAM questionnaire
/andropause adam

# TRT treatment
/andropause trt start gel 50mg
/andropause trt effectiveness good

# Monitoring
/andropause monitor psa 2.1

# View status
/andropause status
/andropause diagnosis
```
