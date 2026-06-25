# Elderly Health Feature Extension Proposal

**Module Number**: 04
**Category**: Population-Based Classification - Elderly Health
**Status**: ✅ Developed
**Priority**: High
**Created**: 2025-12-31
**Completed**: 2025-01-02

---

## Feature Overview

The Elderly Health module contains three sub-modules that comprehensively cover the unique health needs of older adults:

1. 🧠 **Cognitive Function Assessment** - MMSE/MoCA testing, dementia risk screening
2. 🚶 **Fall Risk Assessment** - Balance function testing, home environment assessment
3. 💊 **Polypharmacy Management** - Beers Criteria screening, drug interaction checks

---

## Sub-module 1: Cognitive Function Assessment

### Feature Description

Cognitive function screening and dementia risk assessment for older adults, helping to detect cognitive decline early.

### Core Features

#### 1. MMSE (Mini-Mental State Examination)

**Test Items** (30 points total):

**Orientation** (10 points):
- Time orientation (5 points): Year, season, month, date, day of week
- Place orientation (5 points): Country, province, city, hospital, floor

**Memory** (3 points):
- Immediate recall of 3 words (1 point each)

**Attention and Calculation** (5 points):
- Serial 7s (subtract 7 from 100 five times, 1 point each)

**Recall** (3 points):
- Delayed recall of the previous 3 words

**Language** (9 points):
- Naming (2 points): Watch, pencil
- Repetition (1 point): Repeat "No ifs, ands, or buts"
- Three-step command (3 points):
  - Take this paper in your right hand
  - Fold it in half
  - Put it on the floor
- Reading comprehension (1 point): "Close your eyes"
- Writing (1 point): Write a complete sentence
- Drawing (1 point): Copy two intersecting pentagons

**Result Interpretation**:
- 27-30 points: Normal
- 21-26 points: Mild cognitive impairment
- 10-20 points: Moderate cognitive impairment
- ≤ 9 points: Severe cognitive impairment

**Influencing Factors**:
- Age
- Education level
- Cultural background

#### 2. MoCA (Montreal Cognitive Assessment)

**Test Scope** (30 points):
- Visuospatial/Executive function (5 points)
- Naming (3 points)
- Memory (0 points, not counted in total)
- Attention (6 points)
- Language (3 points)
- Abstraction (2 points)
- Delayed recall (5 points)
- Orientation (6 points)

**Result Interpretation**:
- ≥ 26 points: Normal
- 18-25 points: Mild cognitive impairment
- 10-17 points: Moderate cognitive impairment
- < 10 points: Severe cognitive impairment

**Education Adjustment**:
- ≤ 12 years of education: Add 1 point

#### 3. Cognitive Domain Assessment

**Memory**:
- Immediate memory
- Short-term memory
- Long-term memory
- Learning ability

**Executive Function**:
- Planning ability
- Problem solving
- Abstract thinking
- Cognitive flexibility

**Language Ability**:
- Comprehension
- Expression
- Naming
- Repetition

**Visuospatial Ability**:
- Object recognition
- Face recognition
- Spatial orientation

**Orientation**:
- Time orientation
- Place orientation
- Person orientation

#### 4. Cognitive Decline Trend Tracking

- Repeated test comparisons
- Rate of decline assessment
- Functional impact assessment
- Activities of daily living assessment

### Data Structure

```json
{
  "cognitive_assessment": {
    "user_id": "user_001",
    "age": 75,
    "education_years": 12,

    "mmse": {
      "date": "2025-06-20",
      "total_score": 27,
      "max_score": 30,
      "interpretation": "normal",

      "subscores": {
        "orientation": {
          "time": 4,
          "place": 5,
          "total": 9
        },
        "registration": 3,
        "attention": 4,
        "recall": 2,
        "language": 9
      },

      "history": [
        {
          "date": "2024-06-20",
          "score": 28
        },
        {
          "date": "2023-06-20",
          "score": 29
        }
      ],

      "trend": "stable_decline",
      "annual_decline": 1.0
    },

    "moca": {
      "date": "2025-06-20",
      "total_score": 24,
      "max_score": 30,
      "education_adjusted": 25,
      "interpretation": "mild_impairment",

      "subscores": {
        "visuospatial_executive": 4,
        "naming": 3,
        "attention": 5,
        "language": 2,
        "abstraction": 2,
        "delayed_recall": 4,
        "orientation": 6
      }
    },

    "cognitive_domains": {
      "memory": {
        "status": "mild_impairment",
        "immediate_recall": "normal",
        "short_term_memory": "mild_impairment",
        "long_term_memory": "normal"
      },
      "executive_function": {
        "status": "normal",
        "planning": "normal",
        "problem_solving": "normal"
      },
      "language": {
        "status": "normal",
        "comprehension": "normal",
        "expression": "normal"
      },
      "visuospatial": {
        "status": "mild_impairment",
        "object_recognition": "normal",
        "spatial_orientation": "mild_impairment"
      }
    },

    "functional_impact": {
      "activities_of_daily_living": {
        "bathing": "independent",
        "dressing": "independent",
        "toileting": "independent",
        "transferring": "independent",
        "continence": "independent",
        "feeding": "independent"
      },
      "instrumental_activities": {
        "shopping": "needs_assistance",
        "cooking": "needs_assistance",
        "managing_medications": "supervision_needed",
        "using_telephone": "independent",
        "managing_finances": "needs_assistance"
      }
    },

    "risk_factors": [
      "age_75",
      "hypertension",
      "education_12_years"
    ],

    "next_assessment": "2026-06-20",
    "recommendations": [
      "annual_cognitive_screening",
      "cardiovascular_risk_management",
      "physical_activity",
      "social_engagement"
    ]
  }
}
```

### Command Interface

```bash
# MMSE test
/cognitive mmse                          # Perform MMSE test
/cognitive mmse score 27                 # Record MMSE score
/cognitive mmse history                  # View MMSE history

# MoCA test
/cognitive moca                          # Perform MoCA test
/cognitive moca score 24                 # Record MoCA score

# Cognitive domain assessment
/cognitive domain memory mild_impairment # Record memory domain assessment
/cognitive domain executive normal       # Record executive function assessment

# Functional assessment
/cognitive adl independent               # Record activities of daily living
/cognitive iadl needs_assistance         # Record instrumental activities of daily living

# View status
/cognitive status                        # View cognitive function status
/cognitive trend                         # View cognitive change trends
/cognitive risk                          # Cognitive function risk assessment
```

---

## Sub-module 2: Fall Risk Assessment

### Feature Description

Fall risk assessment and prevention for older adults, including balance function testing and home environment assessment.

### Core Features

#### 1. Fall Risk Factor Assessment

**Intrinsic Factors**:
- **Age**: > 65 years
- **Fall History**: Previous falls increase risk of future falls
- **Balance Impairment**: Balance disorders
- **Gait Abnormality**: Unsteady gait
- **Muscle Weakness**: Lower limb muscle weakness
- **Vision Problems**: Visual impairment, cataracts, glaucoma
- **Cognitive Function**: Cognitive impairment
- **Chronic Diseases**: Parkinson's, stroke, arthritis
- **Medications**: Sedatives, antihypertensives, hypoglycemics, antidepressants

**Extrinsic Factors**:
- **Environmental Hazards**: Slippery floors, obstacles, poor lighting
- **Footwear**: Inappropriate footwear
- **Assistive Devices**: Not used or used incorrectly

#### 2. Balance Function Testing

**TUG Test** (Timed Up and Go):
- Method: Rise from a chair, walk 3 meters, turn around, walk back, sit down
- Timing: Total time
- Result Interpretation:
  - < 10 seconds: Normal
  - 10-19 seconds: Mostly independent
  - 20-29 seconds: Mobility limitation
  - ≥ 30 seconds: Dependent

**Berg Balance Scale** (56 points):
- 14 balance tasks
- Each task scored 0-4
- Result Interpretation:
  - 0-20 points: Wheelchair-bound
  - 21-40 points: Assisted ambulation
  - 41-56 points: Independent ambulation

**Single Leg Stance Test**:
- Timing: Eyes open/closed single leg stance duration
- Normal: > 30 seconds (< 60 years), > 15 seconds (60-69 years), > 5 seconds (70-79 years)

#### 3. Gait Analysis

**Gait Speed**:
- Normal: > 1.0 m/s
- Mobility limitation: 0.6-1.0 m/s
- Severe limitation: < 0.6 m/s

**Gait Abnormalities**:
- Shortened step length
- Widened base of support
- Unsteady gait
- Shuffling

#### 4. Home Safety Assessment

**Living Room**:
- Non-slip flooring
- Furniture arrangement
- Adequate lighting
- Cord management

**Bedroom**:
- Bedside lamp
- Night light
- Appropriate bed height
- Secured rugs

**Bathroom**:
- Non-slip mat
- Grab bars (toilet, shower area)
- Shower chair
- Easy door access

**Stairs**:
- Handrails
- Non-slip treads
- Lighting
- Clear of clutter

#### 5. Fall Records

- Date and time of fall
- Location of fall
- Cause of fall
- Injuries sustained
- Treatment measures

### Data Structure

```json
{
  "fall_risk_assessment": {
    "user_id": "user_001",
    "age": 78,
    "assessment_date": "2025-06-20",

    "fall_history": {
      "fallen_last_year": true,
      "fall_count_last_year": 2,
      "fall_count_last_6_months": 1,
      "last_fall": {
        "date": "2025-03-15",
        "location": "bathroom",
        "time": "06:00",
        "cause": "slippery_floor",
        "injury": "bruise",
        "required_medical_attention": false,
        "fracture": false
      }
    },

    "risk_factors": {
      "age_over_65": true,
      "previous_falls": true,
      "balance_impairment": true,
      "gait_abnormality": true,
      "muscle_weakness": true,
      "visual_impairment": true,
      "cognitive_impairment": false,
      "medications": [
        "sedatives",
        "antihypertensives",
        "diuretics"
      ],
      "chronic_conditions": [
        "osteoarthritis",
        "hypertension"
      ]
    },

    "balance_tests": {
      "tug_test": {
        "date": "2025-06-20",
        "time_seconds": 18,
        "interpretation": "mobility_limitation",
        "reference": "<10_seconds_normal"
      },

      "berg_balance_scale": {
        "date": "2025-06-20",
        "score": 42,
        "max_score": 56,
        "interpretation": "moderate_risk"
      },

      "single_leg_stance": {
        "date": "2025-06-20",
        "eyes_open_seconds": 8,
        "eyes_closed_seconds": 2,
        "age_reference": ">5_seconds_normal",
        "result": "impaired"
      }
    },

    "gait_analysis": {
      "date": "2025-06-20",
      "speed_m_per_s": 0.8,
      "interpretation": "mobility_impaired",
      "abnormalities": [
        "shortened_step_length",
        "widened_base_of_support",
        "unsteady_gait"
      ]
    },

    "home_safety": {
      "living_room": {
        "floor_slippery": false,
        "adequate_lighting": true,
        "obstacles_removed": true,
        "rugs_secure": true
      },
      "bedroom": {
        "bedside_light": true,
        "night_light": false,
        "bed_height_appropriate": true,
        "clutter_free": true
      },
      "bathroom": {
        "non_slip_mat": true,
        "grab_bars": true,
        "shower_chair": false,
        "easy_access": true
      },
      "stairs": {
        "handrails": true,
        "non_slip_treads": true,
        "adequate_lighting": true,
        "clutter_free": true
      },
      "overall_safety": "good",
      "recommendations": [
        "add_night_light_in_bedroom",
        "consider_shower_chair"
      ]
    },

    "overall_risk": "moderate",
    "risk_score": 12,
    "max_score": 18,

    "interventions": [
      "physical_therapy_for_balance",
      "home_modifications",
      "medication_review",
      "vision_check",
      "appropriate_footwear"
    ],

    "next_assessment": "2025-12-20"
  }
}
```

### Command Interface

```bash
# Record a fall
/fall record 2025-03-15 bathroom slippery  # Record fall event
/fall history                             # View fall history

# Balance testing
/fall tug 18                              # Record TUG test
/fall berg 42                             # Record Berg Balance Scale
/fall single-leg-stance 8                 # Record single leg stance

# Gait analysis
/fall gait speed 0.8                      # Record gait speed
/fall gait abnormal shortened_step        # Record gait abnormality

# Home safety assessment
/fall home living_room floor_slippery true # Assess living room safety
/fall home bathroom grab_bars true        # Assess bathroom safety
/fall home assessment                     # Complete home safety assessment

# Risk assessment
/fall risk                                # Fall risk assessment
/fall risk-factors                        # View risk factors
/fall interventions                       # View intervention recommendations
```

---

## Sub-module 3: Polypharmacy Management

### Feature Description

Polypharmacy management and drug interaction checks for older adults, identifying potentially inappropriate medications.

### Core Features

#### 1. Medication List Management

- Current medication list
- Medication indications
- Dosage and frequency
- Duration of use
- Prescribing physician

#### 2. Potentially Inappropriate Medication Screening

**Beers Criteria** (2019 edition):
- Potentially inappropriate medications for older adults
- Potentially inappropriate medications for older adults based on disease/condition
- Medications to use with caution in older adults
- Non-anti-infective medications that interact with diseases in older adults
- Independent prescribing cascades based on Beers Criteria for older adults

**Common Potentially Inappropriate Medications**:
- Benzodiazepines (falls, over-sedation)
- Anticholinergic drugs (cognitive impairment, constipation)
- First-generation antihistamines (sedation, anticholinergic effects)
- NSAIDs (gastrointestinal bleeding, renal impairment)
- Corticosteroids (long-term use)
- Warfarin (bleeding risk)

#### 3. Drug Interaction Checks

**Drug-Drug Interactions**:
- Warfarin + aspirin (bleeding risk)
- ACEIs + potassium-sparing diuretics (hyperkalemia)
- Beta-blockers + digoxin (bradycardia)
- Antidepressants + MAOIs (serotonin syndrome)

**Drug-Disease Interactions**:
- NSAIDs + peptic ulcer (worsens ulcer)
- Beta-blockers + asthma (worsens asthma)
- Anticholinergics + constipation/glaucoma (worsens symptoms)
- Corticosteroids + diabetes/osteoporosis (worsens disease)

#### 4. Anticholinergic Drug Burden

**Anticholinergic Drug Score**:
- Each drug scored 0-3 points
- Cumulative total score
- Result Interpretation:
  - 0-1 points: Acceptable
  - 2-3 points: Avoid if possible
  - ≥ 4 points: Significant risk

**Common Anticholinergic Drugs**:
- Benzodiazepines
- Antihistamines
- Tricyclic antidepressants
- Antipsychotics
- Anti-Parkinson's drugs
- Bladder anticholinergics

#### 5. Deprescribing Plan

**Deprescribing Principles**:
- Discontinue medications without clear indications
- Discontinue medications with poor efficacy
- Discontinue preventive medications (where benefit is unclear)
- Reduce the number of medications
- Simplify dosing regimens

**Deprescribing Steps**:
- Assess each medication's indication
- Assess risks and benefits of each medication
- Identify medications that can be discontinued
- Develop a tapering plan
- Monitor response to dose reduction

### Data Structure

```json
{
  "polypharmacy_management": {
    "user_id": "user_001",
    "age": 82,
    "assessment_date": "2025-06-20",

    "medication_list": [
      {
        "name": "Aspirin",
        "dose": "100mg",
        "frequency": "qd",
        "indication": "cardiovascular_protection",
        "start_date": "2015-01-01",
        "prescriber": "cardiologist",
        "appropriate": true,
        "beers_criteria": false
      },
      {
        "name": "Amlodipine",
        "dose": "5mg",
        "frequency": "qd",
        "indication": "hypertension",
        "start_date": "2018-03-15",
        "prescriber": "gp",
        "appropriate": true,
        "beers_criteria": false
      },
      {
        "name": "Diazepam",
        "dose": "5mg",
        "frequency": "prn",
        "indication": "insomnia",
        "start_date": "2020-06-01",
        "prescriber": "gp",
        "appropriate": false,
        "beers_criteria": true,
        "beers_recommendation": "avoid",
        "alternative": "melatonin_sleep_hygiene"
      }
    ],

    "total_medications": 8,
    "prescribed_medications": 6,
    "otc_medications": 2,

    "beers_criteria_violations": [
      {
        "medication": "Diazepam",
        "issue": "falls_risk_sedation",
        "recommendation": "avoid_use",
        "severity": "high",
        "alternative": "melatonin_cbt_i"
      },
      {
        "medication": "Chlorphenamine",
        "issue": "anticholinergic_effects",
        "recommendation": "avoid_use",
        "severity": "moderate",
        "alternative": "loratadine"
      }
    ],

    "drug_interactions": [
      {
        "medications": ["Warfarin", "Aspirin"],
        "severity": "moderate",
        "interaction": "increased_bleeding_risk",
        "recommendation": "monitor_inr",
        "clinically_significant": true
      },
      {
        "medications": ["Digoxin", "Furosemide"],
        "severity": "moderate",
        "interaction": "increased_digoxin_toxicity_risk",
        "recommendation": "monitor_digoxin_level_electrolytes",
        "clinically_significant": true
      }
    ],

    "disease_drug_interactions": [
      {
        "medication": "Ibuprofen",
        "condition": "chronic_kidney_disease_stage_3",
        "interaction": "worsens_renal_function",
        "recommendation": "avoid_use_use_acetaminophen",
        "severity": "high"
      }
    ],

    "anticholinergic_burden": {
      "total_score": 4,
      "medications_contributing": [
        {"name": "Diazepam", "score": 1},
        {"name": "Chlorphenamine", "score": 2},
        {"name": "Oxybutynin", "score": 1}
      ],
      "interpretation": "significant_risk",
      "risks": ["cognitive_impairment", "falls", "dry_mouth", "constipation"]
    },

    "deprescribing_plan": [
      {
        "medication": "Diazepam",
        "action": "taper",
        "timeline": "4-8_weeks",
        "taper_schedule": "reduce_by_25_every_1-2_weeks",
        "alternative": "sleep_hygiene_melatonin",
        "monitoring": ["withdrawal_symptoms", "sleep_quality"]
      },
      {
        "medication": "Chlorphenamine",
        "action": "switch",
        "alternative": "loratadine",
        "timeline": "immediate",
        "reason": "reduce_anticholinergic_burden"
      }
    ],

    "medication_adherence": {
      "overall_adherence": "good",
      "missed_doses_weekly": 1,
      "barriers": ["pill_burden", "cost"],
      "aids": ["pill_box", "reminder_app"]
    },

    "next_medication_review": "2025-09-20",
    "recommendations": [
      "deprescribe_diazepam",
      "review_antihistamine_use",
      "consolidate_medications",
      "simplify_dosing_schedule"
    ]
  }
}
```

### Command Interface

```bash
# Record medications
/polypharmacy add aspirin 100mg qd        # Add medication
/polypharmacy list                         # View medication list

# Beers Criteria screening
/polypharmacy beers                        # Beers Criteria screening
/polypharmacy inappropriate                # View potentially inappropriate medications

# Drug interactions
/polypharmacy interaction check            # Check drug interactions
/polypharmacy interaction add warfarin aspirin moderate  # Add interaction

# Anticholinergic burden
/polypharmacy anticholinergic              # Calculate anticholinergic burden
/polypharmacy acb-score 4                  # Record ACB score

# Deprescribing
/polypharmacy deprescribe                  # Generate deprescribing plan
/polypharmacy deprescribe diazepam taper   # Add medication to deprescribe

# View status
/polypharmacy status                       # View polypharmacy status
/polypharmacy recommendations              # View recommendations
```

---

## Medical Safety Principles

### ⚠️ Safety Boundaries

1. **No cognitive impairment diagnosis**
   - No dementia diagnosis
   - Diagnosis requires a neurologist/geriatrician

2. **No management of fall injuries**
   - Fall injuries require medical attention
   - System only records and assesses

3. **No medication adjustments**
   - No medication adjustment recommendations
   - Adjustments require physician evaluation

4. **No replacement of professional assessment**
   - Cognitive function requires professional assessment
   - Medications require pharmacist/physician guidance

### ✅ What the System Can Do

- Cognitive function screening
- Cognitive decline trend tracking
- Fall risk assessment
- Balance function test recording
- Medication list management
- Potentially inappropriate medication screening
- Drug interaction checks
- Deprescribing plan recommendations

---

## Important Notes

### Cognitive Function Assessment

- Regular screening (annually)
- Note the influence of education level and cultural background
- Combine with daily functional assessment
- Abnormal results require medical confirmation

### Fall Prevention

- Identify high-risk individuals
- Improve home environment
- Balance and strength training
- Medication review
- Vision correction

### Polypharmacy Management

- Regular medication reviews
- Avoid potentially inappropriate medications
- Reduce the number of medications
- Simplify dosing regimens
- Improve adherence

---

## Reference Resources

### Cognitive Function
- [NIA-AA Diagnostic Criteria for Dementia](https://www.nia.nih.gov/health/alzheimers-disease-fact-sheet)
- [Chinese Dementia Diagnosis and Treatment Guidelines](http://www.cma.org.cn/)

### Fall Prevention
- [AGS Fall Prevention Guidelines](https://www.americangeriatrics.org/)
- [Elderly Fall Risk Assessment](https://www.cdc.gov/)

### Polypharmacy
- [Beers Criteria 2019 Edition](https://www.americangeriatrics.org/)
- [List of Potentially Inappropriate Medications for Chinese Elderly](http://www.cma.org.cn/)

---

**Document Version**: v1.0
**Last Updated**: 2025-12-31
**Maintainer**: WellAlly Tech
