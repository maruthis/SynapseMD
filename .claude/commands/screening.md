---
description: Manage gynecological cancer screening and tumor markers
arguments:
  - name: action
    description: "Action type: hpv (HPV test) / tct (TCT test) / co-testing (combined screening) / marker (tumor markers) / abnormal (abnormal results) / status (status) / next (next screening)"
    required: true
  - name: info
    description: "Screening information (test results, values, dates, etc., in natural language)"
    required: false
---

# Gynecological Cancer Screening Tracking

Cervical cancer, ovarian cancer, and endometrial cancer screening plan management and result tracking.

## Action Types

### 1. Record HPV Test - `hpv`

Record HPV (Human Papillomavirus) test results.

**Parameter description:**
- `info`: HPV test result (required)
  - Result: negative, positive, positive type (16, 18, 31, 33, 52, 58, etc.)

**Examples:**
```
/screening hpv negative
/screening hpv positive 16
/screening hpv positive 18
/screening hpv positive 52 58
/screening hpv 2025-01-15 negative
```

**Execution steps:**

#### 1. Parse HPV result

**Result identification:**
- negative → negative
- positive → positive
- Numbers 16, 18, 31, 33, 45, 52, 58 → HPV type

**HPV type classification:**

| Risk level | HPV types |
|-----------|-----------|
| High risk (highest) | 16, 18 |
| High risk (other) | 31, 33, 35, 39, 45, 51, 52, 56, 58, 59 |
| Low risk | 6, 11, 40, 42, 43, 44, 54, 61, 70, 72, 81 |

#### 2. Risk assessment and management recommendations

**HPV negative:**
```
HPV Negative

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current risk: Low

Management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Continue routine screening
- Ages 21-29: TCT every 3 years
- Ages 30-65: TCT+HPV every 5 years
- Or TCT every 3 years

Next screening:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Determined based on age and screening strategy
(Usually 3-5 years from now)
```

**HPV 16/18 positive (highest risk):**
```
HPV 16/18 Positive (Highest Risk)

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current risk: High

HPV 16/18 are the main types that cause cervical cancer,
accounting for approximately 70% of cervical cancer cases.

Immediate action:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Colposcopy immediately
Cervical biopsy may be needed

Do not wait, do not panic:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- HPV positive does not equal cancer
- Most HPV infections clear within 1-2 years
- Types 16/18 are more persistent and require close monitoring

Colposcopy:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Magnified examination of the cervix and vagina
- Identifies abnormal areas
- Biopsy may be taken
- Minimally uncomfortable, no anesthesia needed

Follow-up management:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on colposcopy results:
- Normal: Recheck HPV+TCT in 6 months
- Abnormal: Managed based on degree of abnormality

Important note:
Please contact your gynecologist immediately for colposcopy!
```

**Other high-risk HPV positive (31, 33, 52, 58, etc.):**
```
High-Risk HPV Positive

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current risk: Moderate-high

Infected types: HPV 52, 58

Management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Option 1: Immediate colposcopy
  - Advantage: Early detection
  - Disadvantage: Additional examination

Option 2: Recheck in 1 year
  - Repeat HPV+TCT
  - If still positive: colposcopy
  - If negative: routine screening

Consultation recommended:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Please discuss with your gynecologist to
choose the most appropriate plan.

In most cases:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Your doctor may recommend:
1. Immediate TCT (if not already done)
2. Determine next steps based on TCT result
3. If TCT abnormal: colposcopy
4. If TCT normal: recheck in 1 year

Lifestyle:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Quit smoking (smoking reduces the ability to clear HPV)
- Healthy diet, strengthen immunity
- Regular exercise
- Adequate sleep
- HPV vaccination (can prevent other types)
```

#### 3. Update screening records

**HPV data structure:**
```json
{
  "cervical_cancer": {
    "last_hpv": "2025-01-15",
    "hpv_result": "positive",
    "hpv_type": "16",
    "hpv_risk_level": "high",
    "hpv_method": "PCR",
    "hpv_high_risk_types": ["16"],
    "hpv_all_types": [],

    "last_tct": null,
    "tct_result": null,

    "last_co_testing": null,
    "co_testing_result": null,

    "screening_strategy": "co-testing",
    "screening_interval": "5_years",
    "age_appropriate_interval": true,

    "next_screening": null,
    "next_screening_type": "colposcopy",
    "days_until_next": 0,

    "abnormal_results": [
      {
        "result_id": "abn_20250115",
        "result_type": "hpv_positive",
        "hpv_type": "16",
        "date_identified": "2025-01-15",
        "follow_up": "colposcopy",
        "follow_up_status": "scheduled",
        "follow_up_date": "2025-02-01",
        "resolved": false
      }
    ],

    "total_screenings": 5,
    "first_screening": "2010-01-15",
    "screening_history": []
  }
}
```

#### 4. Output confirmation

**HPV negative output:**
```
HPV test record updated

HPV test information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test date: January 15, 2025
HPV result: Negative

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current cervical cancer risk: Low

Screening strategy:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Combined screening (HPV+TCT)
Screening interval: 5 years

Next screening:
━━━━━━━━━━━━━━━━━━━━━━━━━━
January 15, 2030 (1825 days from now)

Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Keep up with regular screenings!
HPV vaccination can prevent other high-risk types.
```

---

### 2. Record TCT Test - `tct`

Record TCT (Liquid-Based Cytology) test results.

**Parameter description:**
- `info`: TCT test result (required)
  - Result: NILM, ASC-US, ASC-H, LSIL, HSIL, AGC, cancer

**Examples:**
```
/screening tct NILM
/screening tct ASC-US
/screening tct LSIL
/screening tct HSIL
/screening tct atypical-squamous-cells undetermined-significance
```

**Execution steps:**

#### 1. Parse TCT result

**TCT result classification (Bethesda system):**

| Result type | Abbreviation | Clinical significance | Risk |
|-------------|-------------|----------------------|------|
| Negative | NILM | No intraepithelial lesion or malignancy | Normal |
| Atypical squamous cells, undetermined significance | ASC-US | Mild abnormality, undetermined significance | Low |
| Atypical squamous cells, cannot exclude HSIL | ASC-H | Possible HSIL | Moderate-high |
| Low-grade squamous intraepithelial lesion | LSIL | CIN 1 | Low-moderate |
| High-grade squamous intraepithelial lesion | HSIL | CIN 2/3 | High |
| Atypical glandular cells | AGC | Glandular cell abnormality | Moderate-high |
| Cancer | Cancer | Invasive carcinoma | Very high |

**Result identification:**
| User input | Standard result |
|-----------|----------------|
| NILM, negative, normal | NILM |
| ASC-US, atypical squamous cells, undetermined significance | ASC-US |
| ASC-H, atypical squamous cells cannot exclude HSIL | ASC-H |
| LSIL, low-grade lesion, CIN1 | LSIL |
| HSIL, high-grade lesion, CIN2, CIN3 | HSIL |
| AGC, atypical glandular cells | AGC |
| cancer | Cancer |

#### 2. Result interpretation and management

**NILM (Negative):**
```
TCT result: NILM (Negative)

Result interpretation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
No intraepithelial lesion or malignancy detected
Cervical cells normal

Management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Continue routine screening
- Ages 21-29: TCT every 3 years
- Ages 30-65: TCT+HPV every 5 years

Next screening:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Determined based on age and screening strategy
```

**ASC-US (Atypical squamous cells, undetermined significance):**
```
TCT result: ASC-US

Result interpretation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Mild cytological abnormality
May be an inflammatory reaction or early lesion

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
CIN 2+ risk: approximately 5-10%

Management options:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Option 1: Reflex HPV testing (recommended)
  - Advantage: Triage management
  - HPV negative: recheck in 3 years
  - HPV positive: colposcopy

Option 2: Repeat TCT in 1 year
  - Repeat TCT+HPV
  - Decide based on result

Option 3: Immediate colposcopy
  - If follow-up is inconvenient

Recommendation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
HPV testing recommended (if not done simultaneously),
next steps based on HPV result.

Note:
Most ASC-US cases return to normal,
but follow-up per doctor's instructions is required.
```

**LSIL (Low-grade squamous intraepithelial lesion):**
```
TCT result: LSIL

Result interpretation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Low-grade squamous intraepithelial lesion
Corresponds to CIN 1

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
CIN 2+ risk: approximately 15-20%
Risk of progression to invasive cancer: <1%

Management option:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Preferred: Recheck TCT+HPV in 1 year

Management pathway:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Recheck TCT+HPV in 1 year
2. If LSIL persists: colposcopy
3. If returns to normal: routine screening
4. If progresses: colposcopy

Prognosis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- 60% of LSIL cases regress spontaneously within 1-2 years
- Only about 10% progress to HSIL
- Very rarely progresses directly to cancer

Recommendation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Follow up regularly per doctor's instructions;
treatment is usually not required.

Lifestyle:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Quit smoking (smoking increases risk of progression)
- HPV vaccination
- Strengthen immunity
```

**HSIL (High-grade squamous intraepithelial lesion):**
```
TCT result: HSIL

Result interpretation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
High-grade squamous intraepithelial lesion
Corresponds to CIN 2/3

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
CIN 2+ risk: >50%
Risk of progression to invasive cancer if untreated:
  - CIN 2: approximately 5%
  - CIN 3: approximately 15-30%

Immediate action:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Immediate colposcopy + biopsy
Treatment plan based on biopsy results

Do not wait!
━━━━━━━━━━━━━━━━━━━━━━━━━━
HSIL is a precancerous lesion
requiring timely assessment and treatment.

Colposcopy + biopsy:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Determine degree of lesion (CIN 2 or CIN 3)
- Rule out invasive cancer
- Guide treatment plan

Possible treatment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
CIN 2:
  - Observation (young women)
  - Or treatment (LEEP, cryotherapy, etc.)

CIN 3:
  - Treatment usually required
  - LEEP, cryotherapy, laser, etc.

Post-treatment follow-up:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Regular TCT+HPV rechecks after treatment
- Usually every 6 months for several years
- Cure rate >90%

Important note:
Please contact your gynecologist immediately for colposcopy!
```

**AGC (Atypical glandular cells):**
```
TCT result: AGC

Result interpretation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Atypical glandular cells
May originate from the cervix or endometrium

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Higher risk (may conceal serious lesions)

Immediate assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Immediate colposcopy
Endocervical sampling
Endometrial biopsy (especially age >35)

Do not wait!
━━━━━━━━━━━━━━━━━━━━━━━━━━
AGC may conceal:
- CIN 2/3
- Glandular precancerous lesions
- Invasive carcinoma

Comprehensive assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Colposcopy + cervical biopsy
- Endocervical curettage (ECC)
- Endometrial biopsy
- Imaging examination may be needed

Important note:
Please contact your gynecologist immediately for comprehensive assessment!
```

#### 3. Update screening records

**TCT data structure:**
```json
{
  "cervical_cancer": {
    "last_tct": "2025-01-15",
    "tct_result": "ASC-US",
    "tct_result_full": "Atypical squamous cells, undetermined significance",
    "tct_sample_adequacy": "satisfactory",
    "tct_details": "Mild cytological abnormality",
    "tct_bethesda_category": "ASC-US"
  }
}
```

#### 4. Output confirmation

```
TCT test record updated

TCT test information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test date: January 15, 2025
TCT result: ASC-US
Details: Atypical squamous cells, undetermined significance

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
CIN 2+ risk: approximately 5-10%

Management recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
HPV testing recommended:
- HPV negative: recheck in 3 years
- HPV positive: colposcopy

Next examination:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Please consult your doctor about whether HPV testing is needed

Important note:
Most ASC-US cases return to normal,
but follow-up assessment per doctor's instructions is required.
```

---

### 3. Combined Screening - `co-testing`

Record HPV+TCT combined screening results.

**Parameter description:**
- `info`: Combined screening result (required)
  - HPV result: negative, positive, type
  - TCT result: NILM, ASC-US, LSIL, HSIL, etc.

**Examples:**
```
/screening co-testing negative NILM
/screening co-testing hpv-positive tct-normal
/screening co-testing positive16 ASC-US
/screening co-testing HPV-negative LSIL
```

**Execution steps:**

#### 1. Parse combined screening results

**Extract HPV and TCT results**

#### 2. Comprehensive risk assessment

**Combined screening result management algorithm:**

| HPV | TCT | Risk | Management |
|-----|-----|------|-----------|
| Negative | NILM | Very low | Recheck in 5 years |
| 16/18 positive | Any TCT | High | Immediate colposcopy |
| Other positive | NILM | Low-moderate | Recheck in 1 year |
| Other positive | ASC-US | Moderate | Colposcopy or recheck in 1 year |
| Other positive | LSIL/HSIL | High | Immediate colposcopy |
| Negative | ASC-US | Low | Recheck in 3 years |
| Negative | LSIL | Low-moderate | Recheck in 1 year |
| Negative | HSIL | High | Colposcopy |
| Any | AGC | High | Comprehensive assessment |

**Result interpretation examples:**

**HPV negative + TCT NILM:**
```
Combined screening result: HPV negative + TCT normal

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Cervical cancer risk: Very low

This is the most ideal result!

Screening interval:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Can extend to recheck in 5 years
(for women aged 30-65)

Protection period:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Cervical cancer risk <0.1% over the next 5 years
- Safer than TCT or HPV alone

Next screening:
━━━━━━━━━━━━━━━━━━━━━━━━━━
January 15, 2030

Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Keep up with regular screenings!
HPV vaccination can prevent other types.
```

**HPV 16/18 positive + TCT NILM:**
```
Combined screening result: HPV 16 positive + TCT normal

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Cervical cancer risk: High

Even with normal TCT, HPV 16/18 positive
still requires colposcopy!

Immediate action:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Immediate colposcopy

Reason:
━━━━━━━━━━━━━━━━━━━━━━━━━━
HPV 16/18 are the most carcinogenic high-risk types;
lesions can be present even with normal TCT.

Colposcopy can detect:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Lesions missed by TCT
- Early precancerous lesions
- Guide further management

Important note:
Please have a colposcopy immediately!
```

**HPV positive + TCT ASC-US:**
```
Combined screening result: HPV positive + TCT mildly abnormal

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Cervical cancer risk: Moderate-high

Management recommendation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Colposcopy

CIN 2+ risk: approximately 20-30%

Colposcopy assessment needed:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Determine degree of lesion
- Rule out more serious lesions
- Guide treatment

Important note:
Please schedule colposcopy!
```

#### 3. Update screening records

**Combined screening data structure:**
```json
{
  "cervical_cancer": {
    "last_hpv": "2025-01-15",
    "hpv_result": "negative",
    "hpv_type": null,

    "last_tct": "2025-01-15",
    "tct_result": "NILM",
    "tct_details": "Negative, no intraepithelial lesion or malignancy",

    "last_co_testing": "2025-01-15",
    "co_testing_result": "negative_NILM",
    "co_testing_interpretation": "Very low risk",

    "screening_strategy": "co-testing",
    "screening_interval": "5_years",
    "age_appropriate_interval": true,

    "next_screening": "2030-01-15",
    "next_screening_type": "co_testing",
    "days_until_next": 1825
  }
}
```

#### 4. Output confirmation

```
Combined screening record updated

Combined screening information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test date: January 15, 2025
HPV result: Negative
TCT result: NILM (normal)

Comprehensive assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Cervical cancer risk: Very low

Screening strategy:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Combined screening (HPV+TCT)
Screening interval: 5 years

Next screening:
━━━━━━━━━━━━━━━━━━━━━━━━━━
January 15, 2030

Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Most ideal result! Keep it up!
```

---

### 4. Record Tumor Markers - `marker`

Record gynecological tumor marker test results.

**Parameter description:**
- `info`: Tumor marker information (required)
  - Marker type: CA125, CA19-9, CEA, AFP
  - Value: number

**Examples:**
```
/screening marker ca125 15.5
/screening marker CA19-9 22.0
/screening marker cea 3.2
/screening marker afp 5.5
/screening marker ca125 80
```

**Execution steps:**

#### 1. Parse tumor marker information

**Marker identification:**
| Marker | Related cancers | Normal value |
|--------|----------------|--------------|
| CA125 | Ovarian cancer, endometrial cancer | <35 U/mL |
| CA19-9 | Ovarian cancer, endometrial cancer, pancreatic cancer | <37 U/mL |
| CEA | Endometrial cancer, colorectal cancer | <5 ng/mL (non-smokers), <10 ng/mL (smokers) |
| AFP | Yolk sac tumor | <10 ng/mL |

#### 2. Result classification

**CA125 classification:**

| Value | Classification | Significance |
|-------|---------------|-------------|
| <35 | Normal | No obvious abnormality |
| 35-65 | Mildly elevated | Need to combine with clinical findings |
| 65-100 | Significantly elevated | Requires assessment |
| >100 | Markedly elevated | High vigilance required |

**CA19-9 classification:**

| Value | Classification | Significance |
|-------|---------------|-------------|
| <37 | Normal | No obvious abnormality |
| 37-74 | Mildly elevated | Need to combine with clinical findings |
| 74-100 | Significantly elevated | Requires assessment |
| >100 | Markedly elevated | High vigilance required |

#### 3. Trend analysis

**Calculate change:**
```javascript
if (previous_value) {
  absolute_change = current_value - previous_value
  percentage_change = (absolute_change / previous_value) * 100

  if (percentage_change > 20) trend = "rising"
  else if (percentage_change < -20) trend = "falling"
  else trend = "stable"
}
```

**Risk assessment:**
```javascript
risk = "low"
if (value > 2 * upper_limit) risk = "high"
else if (value > upper_limit) risk = "moderate"
else if (trend === "rising" && previous_elevated) risk = "moderate"

if (trend === "rising" && percentage_change > 50) risk = "high"
```

#### 4. Update tumor marker records

**Tumor marker data structure:**
```json
{
  "tumor_markers": {
    "CA125": {
      "current_value": 15.5,
      "reference_range": "<35",
      "unit": "U/mL",
      "last_checked": "2025-06-20",
      "classification": "normal",
      "trend": "stable",
      "trend_direction": "stable",
      "percentage_change": -14.8,
      "history": [
        {
          "date": "2024-06-20",
          "value": 18.2
        },
        {
          "date": "2024-12-20",
          "value": 16.5
        },
        {
          "date": "2025-06-20",
          "value": 15.5
        }
      ],
      "interpretation": "",
      "notes": ""
    },

    "CA19-9": {
      "current_value": 22.0,
      "reference_range": "<37",
      "unit": "U/mL",
      "last_checked": "2025-06-20",
      "classification": "normal",
      "trend": "stable",
      "history": [
        {
          "date": "2024-06-20",
          "value": 23.5
        },
        {
          "date": "2025-06-20",
          "value": 22.0
        }
      ]
    },

    "CEA": {
      "current_value": null,
      "reference_range": "<5",
      "unit": "ng/mL",
      "last_checked": null,
      "classification": null,
      "history": []
    },

    "AFP": {
      "current_value": null,
      "reference_range": "<10",
      "unit": "ng/mL",
      "last_checked": null,
      "classification": null,
      "history": []
    }
  }
}
```

#### 5. Output confirmation

**Normal value output:**
```
Tumor marker record updated

CA125 test information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test date: June 20, 2025
CA125: 15.5 U/mL
Reference range: <35 U/mL
Classification: Normal

Trend analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
History:
- 2024-06-20: 18.2 U/mL
- 2024-12-20: 16.5 U/mL
- 2025-06-20: 15.5 U/mL

Trend: Steadily declining
Change: -14.8% (within 6 months)

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
CA125 is within normal range,
trend is stable, no abnormal signs.

Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
A normal CA125 value does not mean 100% no risk,
but current test results are reassuring.

Keep up with regular screenings!
```

**Elevated value output:**
```
Tumor marker record updated

CA125 test information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test date: June 20, 2025
CA125: 80 U/mL
Reference range: <35 U/mL
Classification: Significantly elevated

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current risk: High

Trend analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
History:
- 2024-06-20: 18.2 U/mL
- 2024-12-20: 35.0 U/mL
- 2025-06-20: 80.0 U/mL

Trend: Rapidly rising
Change: +128% (within 6 months)

Possible causes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Non-cancer causes of elevated CA125:
- Benign gynecological conditions
  - Endometriosis
  - Uterine fibroids
  - Pelvic inflammatory disease
  - Menstrual period (mild elevation)
- Benign non-gynecological conditions
  - Liver cirrhosis
  - Heart failure
  - Kidney disease
- Physiological causes
  - Pregnancy
  - Menstruation
  - Ovulation

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Consult a gynecologist immediately

Further examinations may include:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Transvaginal ultrasound
- Pelvic MRI
- CT scan
- Other markers such as CA19-9, CEA
- Clinical assessment

Important note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Elevated CA125 does not equal cancer

But professional assessment is needed to rule out other causes.
Please seek medical attention promptly!
```

---

### 5. Record Abnormal Result Follow-up - `abnormal`

Record follow-up on abnormal results.

**Parameter description:**
- `info`: Abnormal result follow-up information (required)
  - Type: asc-us, lsil, hsil, agc, etc.
  - Follow-up method: colposcopy, biopsy, repeat
  - Result: normal, CIN1, CIN2, CIN3, cancer, etc.

**Examples:**
```
/screening abnormal asc-us colposcopy scheduled 2025-02-01
/screening abnormal lsil repeat 2025-06-20
/screening abnormal hsil biopsy CIN2
/screening abnormal colposcopy normal
```

**Execution steps:**

#### 1. Parse follow-up information

#### 2. Update abnormal result records

**Abnormal result data structure:**
```json
{
  "abnormal_result_followup": [
    {
      "result_id": "abn_20250115",
      "initial_result": {
        "type": "hpv_positive",
        "hpv_type": "16",
        "date_identified": "2025-01-15",
        "tct_result": null
      },
      "follow_up": {
        "type": "colposcopy",
        "scheduled_date": "2025-02-01",
        "completed_date": "2025-02-01",
        "result": "normal",
        "biopsy_result": null,
        "notes": "Colposcopy showed no abnormality"
      },
      "status": "resolved",
      "resolved_date": "2025-02-01",
      "next_follow_up": "2025-08-01"
    },
    {
      "result_id": "abn_20250201",
      "initial_result": {
        "type": "tct_abnormal",
        "tct_result": "HSIL",
        "hpv_result": "positive",
        "hpv_type": "52",
        "date_identified": "2025-02-01"
      },
      "follow_up": {
        "type": "colposcopy_biopsy",
        "scheduled_date": "2025-02-15",
        "completed_date": "2025-02-15",
        "result": "CIN2",
        "biopsy_result": "CIN2",
        "treatment": "LEEP",
        "treatment_date": "2025-03-01"
      },
      "status": "treated",
      "resolved_date": null,
      "next_follow_up": "2025-08-01"
    }
  ]
}
```

#### 3. Output confirmation

```
Abnormal result follow-up record updated

Abnormal result information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Initial result: HPV 16 positive
Date identified: January 15, 2025

Follow-up information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Follow-up method: Colposcopy
Completed date: February 1, 2025
Result: Normal

Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Resolved

Next follow-up:
━━━━━━━━━━━━━━━━━━━━━━━━━━
August 1, 2025 (6 months later)
Recheck HPV+TCT

Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Normal colposcopy is good news!
But regular follow-up per doctor's instructions is still needed
to confirm HPV has cleared or lesion has stabilized.
```

---

### 6. View Screening Status - `status`

Display current screening status.

**Parameter description:**
- No parameters

**Example:**
```
/screening status
```

**Execution steps:**

#### 1. Read screening data

#### 2. Generate status report

```
Gynecological Cancer Screening Status

Cervical cancer screening:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Screening strategy: Combined screening (HPV+TCT)

Recent examinations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
HPV test (January 15, 2025)
Result: Negative

TCT test (January 15, 2025)
Result: NILM (normal)

Comprehensive assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Cervical cancer risk: Very low

Next screening:
━━━━━━━━━━━━━━━━━━━━━━━━━━
January 15, 2030
1825 days remaining (5 years)

Screening history:
━━━━━━━━━━━━━━━━━━━━━━━━━━
First screening: January 15, 2010
Number of screenings: 5
Years of screening: 15

Abnormal result records:
━━━━━━━━━━━━━━━━━━━━━━━━━━
No abnormal records

Tumor markers:
━━━━━━━━━━━━━━━━━━━━━━━━━━
CA125: 15.5 U/mL (normal)
  Trend: Stable
  Last tested: June 20, 2025

CA19-9: 22.0 U/mL (normal)
  Trend: Stable
  Last tested: June 20, 2025

CEA: Not tested
AFP: Not tested

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Cervical cancer screening on track
- Consider adding CEA, AFP tests
- Continue regular examinations

Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Cervical cancer screening is very regular and results are normal.
Keep it up!
```

---

### 7. Next Screening Reminder - `next`

Display next screening information.

**Parameter description:**
- No parameters

**Example:**
```
/screening next
```

**Execution steps:**

#### 1. Find next screening

#### 2. Generate reminder

```
Next Screening Reminder

Next screening information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Examination type: Combined screening (HPV+TCT)
Scheduled date: January 15, 2030 (Monday)
1825 days remaining (5 years)

Examination items:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- HPV test (high-risk types)
- TCT (Liquid-Based Cytology)

Examination description:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Combined screening is currently the most effective cervical cancer
screening method; it can:
- Detect precancerous lesions early
- Detect cervical cancer early
- Extend screening interval to 5 years

Preparation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Avoid menstrual period (best 3-7 days after period ends)
- Avoid sexual intercourse 24-48 hours before examination
- Avoid vaginal douching 24-48 hours before examination
- Avoid vaginal medications 24-48 hours before examination
- Wear loose clothing for easier examination

Examination process:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Gynecological examination
2. Cervical cell sampling (TCT)
3. HPV sampling (can be done simultaneously with TCT)

Procedure time: approximately 5-10 minutes
Pain level: mild discomfort

Common questions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Q: Do I need to fast?
A: No fasting needed.

Q: Will it be painful?
A: There may be mild discomfort, but it is usually tolerable.

Q: Can I resume normal activities after the examination?
A: Yes, no special restrictions.

Q: When will the results be available?
A: Usually 1-2 weeks.

Suggested questions for your doctor:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Are this year's screening results normal?
- When is the next screening?
- Are any additional tests needed?
- HPV vaccination recommendations?

Location:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Hospital: [Hospital name]
Department: Gynecology outpatient clinic
Address: [Address]
Phone: [Phone number]

Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
It is recommended to schedule 1-2 weeks in advance
to avoid waiting in line.
```

---

## Data Structure

### Main file: data/screening-tracker.json

```json
{
  "created_at": "2025-12-31T12:00:00.000Z",
  "last_updated": "2025-12-31T12:00:00.000Z",

  "cancer_screening": {
    "screening_id": "screening_20250101",

    "cervical_cancer": {
      "last_hpv": "2025-01-15",
      "hpv_result": "negative",
      "hpv_type": null,
      "hpv_risk_level": null,
      "hpv_method": "PCR",
      "hpv_high_risk_types": [],
      "hpv_all_types": [],

      "last_tct": "2025-01-15",
      "tct_result": "NILM",
      "tct_result_full": "Negative, no intraepithelial lesion or malignancy",
      "tct_sample_adequacy": "satisfactory",
      "tct_details": "Negative",
      "tct_bethesda_category": "NILM",

      "last_co_testing": "2025-01-15",
      "co_testing_result": "negative_NILM",
      "co_testing_interpretation": "Very low risk",

      "screening_strategy": "co-testing",
      "screening_interval": "5_years",
      "age_appropriate_interval": true,

      "next_screening": "2030-01-15",
      "next_screening_type": "co-testing",
      "days_until_next": 1825,

      "abnormal_results": [],

      "total_screenings": 5,
      "first_screening": "2010-01-15",
      "screening_history": []
    },

    "tumor_markers": {
      "CA125": {
        "current_value": 15.5,
        "reference_range": "<35",
        "unit": "U/mL",
        "last_checked": "2025-06-20",
        "classification": "normal",
        "trend": "stable",
        "trend_direction": "stable",
        "percentage_change": -14.8,
        "history": [
          {
            "date": "2024-06-20",
            "value": 18.2
          },
          {
            "date": "2024-12-20",
            "value": 16.5
          },
          {
            "date": "2025-06-20",
            "value": 15.5
          }
        ],
        "interpretation": "",
        "notes": ""
      },

      "CA19-9": {
        "current_value": 22.0,
        "reference_range": "<37",
        "unit": "U/mL",
        "last_checked": "2025-06-20",
        "classification": "normal",
        "trend": "stable",
        "history": [
          {
            "date": "2024-06-20",
            "value": 23.5
          },
          {
            "date": "2025-06-20",
            "value": 22.0
          }
        ]
      },

      "CEA": {
        "current_value": null,
        "reference_range": "<5",
        "unit": "ng/mL",
        "last_checked": null,
        "classification": null,
        "history": []
      },

      "AFP": {
        "current_value": null,
        "reference_range": "<10",
        "unit": "ng/mL",
        "last_checked": null,
        "classification": null,
        "history": []
      }
    },

    "abnormal_result_followup": [],

    "upcoming_appointments": [
      {
        "appointment_id": "appt_001",
        "type": "annual_gyn_exam",
        "date": "2026-01-15",
        "purpose": "annual_gynecological_exam",
        "preparation": [],
        "location": "",
        "notes": ""
      }
    ],

    "metadata": {
      "created_at": "2025-01-01T00:00:00.000Z",
      "last_updated": "2025-06-20T00:00:00.000Z"
    }
  },

  "statistics": {
    "total_cervical_screenings": 5,
    "years_of_screening": 15,
    "abnormal_results_count": 0,
    "colposcopies": 0,
    "tumor_marker_tests": 3,
    "all_markers_normal": true,
    "screening_uptodate": true,
    "next_screening_due": "2030-01-15"
  },

  "settings": {
    "screening_strategy": "co-testing",
    "reminder_days_before": 30,
    "age": 45,
    "screening_age_started": 30,
    "family_history_cancer": []
  }
}
```

### Detailed record file: data/screening-records/YYYY-MM/YYYY-MM-DD_screening-record.json

```json
{
  "screening_id": "screening_20250115",
  "record_date": "2025-01-15",
  "screening_type": "co-testing",

  "hpv_result": {
    "result": "negative",
    "type": null,
    "method": "PCR",
    "lab": "",
    "notes": ""
  },

  "tct_result": {
    "result": "NILM",
    "full_result": "Negative, no intraepithelial lesion or malignancy",
    "sample_adequacy": "satisfactory",
    "bethesda_category": "NILM",
    "pathologist": "",
    "notes": ""
  },

  "combined_interpretation": "Very low risk",
  "management_plan": "Recheck in 5 years",

  "metadata": {
    "created_at": "2025-01-15T14:30:00.000Z",
    "last_updated": "2025-01-15T14:30:00.000Z"
  }
}
```

---

## Intelligent Recognition Rules

### HPV result recognition

| User input | Standard result |
|-----------|----------------|
| negative | negative |
| positive | positive |
| 16, 18, 31, 33, 52, 58 | HPV type |

### TCT result recognition

| User input | Standard result |
|-----------|----------------|
| NILM, negative, normal | NILM |
| ASC-US, atypical squamous cells | ASC-US |
| ASC-H, atypical cannot exclude HSIL | ASC-H |
| LSIL, low-grade lesion, CIN1 | LSIL |
| HSIL, high-grade lesion, CIN2, CIN3 | HSIL |
| AGC, atypical glandular cells | AGC |

### Tumor marker recognition

| Keyword | Marker |
|---------|--------|
| ca125, CA125 | CA125 |
| ca19-9, CA19-9 | CA19-9 |
| cea, CEA | CEA |
| afp, AFP | AFP |

### Value recognition

| Format | Example |
|--------|---------|
| Number | 15.5, 80 |
| Number + unit | 15.5 U/mL, 22.0 U/mL |

---

## Error Handling

| Scenario | Error message | Recommendation |
|----------|--------------|----------------|
| No screening records | No screening records. Please use /screening hpv or /screening tct first | Guide user to start recording |
| HPV format error | HPV result format error. Correct format: /screening hpv negative | Provide correct format |
| TCT result not recognized | Unrecognized TCT result. Supported: NILM, ASC-US, LSIL, HSIL, etc. | List supported types |
| Marker not recognized | Unrecognized tumor marker. Supported: CA125, CA19-9, CEA, AFP | List supported types |
| Value format error | Value format error. Correct format: /screening marker ca125 15.5 | Provide correct format |

---

## Notes

- Elevated tumor markers do not equal cancer
- Screening intervals should follow doctor's instructions
- Abnormal results require prompt medical attention
- HPV positive does not equal cervical cancer
- Abnormal TCT does not equal cervical cancer
- Most HPV infections clear naturally
- Precancerous lesions can be treated and prevented

**Situations requiring immediate medical attention:**
- HPV 16/18 positive
- HSIL (high-grade lesion)
- AGC (atypical glandular cells)
- Tumor markers significantly elevated (>3 times normal value)
- Tumor markers rapidly rising (>50% change)

---

## Example Usage

```
# Record HPV test
/screening hpv negative

# Record TCT test
/screening tct NILM

# Combined screening
/screening co-testing negative NILM

# Record tumor markers
/screening marker ca125 15.5
/screening marker ca19-9 22.0

# Abnormal result follow-up
/screening abnormal colposcopy scheduled 2025-02-01

# View status
/screening status

# Next screening
/screening next
```
