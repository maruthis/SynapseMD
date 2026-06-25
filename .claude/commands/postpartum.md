---
description: Manage postpartum recovery and newborn care
arguments:
  - name: action
    description: "Action type: start/lochia/pain/breastfeeding/epds(psychological screening)/mood/weight/pelvic-floor/baby/status/recovery-summary/extend"
    required: true
  - name: info
    description: Postpartum information (delivery date, symptom description, examination results, etc., natural language description)
    required: false
---

# Postpartum Care Management

Comprehensive postpartum recovery tracking and newborn care management, from delivery through the postpartum recovery period, providing professional postpartum health monitoring and guidance.

**⏱️ Optional tracking periods**: 6 weeks (42 days) / 6 months (180 days) / 1 year (365 days)

**👶 Baby care**: Basic feeding, sleep, weight, diaper records

**🧠 Mental health**: EPDS depression screening + red flag alert system

## Action Types

### 1. Start Postpartum Record - `start`

Initialize postpartum recovery records.

**Parameter description:**
- `info`: Delivery information (required)
  - Delivery date: YYYY-MM-DD
  - Delivery method: vaginal / c-section
  - Number of babies: 1/2/3/4 (optional, default 1)
  - Tracking period: 6weeks/6months/1year (optional, default 6months)

**Examples:**
```
/postpartum start 2025-10-08 vaginal
/postpartum start 2025-10-08 c-section 6weeks
/postpartum start 2025-10-08 vaginal 2-babies 1year
```

**Execution steps:**

#### 1. Parse delivery information

**Extract information:**
- **Delivery date**: YYYY-MM-DD format
- **Delivery method**:
  - Vaginal: vaginal, natural
  - C-section: c-section, cesarean
- **Number of babies**: 1, 2, 3, 4 (default 1)
- **Tracking period**:
  - 6weeks: 42 days (standard)
  - 6months: 180 days (recommended)
  - 1year: 365 days (complete)

#### 2. Validate input

**Check items:**
- Delivery date cannot be a future date
- Delivery date should be within the past 2 weeks (avoid outdated data)
- Number of babies should be within reasonable range (1-4)

#### 3. Calculate postpartum days and stage

**Postpartum stage classification:**
```javascript
days_postpartum = today - delivery_date

if (days_postpartum <= 2) {
  stage = "immediate" // Acute phase (0-2 days)
} else if (days_postpartum <= 14) {
  stage = "early" // Early phase (3-14 days)
} else if (days_postpartum <= 42) {
  stage = "subacute" // Subacute phase (15-42 days)
} else {
  stage = "late" // Recovery phase (43+ days)
}
```

#### 4. Create postpartum record

**Data structure:**
```json
{
  "postpartum_id": "postpartum_20251008",
  "delivery_date": "2025-10-08",
  "delivery_type": "vaginal",
  "baby_count": 1,
  "tracking_period": "6months",
  "tracking_end_date": "2026-04-06",

  "current_status": {
    "days_postpartum": 0,
    "stage": "immediate",
    "progress_percentage": 0
  },

  "recovery_tracking": {
    "lochia": {
      "stage": "rubra",
      "amount": "moderate",
      "last_updated": null
    },
    "perineal_care": {
      "healing": "good",
      "pain_level": 3,
      "incision_type": null,
      "notes": ""
    },
    "breastfeeding": {
      "status": "establishing",
      "challenges": [],
      "last_updated": null
    },
    "pain": {
      "uterine_contractions": {
        "present": true,
        "severity": "moderate"
      },
      "incision_pain": null,
      "back_pain": null,
      "headache": null
    }
  },

  "mental_health": {
    "epds": {
      "last_screened": null,
      "total_score": null,
      "risk_level": "not_screened",
      "q10_positive": false,
      "last_updated": null
    },
    "mood_log": []
  },

  "physical_recovery": {
    "pelvic_floor": {
      "status": "recovering",
      "exercises": "not_started",
      "notes": ""
    },
    "diastasis_recti": {
      "present": null,
      "severity": null,
      "assessed": false
    },
    "weight_tracking": [],
    "sleep_tracking": []
  },

  "babies": [
    {
      "baby_id": "A",
      "name": null,
      "gender": null,
      "birth_weight": null,
      "current_weight": null,
      "feeding": {
        "method": "establishing",
        "pattern": "on_demand",
        "last_feed": null,
        "feeds_log": []
      },
      "sleep": {
        "pattern": "newborn",
        "last_sleep": null,
        "sleep_log": []
      },
      "diapers": {
        "count": 0,
        "last_change": null,
        "diaper_log": []
      },
      "notes": ""
    }
  ],

  "red_flags": {
    "active": [],
    "resolved": [],
    "last_assessment": null
  },

  "metadata": {
    "created_at": "2025-10-08T00:00:00.000Z",
    "last_updated": "2025-10-08T00:00:00.000Z"
  }
}
```

#### 5. Output confirmation

```
✅ Postpartum record created

Delivery information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Delivery date: October 8, 2025
Delivery method: Vaginal
Number of babies: 1
Current postpartum: Day 0

Tracking settings:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Tracking period: 6 months
Tracking end: April 6, 2026

Postpartum stage: Acute phase (0-2 days)

📋 Postpartum care guide:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Acute phase (0-2 days) focus:
• Rest and recovery
• Lochia observation (color, amount)
• Pain management
• Begin breastfeeding (if applicable)
• Monitor temperature, blood pressure

Red flags (seek medical care immediately if present):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Postpartum hemorrhage (>1 pad/hour)
• Fever > 100.4°F (38°C)
• Severe headache
• Blurred vision
• Difficulty breathing
• Chest pain

⚠️ Important disclaimer:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is only for postpartum health tracking and cannot replace the postpartum examination (6-week checkup).
Seek medical care promptly if any abnormalities occur.

EPDS psychological screening will be reminded at 6 weeks postpartum.

Data saved to: data/postpartum-records/2025-10/2025-10-08_postpartum-record.json
```

---

### 2. Record Lochia - `lochia`

Record postpartum lochia.

**Parameter description:**
- `info`: Lochia information (required)
  - Stage: rubra (red), serosa (serous), alba (white)
  - Amount: light, moderate, heavy

**Examples:**
```
/postpartum lochia rubra moderate
/postpartum lochia serosa light
/postpartum lochia heavy large_clots  # Heavy + blood clots
```

**Lochia stages:**

| Stage | Time | Color | Duration |
|-------|------|-------|---------|
| Lochia Rubra | 0-3 days | Bright red | 2-4 days |
| Lochia Serosa | 4-9 days | Pink/brown | 5-7 days |
| Lochia Alba | 10+ days | Yellow/white | 2-6 weeks |

**Abnormal alert:**
```
⚠️ Lochia abnormality alert

Current situation: Excessive lochia + large blood clots

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Still having large amounts of bright red lochia on day 10
Possible causes:
• Poor uterine contraction
• Retained placenta/membranes
• Infection

🏥 Seek immediate medical evaluation:
• Uterine ultrasound
• Monitor hemoglobin
• Consider uterine evacuation
```

---

### 3. Record Pain - `pain`

Record postpartum pain.

**Parameter description:**
- `info`: Pain information (required)
  - Location: uterine (uterine contractions), incision (wound), breast, head (headache), back
  - Severity: 1-10 scale or mild/moderate/severe

**Examples:**
```
/postpartum pain uterine 6
/postpartum pain incision moderate
/postpartum pain breast engorgement
/postpartum pain severe 9  # Severe pain, 9/10
```

**Pain assessment:**
- **Uterine contraction pain**: Similar to menstrual cramps, worsens during breastfeeding (normal)
- **Perineal/c-section incision pain**: Gradually decreases
- **Breast engorgement pain**: May accompany mastitis
- **Severe headache**: Watch for epidural complications or eclampsia

**Alert:**
```
⚠️ Severe headache alert

Symptoms: Day 5 postpartum, severe headache (9/10)

🚨 Requires immediate evaluation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Blood pressure monitoring (pre-eclampsia)
• Neurological examination
• Consider epidural hematoma
• Consider infection

Please seek immediate medical attention!
```

---

### 4. Breastfeeding Record - `breastfeeding`

Record breastfeeding.

**Parameter description:**
- `info`: Breastfeeding information (required)
  - Method: exclusive (exclusive breastfeeding), mixed (mixed feeding), formula
  - Issues: engorgement, mastitis, low-supply, cracked-nipples

**Examples:**
```
/postpartum breastfeeding exclusive
/postpartum breastfeeding mixed engorgement
/postpartum breastfeeding formula 60ml
/postpartum breastfeeding low-supply
```

**Breastfeeding assessment:**
```json
{
  "breastfeeding": {
    "status": "exclusive",
    "frequency": "on_demand",
    "latch": "good",
    "milk_supply": "adequate",
    "challenges": ["engorgement"],
    "pain_level": 2,
    "last_updated": "2025-10-10T10:00:00.000Z"
  }
}
```

**Mastitis alert:**
```
⚠️ Possible mastitis

Symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Breast redness, swelling, warmth, pain
• Fever > 100.4°F
• Flu-like symptoms
• Hard lump in breast

🏥 Management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Continue breastfeeding or pumping
• Warm compress + massage
• Rest + hydration
• Consider antibiotics (requires physician prescription)

⚠️ No improvement within 24 hours or fever > 102°F:
Seek immediate medical attention! May require abscess drainage.
```

---

### 5. EPDS Psychological Screening - `epds`

Edinburgh Postnatal Depression Scale (EPDS) screening.

**Parameter description:**
- `info`: EPDS score (required)
  - 10 questions, each scored 0-3 points
  - Total score: 0-30 points
  - Question 10: Self-harm thoughts (score of 2-3 requires special alert)

**EPDS 10 questions:**
1. I have been able to laugh and see the funny side of things
2. I have looked forward with enjoyment to things
3. I have blamed myself unnecessarily when things went wrong
4. I have been anxious or worried for no good reason
5. I have felt scared or panicky for no good reason
6. Things have been getting on top of me
7. I have been so unhappy that I have had difficulty sleeping
8. I have felt sad or miserable
9. I have been so unhappy that I have been crying
10. The thought of harming myself has occurred to me

**Scoring standards:**
- 0-9: Low risk
- 10-12: Moderate risk (monitoring recommended)
- 13-24: High risk (immediate medical attention required)
- Question 10 ≥ 1: Suicidal ideation (emergency)

**Examples:**
```
/postpartum epds 8           # Total score 8 (low risk)
/postpartum epds 14          # Total score 14 (high risk)
/postpartum epds 10 q10=2    # Total score 10, Q10 score 2
```

**Execution steps:**

#### 1. Parse EPDS score

**Extract information:**
- **Total score**: 0-30
- **Q10 score**: Recorded separately (0-3)
- **Screening time**: Record current time

#### 2. Risk assessment

**Risk classification:**
```javascript
function assessEPDS(score, q10Score) {
  if (q10Score >= 2) {
    return {
      risk_level: "emergency",
      recommendation: "immediate_intervention",
      message: "🚨 Emergency: self-harm thoughts present"
    };
  }

  if (score >= 13) {
    return {
      risk_level: "high",
      recommendation: "immediate_referral",
      message: "⚠️ High risk: immediate medical evaluation required"
    };
  }

  if (score >= 10) {
    return {
      risk_level: "moderate",
      recommendation: "monitoring",
      message: "⚠️ Moderate risk: close monitoring and follow-up recommended"
    };
  }

  return {
    risk_level: "low",
    recommendation: "routine",
    message: "✓ Low risk: continue routine monitoring"
  };
}
```

#### 3. Output results

**Low risk (0-9):**
```
✅ EPDS psychological screening completed

EPDS results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Screening date: November 15, 2025
Postpartum days: 35 days
EPDS total score: 8

Risk assessment: Low risk ✓

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Continue maintaining a positive mindset
• Adequate rest and sleep
• Communicate with family and friends
• Moderate exercise (e.g., walking)

Next screening:
━━━━━━━━━━━━━━━━━━━━━━━━━━
3 months postpartum (approximately January 2026)

Re-screen anytime if:
• Persistent low mood
• Unable to care for baby
• Feelings of hopelessness or thoughts of harming yourself
```

**Moderate risk (10-12):**
```
⚠️ EPDS screening - Moderate risk

EPDS results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Screening date: November 15, 2025
EPDS total score: 11

Risk assessment: Moderate risk

Possible manifestations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Mood swings
• Anxiety and worry
• Sleep difficulties
• Fatigue

Recommended measures:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Re-screen EPDS in 2 weeks
2. Increase family support
3. Ensure rest time
4. Consider psychological counseling
5. Join a postpartum mothers' support group

🏥 Professional help:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Consult obstetrician
• Consider referral to psychiatry
• Postpartum depression hotline

⚠️ Warning signs (seek immediate medical attention if present):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Emotional numbness or emptiness
• Unable to care for yourself and baby
• Thoughts of harming yourself or baby
```

**High risk (≥13):**
```
🚨 EPDS screening - High risk

EPDS results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Screening date: November 15, 2025
EPDS total score: 15

Risk assessment: High risk ⚠️

🏥 Immediate medical attention recommended:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Please consult within 48 hours:
1. Obstetrician or gynecologist
2. Psychologist or psychiatrist
3. Postpartum depression specialty clinic

Postpartum depression is treatable, do not delay!

Possible diagnosis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Postpartum depression
• Requires professional evaluation and treatment

Treatment options:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Psychological therapy (CBT)
• Medication (compatible with breastfeeding)
• Support groups
• Family support

📞 Emergency help:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Postpartum depression hotline
• Mental health crisis intervention hotline
• Go to emergency room

⚠️ If you have suicidal thoughts:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Tell a family member or friend immediately!
Call emergency services or go to the ER immediately!
```

**Emergency (Q10 ≥ 2):**
```
🚨🚨🚨 Emergency alert

Question 10 score: 2-3
(Self-harm thoughts present)

🚨 Must act immediately:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Tell someone nearby immediately
• Partner/family member
• Friend/neighbor
• Do not face this alone!

Step 2: Seek professional help immediately
• Call emergency services
• Go to the nearest hospital emergency room
• Contact your obstetrician

Step 3: Ensure baby's safety
• Ask family to temporarily care for baby
• Do not leave baby alone

📞 24-hour help hotlines:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• National psychological support hotline
• Crisis lifeline
• Local mental health center

You are not alone! Help is nearby!
Please seek help immediately!
```

---

### 6. Record Mood - `mood`

Record postpartum emotional state.

**Parameter description:**
- `info`: Mood description (required)
  - Mood: happy, anxious, sad, irritable, overwhelmed
  - Severity: mild/moderate/severe

**Examples:**
```
/postpartum mood anxious
/postpartum mood happy
/postpartum mood overwhelmed severe
/postpartum mood sad crying_spells
```

**Mood classification:**
- **Baby Blues**: Begins 3-5 days postpartum, lasts days to 2 weeks
  - Mood swings
  - Tearfulness
  - Fatigue
  - Anxiety

- **Postpartum Depression**:
  - Persistent sadness
  - Loss of interest
  - Sleep problems (not caused by baby)
  - Feelings of worthlessness or guilt
  - Difficulty concentrating

- **Postpartum Psychosis** (rare but urgent):
  - Hallucinations or delusions
  - Confused thinking
  - Extreme behavior
  - Thoughts of harming self or baby

**Alert:**
```
🚨 Suspected postpartum psychosis

Symptoms: Hallucinations, confused thinking

🚨 This is a medical emergency!
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Call emergency services immediately
• Go to hospital emergency room
• Do not leave patient alone
• Ensure baby's safety

Requires immediate psychiatric evaluation!
```

---

### 7. Record Weight - `weight`

Record postpartum weight recovery.

**Parameter description:**
- `info`: Weight value (required)
  - Weight: number + kg or lbs

**Examples:**
```
/postpartum weight 65.0
/postpartum weight 145 lbs
```

**Weight recovery assessment:**
```javascript
weight_loss = delivery_weight - current_weight
expected_loss = delivery_weight - pre_pregnancy_weight

// 6 weeks postpartum: should have lost 50% of pregnancy weight gain
// 6 months postpartum: should be close to pre-pregnancy weight
```

---

### 8. Pelvic Floor Record - `pelvic-floor`

Record pelvic floor recovery and exercises.

**Parameter description:**
- `info`: Pelvic floor information (required)
  - Exercises: kegel, squats
  - Symptoms: incontinence, prolapse (prolapse feeling)

**Examples:**
```
/postpartum pelvic-floor kegel-exercises 20
/postpartum pelvic-floor incontinence mild
/postpartum pelvic-floor recovering
```

**Pelvic floor recovery timeline:**
- **Postpartum 0-6 weeks**: Begin Kegel exercises gently (10 times/day)
- **Postpartum 6-12 weeks**: Gradually increase intensity (20-30 times/day)
- **Postpartum 3-6 months**: Continue strengthening

**Incontinence alert:**
```
⚠️ Urinary incontinence alert

Symptom: Stress urinary incontinence (leaking when coughing or sneezing)

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Persist with Kegel exercises
• Bladder training
• Avoid heavy lifting
• Pelvic floor assessment at 6 weeks postpartum

If persistent:
Consider pelvic floor physical therapy
```

---

### 9. Baby Record - `baby`

Record baby's feeding, sleep, weight, and diapers.

**Parameter description:**
- `info`: Baby information (required)
  - Baby identifier: A/B/C/D (for multiples)
  - Type: feeding, sleep, weight, diaper
  - Detailed information

**Examples:**
```
# Feeding
/postpartum baby A feeding breastfeeding left 15min
/postpartum baby A feeding formula 60ml
/postpartum baby A feeding mixed 50ml

# Sleep
/postpartum baby A sleep 2hrs
/postpartum baby B sleep 1.5hrs

# Weight
/postpartum baby A weight 3.2kg
/postpartum baby A weight 3200g

# Diaper
/postpartum baby A diaper wet
/postpartum baby A diaper soiled
```

**Baby data structure:**
```json
{
  "babies": [
    {
      "baby_id": "A",
      "name": null,
      "gender": null,
      "birth_date": "2025-10-08",
      "birth_weight": null,
      "current_weight": {
        "value": 3.2,
        "unit": "kg",
        "date": "2025-10-15",
        "weight_gain": null
      },
      "feeding": {
        "method": "breastfeeding",
        "last_feed": {
          "time": "2025-10-15T14:30:00.000Z",
          "type": "breast",
          "side": "left",
          "duration_minutes": 15,
          "amount_ml": null
        },
        "feeds_today": 8,
        "pattern": "on_demand"
      },
      "sleep": {
        "last_sleep": {
          "start": "2025-10-15T12:00:00.000Z",
          "end": "2025-10-15T14:00:00.000Z",
          "duration_hours": 2
        },
        "pattern": "newborn",
        "total_sleep_today": 16
      },
      "diapers": {
        "wet_today": 6,
        "soiled_today": 3,
        "last_change": "2025-10-15T14:30:00.000Z",
        "pattern": "normal"
      },
      "notes": ""
    }
  ]
}
```

**Feeding assessment:**
- **Newborn feeding frequency**: 8-12 times/24 hours
- **Wet diapers**: ≥6/24 hours (indicates adequate intake)
- **Weight gain**:
  - Week 1: May lose 5-10% (physiological weight loss)
  - Week 2: Return to birth weight
  - 0-3 months: Weight gain 150-200g/week

**Abnormality alert:**
```
⚠️ Insufficient baby intake alert

Observations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Today's wet diapers: 3 (normal ≥6)
• Weight loss: 12% (normal <10%)
• Feeding count: 5 (normal 8-12)

🏥 Recommended immediate medical evaluation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Assess breastfeeding position
• Check baby's latch
• Monitor weight
• May need formula supplementation

⚠️ Dehydration symptoms (seek immediate medical attention):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Sunken fontanelle
• Dry mouth
• No urine for >6 hours
• Lethargy
```

---

### 10. View Status - `status`

Display current postpartum recovery status.

**Example:**
```
/postpartum status
```

**Output:**
```
📍 Postpartum recovery status

Basic information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Delivery date: October 8, 2025
Current date: November 15, 2025
Postpartum days: 38 days
Postpartum stage: Subacute phase (15-42 days)
Tracking progress: 21% (38/180 days)

Delivery method: Vaginal
Number of babies: 1

Recovery tracking:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Lochia: Lochia Alba (white), light amount
Wound healing: Good, pain 1/10
Breastfeeding: Exclusive breastfeeding, adequate supply
Pain: Mild uterine contraction pain

Mental health:
━━━━━━━━━━━━━━━━━━━━━━━━━━
EPDS screening: 8 points (low risk) ✓
Last screening: Postpartum day 35
Mood: Stable

Physical recovery:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current weight: 65.0 kg
Pre-pregnancy weight: 60.0 kg
Delivery weight: 70.0 kg
Weight recovered: 5.0 kg (50%)

Pelvic floor: Recovering, Kegel exercises 20 times/day
Sleep: Average 5.5 hours/24 hours

Baby A information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current weight: 3.8 kg (+600g)
Birth weight: 3.2 kg
Age: 38 days

Feeding: Exclusive breastfeeding, 8-10 times/day
Sleep: 3-4 hour cycles, 16 hours/24 hours
Diapers: 6-8 wet diapers/24 hours ✓

Next checkups:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• 6-week postpartum checkup: November 19, 2025 (4 days away)
• EPDS re-screening: 3 months postpartum (approximately January 2026)

This week's focus:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Prepare for 6-week postpartum checkup
• Continue pelvic floor exercises
• Monitor lochia changes
• Maintain breastfeeding

Red flag review:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ No active alerts

⚠️ Seek immediate medical attention for:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Sudden increase in lochia or bright red color
• Fever > 100.4°F (38°C)
• Severe abdominal pain
• Breast redness, swelling, warmth, pain (mastitis)
• Persistent low mood or despair
• Thoughts of harming yourself or baby
```

---

### 11. Recovery Summary - `recovery-summary`

Generate a complete postpartum recovery summary report.

**Example:**
```
/postpartum recovery-summary
```

**Output includes:**
- Lochia change curve
- Weight recovery curve
- Breastfeeding journey
- Mental health assessment
- Baby growth curve
- Next checkup reminders

---

### 12. Extend Tracking Period - `extend`

Extend the postpartum tracking period.

**Parameter description:**
- `info`: New tracking period (required)
  - 6weeks/6months/1year

**Example:**
```
/postpartum extend 1year
```

---

## Red Flag Alert System

The system automatically monitors the following red flag situations:

### Maternal Red Flags

| Symptom | Threshold | Response |
|---------|-----------|----------|
| Postpartum hemorrhage | >1 pad/hour | ⚠️ Immediate medical attention |
| Fever | >100.4°F (38°C) | ⚠️ Medical evaluation |
| Severe headache | Persistent, unrelieved | 🚨 Emergency evaluation |
| Vision changes | Blurring, flashes | 🚨 Emergency evaluation |
| Difficulty breathing | Present at rest | 🚨 Emergency |
| Chest pain | Any severity | 🚨 Emergency |
| Leg pain and swelling | Unilateral | ⚠️ Watch for DVT |
| Wound infection | Redness, swelling, warmth, pain, pus | ⚠️ Medical attention |
| Mastitis | Fever + breast redness/swelling | ⚠️ Medical attention within 24h |
| Mood issues | EPDS≥13 or Q10≥1 | 🚨 Emergency/immediate |
| Suicidal thoughts | Q10≥2 | 🚨🚨🚨 Immediate |

### Baby Red Flags

| Symptom | Threshold | Response |
|---------|-----------|----------|
| Insufficient intake | <6 wet diapers/24h | ⚠️ Medical evaluation |
| Weight loss | >10% birth weight | ⚠️ Immediate medical attention |
| Fever | >100.4°F (38°C) | 🚨 Emergency |
| Feeding difficulty | Unable to suck/swallow | 🚨 Emergency |
| Breathing difficulty | Rapid/grunting/retracting | 🚨🚨 Emergency |
| Jaundice | Severe/persistent | ⚠️ Medical attention |
| Dehydration | Sunken fontanelle/no urine 6h+ | 🚨 Emergency |

---

## Data File Structure

### Main file: data/postpartum-tracker.json

```json
{
  "created_at": null,
  "last_updated": null,

  "current_postpartum": null,
  "postpartum_history": [],

  "statistics": {
    "total_postpartum_periods": 0,
    "current_days_postpartum": null,
    "total_babies_tracked": 0
  },

  "settings": {
    "tracking_period_default": "6months",
    "epds_reminder_enabled": true,
    "red_flag_monitoring": true
  }
}
```

### Detailed records: data/postpartum-records/YYYY-MM/YYYY-MM-DD_postpartum-record.json

---

## Safety Disclaimer

⚠️ **Important disclaimer**:

This system is only for postpartum health tracking and cannot replace professional medical care:

- **The 6-week postpartum checkup must be completed on time**
- **Red flag situations require immediate medical attention**
- **EPDS≥13 or Q10≥1 requires immediate mental health assistance**
- **Baby abnormalities require immediate consultation with a pediatrician**

Emergency contact numbers:
- 🚨 Emergency: Call 911 (or local emergency number)
- 🏥 Obstetrics/Gynecology: [Enter hospital phone number]
- 👶 Pediatrics: [Enter hospital phone number]
- 📞 Postpartum depression hotline: [Enter local hotline]

---

## Usage Examples

```
# Start postpartum record
/postpartum start 2025-10-08 vaginal

# Record lochia
/postpartum lochia rubra moderate

# Record pain
/postpartum pain uterine 5

# Breastfeeding record
/postpartum breastfeeding exclusive

# EPDS screening
/postpartum epds 8

# Baby feeding
/postpartum baby A feeding breastfeeding left 15min

# View status
/postpartum status

# Recovery summary
/postpartum recovery-summary
```
