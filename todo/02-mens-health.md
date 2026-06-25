# Men's Health Feature Extension Proposal

**Module Number**: 02
**Category**: Population-Based Classification - Men's Health
**Status**: ✅ Implemented
**Priority**: Medium
**Created**: 2025-12-31
**Completed**: 2026-01-02
---

## Feature Overview

The Men's Health module contains three sub-modules that comprehensively cover men's health needs across different life stages:

1. 👨 **Prostate Health Management System** - PSA monitoring, IPSS symptom scoring
2. 👶 **Male Infertility Management** - Semen analysis, hormone level assessment
3. 👴 **Male Menopause Management** - Testosterone monitoring, TRT treatment records

---

## Sub-module 1: Prostate Health Management System

### Feature Description

Prostate disease risk assessment and screening management, including prostate cancer and benign prostatic hyperplasia (BPH).

### Core Features

#### 1. Prostate-Specific Antigen (PSA) Monitoring
- **Total PSA** (tPSA): < 4.0 ng/mL (general reference value)
- **Free PSA** (fPSA)
- **Free/Total PSA Ratio** (fPSA/tPSA): > 0.25 suggests benign
- **PSA Density** (PSAD): PSA / prostate volume
- **PSA Velocity** (PSAV): > 0.75 ng/mL/year suggests risk

#### 2. Prostate Symptom Assessment

**IPSS Score** (International Prostate Symptom Score, 0-35 points):

**Incomplete Emptying**:
- 0: Not at all
- 1: Less than 1 in 5 times
- 2: Less than half the time
- 3: About half the time
- 4: More than half the time
- 5: Almost always

**Frequency**:
- 0: Not at all
- 1: Less than 1 in 5 times
- 2: Less than half the time
- 3: About half the time
- 4: More than half the time
- 5: Almost always

**Intermittency**, **Urgency**, **Weak Stream**, **Straining**, **Nocturia**: Scored the same as above

**Result Interpretation**:
- 0-7 points: Mild
- 8-19 points: Moderate
- 20-35 points: Severe

#### 3. Prostate Examination Schedule
- **Digital Rectal Exam (DRE)**: Annually from age 50
- **Prostate Ultrasound**: When necessary
- **Prostate MRI**: When PSA is elevated
- **Prostate Biopsy**: When cancer is suspected

#### 4. Prostate Cancer Risk Assessment
- **Age Factor**: > 50 years (average risk), > 45 years (high risk)
- **Family History**: Father or brother with prostate cancer
- **Racial Factor**: African Americans at higher risk
- **Screening Recommendations**: Individualized risk-based screening

### Data Structure

```json
{
  "prostate_health": {
    "user_id": "user_001",
    "age": 55,
    "family_history": {
      "father": false,
      "brother": true,
      "age_at_diagnosis": 62
    },

    "psa_history": [
      {
        "date": "2025-06-15",
        "total_psa": 2.5,
        "free_psa": 0.8,
        "ratio": 0.32,
        "reference": "<4.0",
        "unit": "ng/mL",
        "trend": "stable"
      },
      {
        "date": "2024-06-15",
        "total_psa": 2.4,
        "free_psa": 0.75,
        "ratio": 0.31
      }
    ],

    "psa_velocity": {
      "change_per_year": 0.1,
      "threshold": 0.75,
      "interpretation": "normal"
    },

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
    },

    "prostate_volume": {
      "date": "2025-03-15",
      "volume_ml": 32,
      "interpretation": "mild_enlargement"
    },

    "dre": {
      "last_exam": "2025-06-15",
      "findings": "normal",
      "nodule": false
    },

    "screening_plan": {
      "psa_frequency": "annual",
      "dre_frequency": "annual",
      "next_psa": "2026-06-15",
      "next_dre": "2026-06-15",
      "risk_category": "average"
    },

    "urinary_symptoms": {
      "stream_weakness": "mild",
      "frequency": "3-4_times_per_day",
      "nocturia": 2,
      "urgency": "occasional"
    }
  }
}
```

### Command Interface

```bash
# Record PSA test
/prostate psa 2.5                        # Record total PSA
/prostate psa 2.5 free 0.8               # Record total PSA and free PSA
/prostate psa history                    # View PSA trends

# IPSS scoring
/prostate ipss                           # Perform IPSS scoring
/prostate ipss incomplete_emptying 1     # Record individual symptom score

# Record examinations
/prostate dre normal                     # Record digital rectal exam
/prostate ultrasound 32ml                # Record prostate ultrasound

# View status
/prostate status                         # View prostate health status
/prostate screening                      # View screening plan
/prostate risk                           # Prostate cancer risk assessment
```

---

## Sub-module 2: Male Infertility Management

### Feature Description

Semen analysis records and male infertility factor assessment to assist in the diagnosis and treatment of male infertility.

### Core Features

#### 1. Semen Analysis Records

**Semen Volume**:
- Normal: ≥ 1.5 mL
- Abnormal: < 1.5 mL (hypospermia)

**Sperm Concentration**:
- Normal: ≥ 15 × 10⁶/mL
- Oligospermia: < 15 × 10⁶/mL
- Azoospermia: 0 × 10⁶/mL

**Total Sperm Count**:
- Normal: ≥ 39 × 10⁶/ejaculate

**Sperm Motility** (PR + NP):
- PR (Progressive motility): ≥ 32%
- NP (Non-progressive motility): ≥ 40%
- Asthenospermia: < 32%

**Sperm Morphology**:
- Normal morphology rate: ≥ 4%
- Teratospermia: < 4%

**Semen pH**:
- Normal: 7.2-8.0
- Abnormal: < 7.2 or > 8.0

**Liquefaction Time**:
- Normal: ≤ 60 minutes

#### 2. Hormone Level Monitoring

**Testosterone (T)**:
- Total testosterone: 10-35 nmol/L
- Free testosterone: 0.22-0.65 nmol/L

**Luteinizing Hormone (LH)**:
- Normal: 1.7-8.6 IU/L

**Follicle-Stimulating Hormone (FSH)**:
- Normal: 1.5-12.4 IU/L

**Prolactin (PRL)**:
- Normal: < 15 ng/mL

**Estradiol (E2)**:
- Normal: < 70 pg/mL

#### 3. Infertility Factor Assessment

**Primary Infertility**:
- Never caused a partner to become pregnant

**Secondary Infertility**:
- Previously caused a partner to become pregnant, now unable

**Varicocele**:
- Ultrasound grading
- Surgical treatment

**Reproductive Tract Infections**:
- Gonorrhea, Chlamydia
- Antibiotic treatment

**Endocrine Abnormalities**:
- Hypogonadotropic hypogonadism
- Hyperprolactinemia

**Genetic Factors**:
- Y chromosome microdeletion
- CFTR gene mutation

**Obstructive Factors**:
- Vasectomy
- Congenital absence of vas deferens

### Data Structure

```json
{
  "fertility_assessment": {
    "user_id": "user_001",
    "age": 35,
    "infertility_type": "primary",
    "partner_age": 32,
    "trying_to_conceive_months": 18,

    "semen_analysis": {
      "date": "2025-06-20",
      "abstinence_period": "3_days",

      "volume": {
        "value": 2.5,
        "unit": "mL",
        "reference": "≥1.5",
        "result": "normal"
      },

      "concentration": {
        "value": 45,
        "unit": "10⁶/mL",
        "reference": "≥15",
        "result": "normal"
      },

      "total_count": {
        "value": 112.5,
        "unit": "10⁶",
        "reference": "≥39",
        "result": "normal"
      },

      "motility": {
        "pr": {
          "value": 35,
          "reference": "≥32",
          "result": "normal"
        },
        "np": {
          "value": 20,
          "reference": "≥40",
          "result": "normal"
        },
        "im": {
          "value": 45,
          "result": "normal"
        }
      },

      "morphology": {
        "value": 4,
        "unit": "%",
        "reference": "≥4",
        "result": "normal"
      },

      "ph": {
        "value": 7.5,
        "reference": "7.2-8.0",
        "result": "normal"
      },

      "liquefaction": {
        "value": 30,
        "unit": "minutes",
        "reference": "≤60",
        "result": "normal"
      },

      "diagnosis": "normospermia"
    },

    "hormones": {
      "date": "2025-06-15",
      "testosterone": {
        "total": 15.5,
        "reference": "10-35",
        "unit": "nmol/L",
        "result": "normal"
      },
      "lh": {
        "value": 5.2,
        "reference": "1.7-8.6",
        "unit": "IU/L",
        "result": "normal"
      },
      "fsh": {
        "value": 8.1,
        "reference": "1.5-12.4",
        "unit": "IU/L",
        "result": "normal"
      },
      "prl": {
        "value": 12.5,
        "reference": "<15",
        "unit": "ng/mL",
        "result": "normal"
      },
      "e2": {
        "value": 35,
        "reference": "<70",
        "unit": "pg/mL",
        "result": "normal"
      }
    },

    "varicocele": {
      "present": false,
      "grade": null,
      "side": null,
      "surgery": false
    },

    "infections": {
      "chlamydia": "negative",
      "gonorrhea": "negative",
      "date": "2025-06-10"
    },

    "genetic_testing": {
      "y_chromosome_microdeletion": "not_done",
      "cftr_mutation": "not_done"
    },

    "recommendations": [
      "continue_trying",
      "healthy_lifestyle",
      "repeat_semen_analysis_in_3_months"
    ]
  }
}
```

### Command Interface

```bash
# Record semen analysis
/fertility semen volume 2.5              # Record semen volume
/fertility semen concentration 45        # Record sperm concentration
/fertility semen motility pr 35 np 20    # Record sperm motility
/fertility semen morphology 4            # Record sperm morphology
/fertility semen complete                # Complete semen analysis record

# Record hormones
/fertility hormone testosterone 15.5     # Record testosterone
/fertility hormone lh 5.2                # Record LH
/fertility hormone fsh 8.1               # Record FSH

# Record examination results
/fertility varicocele none               # Record varicocele examination
/fertility infection chlamydia negative   # Record infection test

# View status
/fertility status                        # View reproductive health status
/fertility diagnosis                     # View diagnosis results
/fertility recommendations               # View recommendations
```

---

## Sub-module 3: Male Menopause Management

### Feature Description

Management of hypogonadism (male menopause) in middle-aged and older men, including symptom assessment and testosterone replacement therapy (TRT).

### Core Features

#### 1. Symptom Assessment

**Sexual Symptoms**:
- Decreased libido
- Erectile dysfunction
- Reduced erectile quality

**Physical Symptoms**:
- Decreased energy
- Reduced muscle mass
- Increased fat (especially abdominal)
- Decreased bone density
- Hot flashes, night sweats

**Psychological Symptoms**:
- Low mood
- Irritability
- Anxiety
- Memory decline
- Difficulty concentrating

#### 2. Testosterone Level Monitoring

**Total Testosterone**:
- Normal: 10-35 nmol/L
- Possible hypogonadism: < 10 nmol/L
- Confirmed hypogonadism: < 8 nmol/L (repeated measurement)

**Timing of Measurement**:
- Morning (8-11 AM) testosterone levels are highest
- At least 2 measurements required for confirmation

**Free Testosterone**:
- More accurately reflects active testosterone
- Measured when needed

**Sex Hormone-Binding Globulin (SHBG)**:
- Affects total testosterone levels
- Increases with age

#### 3. Testosterone Replacement Therapy (TRT) Records

**Treatment Indications**:
- Total testosterone < 8 nmol/L + symptoms
- Total testosterone 8-12 nmol/L + significant symptoms

**Treatment Methods**:
- **Oral**: Testosterone undecanoate
- **Injection**: Testosterone esters
- **Gel**: Testosterone gel
- **Patch**: Testosterone patch

**Effectiveness Assessment**:
- Improved libido
- Improved erectile function
- Improved mood
- Improved energy levels
- Increased muscle mass
- Reduced fat

**Side Effect Monitoring**:
- Polycythemia (Hct > 54%)
- Prostate: PSA, prostate volume
- Cardiovascular events
- Liver function
- Fatty liver

### Data Structure

```json
{
  "andropause": {
    "user_id": "user_001",
    "age": 52,
    "assessment_date": "2025-06-20",

    "symptoms": {
      "sexual": {
        "libido": "decreased",
        "erectile_function": "mild_ed",
        "morning_erection": "reduced"
      },
      "physical": {
        "fatigue": "moderate",
        "muscle_mass": "decreased",
        "body_fat": "increased_abdominal",
        "hot_flashes": false
      },
      "psychological": {
        "mood": "depressed",
        "irritability": true,
        "memory": "mild_impairment",
        "concentration": "difficult"
      }
    },

    "testosterone_levels": {
      "total_testosterone": {
        "date": "2025-06-15",
        "time": "09:00",
        "value": 7.5,
        "reference": "10-35",
        "unit": "nmol/L",
        "result": "low",
        "confirmed": true,
        "repeat_count": 2
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
    },

    "questionnaire_scores": {
      "adam": {
        "score": 8,
        "positive": true,
        "questions": [
          "Do you have a decrease in libido?",
          "Do you have a lack of energy?",
          "Do you have a decrease in strength or endurance?",
          "Have you lost height?",
          "Have you noticed a decreased enjoyment of life?",
          "Are you sad or grumpy?",
          "Are your erections less strong?",
          "Have you noticed a recent deterioration in your ability to play sports?",
          "Are you falling asleep after dinner?",
          "Has there been a recent deterioration in your work performance?"
        ]
      },
      "ams": {
        "score": 27,
        "severity": "moderate"
      }
    },

    "trt": {
      "on_treatment": false,
      "medication": null,
      "dose": null,
      "frequency": null,
      "route": null,
      "started_date": null,
      "effectiveness": null,
      "side_effects": []
    },

    "monitoring": {
      "psa": {
        "baseline": 2.0,
        "current": 2.1,
        "date": "2025-06-15"
      },
      "hematocrit": {
        "baseline": 45,
        "current": 46,
        "date": "2025-06-15",
        "threshold": 54
      },
      "prostate_volume": {
        "baseline": 28,
        "current": null
      }
    },

    "recommendations": [
      "confirm_testosterone_with_repeat_test",
      "consider_trt_if_symptoms_bothersome",
      "lifestyle_modifications",
      "monitor_bone_density"
    ]
  }
}
```

### Command Interface

```bash
# Record symptoms
/andropause symptom libido decreased      # Record decreased libido
/andropause symptom fatigue moderate      # Record fatigue
/andropause symptom mood depressed        # Record low mood

# Record testosterone levels
/andropause testosterone 7.5 09:00        # Record total testosterone and measurement time
/andropause free-testosterone 0.18        # Record free testosterone

# Questionnaire assessment
/andropause adam                          # ADAM questionnaire
/andropause ams                           # AMS questionnaire

# TRT treatment
/andropause trt start gel 50mg daily      # Start TRT treatment
/andropause trt effectiveness good        # Evaluate effectiveness
/andropause trt side-effects              # Record side effects

# Monitoring
/andropause monitor psa 2.1               # Record PSA
/andropause monitor hematocrit 46         # Record hematocrit

# View status
/andropause status                        # View male menopause status
/andropause diagnosis                     # View diagnosis
```

---

## Medical Safety Principles

### ⚠️ Safety Boundaries

1. **No specific medication dosages**
   - TRT dosage must be determined by a physician
   - No specific drugs recommended

2. **No male infertility diagnosis**
   - No diagnostic conclusions
   - Diagnosis requires a specialist in andrology

3. **No prostate cancer risk judgments**
   - No cancer risk assessment
   - Elevated PSA requires urology evaluation

4. **No replacement of professional treatment**
   - Infertility requires a reproductive medicine center
   - TRT requires endocrinology or urology

### ✅ What the System Can Do

- PSA monitoring and trend analysis
- Prostate symptom assessment
- Semen analysis records
- Hormone level tracking
- Male menopause symptom assessment
- TRT treatment records and monitoring

---

## Important Notes

### Prostate Health

- Regular PSA screening (risk-based)
- Elevated PSA requires further evaluation
- DRE combined with PSA improves detection rate
- Family history warrants earlier screening

### Male Infertility

- Semen analysis requires 2-3 confirmations
- 3-7 days abstinence before testing
- Avoid high temperatures, toxins, and radiation
- Maintain a healthy lifestyle

### Male Menopause

- Symptoms + low testosterone required for diagnosis
- Other diseases must be excluded
- TRT requires physician prescription
- Regular monitoring for side effects

---

## Reference Resources

### Prostate Health
- [EAU Prostate Cancer Guidelines](https://uroweb.org/guideline/prostate-cancer/)
- [Chinese Prostate Cancer Diagnosis and Treatment Guidelines](https://www.caca.org.cn/)

### Male Infertility
- [EAU Male Sexual Health Guidelines](https://uroweb.org/guideline/male-sexual-health/)
- [WHO Laboratory Manual for the Examination and Processing of Human Semen](https://www.who.int/)

### Male Menopause
- [ISSAM Guidelines on Male Hypogonadism](https://www.isaam.org/)
- [Chinese Society of Andrology Guidelines](http://www.cuam.org.cn/)

---

**Document Version**: v1.0
**Last Updated**: 2025-12-31
**Maintainer**: SynapseMD
