# Women's Health Feature Extension Proposal

**Module Number**: 01
**Category**: Population-Based Classification - Women's Health
**Status**: ✅ Implemented
**Priority**: High
**Created**: 2025-12-31
**Completed**: 2026-01-01

---

## Feature Overview

The Women's Health module contains three sub-modules that comprehensively cover women's health needs across different life stages:

1. 🤰 **Pregnancy Management System** - Full-cycle management from pre-conception to delivery
2. 🌸 **Menopause Management System** - Perimenopause symptom management and health guidance
3. 🎗️ **Gynecological Cancer Screening Tracker** - Screening management for cervical, ovarian, and endometrial cancer

---

## Sub-module 1: Pregnancy Management System

### Feature Description

Full-cycle pregnancy tracking and management, from pre-conception to postpartum recovery, providing comprehensive pregnancy health monitoring and management functions.

### Core Features

#### 1. Due Date Calculator
- Calculated based on Last Menstrual Period (LMP)
- Corrected using ultrasound-confirmed dates
- Automatic gestational week updates and trimester classification
- Due date confidence intervals

#### 2. Pregnancy Milestone Tracking
- **First Trimester (Weeks 1-12)**: Critical organ development period, NT scan
- **Second Trimester (Weeks 13-27)**: Down syndrome screening, anatomy scan, glucose tolerance test
- **Third Trimester (Weeks 28-40)**: Fetal movements, fetal position, birth preparation

#### 3. Prenatal Visit Reminders
- Standard prenatal visit schedule
  - Weeks 12, 16, 20, 24, 28
  - Weeks 32, 34, 36
  - Weeks 37-40: weekly
- Special exam schedule (NT, Down syndrome screening, glucose tolerance, anatomy scan)
- Exam preparation and precautions

#### 4. Pregnancy Symptom Recording
- **Morning Sickness (First Trimester)**: Nausea/vomiting frequency and severity
- **Edema (Third Trimester)**: Degree of swelling in hands and feet
- **Fetal Movement Record (After Week 28)**: Number and timing of movements
- **Contraction Record (Third Trimester)**: Braxton Hicks vs. true contractions
- **Weight Gain Curve**: Weekly weight monitoring
- **Blood Pressure Monitoring**: Gestational hypertension screening

#### 5. Pregnancy Medication Safety Check
- Drug pregnancy category (A/B/C/D/X)
- Contraindicated drug alerts
- Safe alternative recommendations
- Herbal medicine safety assessment

#### 6. Nutritional Guidance
- **Folic Acid Supplementation**: 3 months pre-conception to early pregnancy (400-800μg/day)
- **Iron Supplementation**: Second and third trimesters
- **Calcium Supplementation**: Throughout pregnancy (1000-1200mg/day)
- **DHA Supplementation**: During pregnancy (200-300mg/day)
- Foods to avoid during pregnancy (raw food, alcohol, high-mercury fish, etc.)

### Data Structure

```json
{
  "pregnancy_id": "pregnancy_20250101",
  "lmp_date": "2025-01-01",
  "due_date": "2025-10-08",
  "due_date_confidence": "high",
  "current_week": 12,
  "current_trimester": "first",
  "corrected_by_ultrasound": false,

  "prenatal_checks": [
    {
      "check_id": "check_001",
      "week": 12,
      "check_type": "NT",
      "scheduled_date": "2025-03-25",
      "completed": false,
      "results": {},
      "notes": ""
    }
  ],

  "symptoms": {
    "nausea": {
      "severity": "moderate",
      "frequency": "daily",
      "triggers": ["morning", "empty_stomach"],
      "relief_methods": ["crackers", "small_frequent_meals"]
    },
    "fatigue": {
      "severity": "mild",
      "frequency": "often"
    },
    "edema": {
      "present": false,
      "severity": null
    }
  },

  "weight_tracking": [
    {
      "date": "2025-01-01",
      "week": 0,
      "weight": 60.0,
      "weight_gain": 0.0,
      "bmi": 22.5,
      "recommended_gain": "11.5-16kg"
    }
  ],

  "blood_pressure": [
    {
      "date": "2025-03-15",
      "week": 10,
      "systolic": 115,
      "diastolic": 75,
      "interpretation": "normal"
    }
  ],

  "fetal_movement": {
    "tracking_started": false,
    "start_week": 28,
    "movements": []
  },

  "contractions": [],

  "medication_safety": {
    "checked_medications": [],
    "contraindications": [],
    "safe_alternatives": {}
  },

  "nutrition_plan": {
    "folic_acid": {
      "dose": "400μg",
      "frequency": "daily",
      "started": "2024-10-01"
    },
    "iron": {
      "dose": null,
      "frequency": null,
      "started": null
    }
  },

  "metadata": {
    "created_at": "2025-01-01T00:00:00.000Z",
    "last_updated": "2025-03-25T10:00:00.000Z"
  }
}
```

### Command Interface

```bash
# Start pregnancy record
/pregnancy start 2025-01-01              # Last menstrual period date

# Record prenatal visit
/pregnancy checkup week 12 NT normal     # Record NT scan
/pregnancy checkup week 16 down-screening low-risk   # Record Down syndrome screening

# Record symptoms
/pregnancy symptom nausea moderate        # Record morning sickness
/pregnancy symptom edema feet            # Record edema

# Record weight
/pregnancy weight 62.5                   # Record current weight

# Record fetal movement (after week 28)
/pregnancy movement 10 kicks              # Record fetal movements

# Record blood pressure
/pregnancy bp 115/75                     # Record blood pressure

# Medication safety check
/pregnancy medication-check aspirin      # Check medication safety

# View status
/pregnancy status                        # View current status
/pregnancy next-checkup                  # Next prenatal visit reminder
```

### Usage Example

```
User: /pregnancy start 2025-01-01

System:
✅ Pregnancy record created

Pregnancy Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Last Menstrual Period: January 1, 2025
Due Date: October 8, 2025
Current Gestational Week: Week 12
Trimester: First Trimester

Next Prenatal Visit:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 12 NT Scan - March 25, 2025 (10 days remaining)

💡 Tips:
- Continue folic acid supplementation 400μg/day
- Seek immediate medical attention if vaginal bleeding or abdominal pain occurs
⚠️ Important Disclaimer:
This system is for pregnancy health tracking only and cannot replace professional prenatal care.
Please attend all scheduled prenatal visits and seek medical attention promptly if any abnormalities arise.
```

---

## Sub-module 1.1: Multiple Pregnancy Extension ✅

### Feature Description

Specialized tracking and management for twin, triplet, and quadruplet pregnancies, including automatic detection, additional monitoring, and safety alerts.

### Core Features

#### 1. Multiple Pregnancy Type Support
- **Singleton pregnancy** - Standard tracking
- **Twin pregnancy** - Delivery at 37 weeks, additional monitoring
- **Triplet pregnancy** - Delivery at 35 weeks, high-risk management
- **Quadruplet pregnancy** - Delivery at 32 weeks, extremely high-risk management

#### 2. Intelligent Detection
- Automatic recognition of multiple pregnancies from ultrasound notes
- Supports Chinese and English keywords:
  - Chinese keywords: twins, triplets, quadruplets, twin babies, triplet babies
  - English keywords: twins, triplets, quadruplets, two/three/four fetuses
- Automatically sets pregnancy type after user confirmation

#### 3. Adjusted Due Dates
- Singleton: 40 weeks (280 days)
- Twins: 37 weeks (259 days) - average 3 weeks early
- Triplets: 35 weeks (245 days) - average 5 weeks early
- Quadruplets: 32 weeks (224 days) - average 8 weeks early

#### 4. Adjusted Weight Gain Recommendations
- Singleton BMI 18.5-24.9: 11.5-16 kg
- Twins BMI 18.5-24.9: 16-20 kg (additional 4-5 kg)
- Triplets BMI 18.5-24.9: 20-25 kg (additional 8-9 kg)
- Quadruplets BMI 18.5-24.9: 22-27 kg (additional 10-11 kg)

#### 5. Fetal Profile Management
- Create individual profiles for each fetus (A, B, C, D)
- Track each fetus's:
  - Estimated weight
  - Fetal position (cephalic, breech, transverse)
  - Heart rate
  - Amniotic fluid index
- Calculate fetal weight discordance

#### 6. High-Risk Monitoring
- **TTTS Alert** (Twin-to-Twin Transfusion Syndrome):
  - Stage I: MVP donor < 2cm, recipient > 8cm
  - Stage II: Donor bladder not visible
  - Stage III: Abnormal Doppler blood flow
  - Stage IV: Hydrops
  - Stage V: Death of one or both fetuses
- **Cervical Length Monitoring**: < 25mm requires attention
- **Fetal Growth Discordance**: > 20% requires attention

### Command Interface

```bash
# Manually set pregnancy type
/pregnancy type twins                   # Set to twin pregnancy
/pregnancy type triplets                # Set to triplet pregnancy

# Add fetal profile
/pregnancy fetal A weight 1500 position cephalic  # Fetus A
/pregnancy fetal B weight 1400 position breech   # Fetus B

# View multiple pregnancy status
/pregnancy status                       # Display all fetal information
```

### Implementation Status

✅ **Completed** (2026-01-01)
- Data structure supports 1-4 fetuses
- Intelligent detection implemented
- Adjusted due dates and weight gain
- TTTS monitoring alerts
- All 21 native test cases passed
- Native test framework (Shell + Python)

---

## Sub-module 1.2: Postpartum Care Tracking ✅

### Feature Description

Comprehensive postpartum recovery tracking, including maternal physical recovery, mental health screening (EPDS), and newborn care.

### Core Features

#### 1. Postpartum Period Settings
- **6 weeks** (42 days) - Standard immediate recovery period
- **6 months** (180 days) - Extended recovery period ✓ **Recommended**
- **1 year** (365 days) - Complete recovery tracking

#### 2. Maternal Recovery Tracking
- **Lochia Stages**:
  - Lochia rubra (blood-red) - Days 0-3
  - Lochia serosa (pink/brown) - Days 4-9
  - Lochia alba (white/yellow) - Day 10+
- **Pain Management**: Uterine cramping, perineal/incision pain
- **Breastfeeding**: Type, challenges, records
- **Pelvic Floor Recovery**: Kegel exercise tracking
- **Weight Tracking**: Postpartum weight loss curve

#### 3. Mental Health Screening (EPDS)
- **Edinburgh Postnatal Depression Scale** (EPDS):
  - 10 questions, 0-3 points each
  - Total score range: 0-30
- **Risk Classification**:
  - **0-9 points**: Low risk - routine monitoring
  - **10-12 points**: Moderate risk - increased monitoring
  - **13+ points**: High risk - ⚠️ **Immediate referral**
  - **Question 10 ≥ 2 points**: Emergency - 🚨 **Immediate intervention**

#### 4. Red Flag Alert System

**Maternal Red Flags**:
- Postpartum hemorrhage (> 1 pad/hour) - ⚠️ Contact doctor
- Fever (> 100.4°F/38°C) - ⚠️ Possible infection
- Severe headache - ⚠️ Contact doctor
- Vision changes - ⚠️ Contact doctor
- Difficulty breathing (at rest) - 🚨 Emergency
- Suicidal thoughts - 🚨 **Immediate emergency intervention**

**Infant Red Flags**:
- Insufficient feeding (< 6 wet diapers/24 hours) - ⚠️ Contact doctor
- Excessive weight loss (> 10% of birth weight) - ⚠️ Contact doctor
- Fever (> 100.4°F/38°C) - 🚨 Emergency
- Feeding difficulties (unable to suck/swallow) - 🚨 Emergency
- Respiratory distress - 🚨 **Immediate emergency intervention**

#### 5. Newborn Care Tracking
- **Feeding Records**:
  - Breastfeeding (duration, left/right side)
  - Formula feeding (milliliters)
  - Mixed feeding
- **Sleep Patterns**: Sleep duration and frequency
- **Weight Tracking**: Current weight (kg)
- **Diaper Records**: Wet/dirty diaper count

#### 6. Automatic Postpartum Phase Calculation
- **Immediate** (Days 0-2) - Hospital recovery, initial breastfeeding
- **Early** (Days 3-14) - Establishing feeding, rest, recovery
- **Subacute** (Days 15-42) - Healing, establishing routines
- **Late** (Day 43+) - Long-term recovery, mental health

### Command Interface

```bash
# Start postpartum tracking
/postpartum start 2025-10-08 vaginal 1-baby 6months

# Maternal recovery records
/postpartum lochia rubra moderate           # Lochia record
/postpartum pain 3 uterus                  # Pain record (0-10 scale)
/postpartum breastfeeding exclusive         # Breastfeeding status
/postpartum weight 68.5                     # Weight record

# Mental health screening
/postpartum epds 7                          # EPDS total score (0-30)
/postpartum epds 15 2                       # Score 15, Q10 = 2 (emergency)
/postpartum mood calm                       # Mood record

# Newborn care (use A, B, C, D for multiples)
/postpartum baby A feeding breastfeeding 15min
/postpartum baby A sleep 3hrs
/postpartum baby A weight 3.2
/postpartum baby A diaper wet

# View status
/postpartum status                          # Current status
/postpartum recovery-summary                # Full recovery summary
/postpartum extend 1year                    # Extend tracking period
```

### Implementation Status

✅ **Completed** (2026-01-01)
- Complete postpartum tracking data structure
- EPDS scoring and risk assessment
- Red flag alert system
- Multiple newborn support (A, B, C, D)
- All 21 native test cases passed
- Native test framework (Shell + Python)
- Complete user documentation: [docs/postpartum-care-guide.md](../docs/postpartum-care-guide.md)
- Testing documentation: [docs/testing.md](../docs/testing.md)

---

## Sub-module 2: Menopause Management System

### Feature Description

Perimenopause symptom tracking and management, providing menopause health assessment and management recommendations.

### Core Features

#### 1. Menopause Symptom Scoring
- **Hot Flashes/Night Sweats**: Frequency (times per day), severity, impact on daily life
- **Mood Changes**: Anxiety, depression, irritability
- **Sleep Disturbances**: Insomnia, early waking, sleep quality
- **Vaginal Dryness**: Degree, impact
- **Joint Pain**: Location, severity

#### 2. Hormone Replacement Therapy (HRT) Records
- Treatment regimen records (estrogen, progesterone)
- Effectiveness evaluation
- Risk monitoring (breast, endometrium, thrombosis)
- Treatment duration

#### 3. Bone Density Monitoring
- Bone density test records (T-score, Z-score)
- Fracture risk assessment (FRAX)
- Calcium and vitamin D supplementation

#### 4. Cardiovascular Risk Assessment
- Blood lipid monitoring
- Blood pressure monitoring
- Lifestyle recommendations

### Data Structure

```json
{
  "menopause_tracking": {
    "stage": "perimenopausal",
    "age": 48,
    "last_menstrual_period": "2025-11-15",

    "symptoms": {
      "hot_flashes": {
        "present": true,
        "frequency": "5-10_per_day",
        "severity": "moderate",
        "impact_on_life": "mild",
        "triggers": ["stress", "hot_drinks"]
      },
      "sleep_issues": {
        "present": true,
        "frequency": "often",
        "type": "difficulty_falling_asleep",
        "sleep_quality": "poor"
      },
      "mood_changes": {
        "present": true,
        "symptoms": ["anxiety", "irritability"]
      },
      "vaginal_dryness": {
        "present": false,
        "severity": null
      }
    },

    "hrt": {
      "on_treatment": false,
      "medication": null,
      "start_date": null,
      "effectiveness": null,
      "side_effects": null
    },

    "bone_density": {
      "last_check": "2025-06-15",
      "t_score": -1.5,
      "z_score": -1.2,
      "diagnosis": "osteopenia",
      "fracture_risk": "low",
      "calcium_supplement": "1000mg_daily",
      "vitamin_d_supplement": "2000IU_daily"
    },

    "cardiovascular_risk": {
      "blood_pressure": "120/80",
      "total_cholesterol": 5.2,
      "ldl": 3.2,
      "hdl": 1.5,
      "triglycerides": 1.3,
      "risk_level": "low"
    },

    "metadata": {
      "created_at": "2025-01-01T00:00:00.000Z",
      "last_updated": "2025-12-01T00:00:00.000Z"
    }
  }
}
```

### Command Interface

```bash
# Record menopause symptoms
/menopause symptom hot-flashes 5-10 moderate    # Record hot flashes
/menopause symptom sleep insomnia               # Record sleep problems
/menopause symptom mood anxiety                 # Record mood changes

# Record bone density test
/menopause bone-density -1.5 osteopenia         # Record T-score and diagnosis

# Record HRT treatment
/menopause hrt start estradiol 1mg              # Start HRT
/menopause hrt effectiveness good               # Evaluate effectiveness

# View status
/menopause status                               # View menopause status
/menopause risk                                 # View risk assessment
```

---

## Sub-module 3: Gynecological Cancer Screening Tracker

### Feature Description

Management of cervical, ovarian, and endometrial cancer screening plans and result tracking.

### Core Features

#### 1. Screening Plan Management
- **HPV Testing**: High-risk types (16/18), low-risk types
- **TCT (Thin-Prep Cytology)**: Liquid-based cytology
- **Co-testing Strategy**: HPV + TCT
- Screening interval reminders (3 years/5 years)

#### 2. Abnormal Result Tracking
- **ASC-US**: Atypical squamous cells of undetermined significance
- **LSIL/HSIL**: Low/high-grade squamous intraepithelial lesion
- Colposcopy appointment scheduling
- Biopsy result records

#### 3. Gynecological Tumor Markers
- **CA125**: Ovarian cancer (< 35 U/mL)
- **CA19-9**: Ovarian cancer, endometrial cancer (< 37 U/mL)
- **CEA**: Endometrial cancer (< 5 ng/mL)
- **AFP**: Yolk sac tumor (< 10 ng/mL)
- Trend analysis and abnormal alerts

### Data Structure

```json
{
  "cancer_screening": {
    "cervical_cancer": {
      "last_hpv": "2025-01-15",
      "hpv_result": "negative",
      "hpv_type": null,

      "last_tct": "2025-01-15",
      "tct_result": "NILM",
      "tct_details": "Negative for intraepithelial lesion or malignancy",

      "next_screening": "2030-01-15",
      "screening_interval": "5_years",
      "screening_strategy": "co-testing",

      "abnormal_results": []
    },

    "tumor_markers": {
      "CA125": {
        "value": 15.5,
        "reference": "<35",
        "unit": "U/mL",
        "date": "2025-06-20",
        "trend": "stable",
        "history": [18.2, 16.5, 15.5]
      },
      "CA19-9": {
        "value": 22.0,
        "reference": "<37",
        "unit": "U/mL",
        "date": "2025-06-20",
        "trend": "stable"
      }
    },

    "upcoming_appointments": [
      {
        "type": "annual_gyn_exam",
        "date": "2026-01-15"
      }
    ],

    "metadata": {
      "created_at": "2025-01-01T00:00:00.000Z",
      "last_updated": "2025-06-20T00:00:00.000Z"
    }
  }
}
```

### Command Interface

```bash
# Record HPV/TCT screening
/screening hpv negative                    # Record HPV test result
/screening tct NILM                        # Record TCT test result
/screening co-testing negative NILM        # Co-testing record

# Record tumor markers
/screening ca125 15.5                      # Record CA125
/screening ca19-9 22.0                     # Record CA19-9

# Handle abnormal results
/screening abnormal asc-us                # Record abnormal result
/screening colposcopy scheduled 2025-07-01 # Schedule colposcopy

# View status
/screening status                          # View screening status
/screening next                            # Next screening reminder
/screening trend                           # Tumor marker trends
```

---

## Medical Safety Principles

### ⚠️ Safety Boundaries

1. **No specific medication dosages**
   - No specific drug doses recommended
   - Medication safety checks are for reference only

2. **No direct prescription drug names**
   - No specific prescription drugs recommended
   - Drug selection requires physician consultation

3. **No pregnancy outcome judgments**
   - No prediction of miscarriage or preterm birth risk
   - No fetal health evaluation

4. **No replacement of physician diagnosis**
   - All analyses are for reference only
   - Diagnosis must be performed by a qualified physician

### ✅ What the System Can Do

- Pregnancy progress tracking and prenatal visit reminders
- Pregnancy symptom recording and analysis
- Medication safety reference (pregnancy categories)
- Menopause symptom assessment and management recommendations
- Cancer screening plan management
- Abnormal result alerts and recommendations

---

## Important Notes

### Pregnancy Management

- This system cannot replace routine prenatal visits
- All abnormalities require prompt medical attention
- Due date calculations may have margins of error; ultrasound is the gold standard
- Fetal movement monitoring cannot replace medical surveillance

### Menopause Management

- HRT treatment must be carried out under physician guidance
- Regular bone density checks
- Pay attention to cardiovascular health
- Seek medical attention for severe symptoms

### Cancer Screening

- Follow screening guidelines for regular screenings
- Abnormal results require further examination
- Elevated tumor markers do not equal cancer
- Inform your doctor of family history

---

## Reference Resources

- [ACOG Obstetrics and Gynecology Practice Guidelines](https://www.acog.org/)
- [NICE Menopause Management Guidelines](https://www.nice.org.uk/guidance/ng23)
- [USPSTF Cervical Cancer Screening Recommendations](https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/cervical-cancer-screening)

---

**Document Version**: v1.0
**Last Updated**: 2025-12-31
**Maintainer**: SynapseMD
