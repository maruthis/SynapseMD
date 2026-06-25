---
description: Male reproductive health and semen analysis records
arguments:
  - name: action
    description: "Action type: semen (semen analysis) / hormone (hormones) / varicocele (varicocele) / infection (infection) / status (status) / diagnosis (diagnosis)"
    required: true
  - name: info
    description: Reproductive health information (semen analysis results, hormone levels, examination results, etc., in natural language)
    required: false
---

# Male Infertility Management

Male reproductive health tracking and management, including semen analysis records, hormone level monitoring, and infertility factor assessment.

## Action Types

### 1. Record Semen Analysis - `semen`

Record semen analysis results, WHO 2021 standards.

**Parameter Description:**
- `info`: Semen analysis information (required)
  - Parameter types: volume / concentration / motility / morphology / ph / liquefaction
  - Values: provide corresponding values based on parameter type
  - Sperm motility: pr (progressive motility), np (non-progressive motility)

**Examples:**
```
/fertility semen volume 2.5
/fertility semen concentration 45
/fertility semen motility pr 35 np 20
/fertility semen morphology 4
/fertility semen ph 7.5
/fertility semen complete    # Complete record
```

**Execution Steps:**

#### 1. Semen Analysis Standards (WHO 2021)

**Semen Volume:**
- Normal: ≥ 1.5 mL
- Abnormal: < 1.5 mL (hypospermia)
- Absent: 0 mL

**Sperm Concentration:**
- Normal: ≥ 15 × 10⁶/mL
- Oligozoospermia: < 15 × 10⁶/mL
- Azoospermia: 0 × 10⁶/mL

**Total Sperm Count:**
- Normal: ≥ 39 × 10⁶/ejaculate

**Sperm Motility:**
- PR (progressive motility): ≥ 32%
- NP (non-progressive motility): ≥ 40%
- Asthenozoospermia: PR < 32%

**Sperm Morphology:**
- Normal morphology rate: ≥ 4%
- Teratozoospermia: < 4%

**Semen pH:**
- Normal: 7.2-8.0
- Abnormal: < 7.2 or > 8.0

**Liquefaction Time:**
- Normal: ≤ 60 minutes

#### 2. Parse Semen Analysis Information

**Parameter Recognition:**
```javascript
// Semen volume
volume_patterns = [
  /volume[:\s]+(\d+\.?\d*)/i,
  /semen_volume[:\s]+(\d+\.?\d*)/i,
  /(\d+\.?\d*)\s*ml/i
]

// Sperm concentration
concentration_patterns = [
  /concentration[:\s]+(\d+)/i,
  /density[:\s]+(\d+)/i,
  /(\d+)\s*10.*6.*ml/i
]

// Motility
motility_patterns = [
  /pr[:\s]+(\d+)/i,
  /progressive[:\s]+(\d+)/i,
  /np[:\s]+(\d+)/i
]

// Morphology
morphology_patterns = [
  /morphology[:\s]+(\d+)/i,
  /normal_forms[:\s]+(\d+)/i
]
```

#### 3. Diagnostic Assessment

**Semen Analysis Result Classification:**

| Result | Diagnosis |
|------|------|
| All parameters normal | Normospermia |
| Sperm concentration <15 | Oligozoospermia |
| Sperm concentration = 0 | Azoospermia |
| PR < 32% | Asthenozoospermia |
| Normal morphology < 4% | Teratozoospermia |
| Semen volume < 1.5 mL | Hypospermia |
| Multiple abnormalities | Mixed abnormality |

#### 4. Update Semen Analysis Records

**Semen Analysis Data Structure:**
```json
{
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
  }
}
```

#### 5. Output Confirmation

**Normal Semen Analysis:**
```
✅ Semen Analysis Recorded

Semen Analysis Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Date: June 20, 2025
Abstinence Period: 3 days ✓

Semen Parameters:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Semen Volume: 2.5 mL ✓ (Reference: ≥1.5)
Sperm Concentration: 45 × 10⁶/mL ✓ (Reference: ≥15)
Total Sperm Count: 112.5 × 10⁶ ✓ (Reference: ≥39)

Sperm Motility:
  PR (Progressive): 35% ✓ (Reference: ≥32)
  NP (Non-progressive): 20% ✓ (Reference: ≥40)
  Total Motility: 55% ✓

Sperm Morphology: 4% ✓ (Reference: ≥4)
Semen pH: 7.5 ✓ (Reference: 7.2-8.0)
Liquefaction Time: 30 minutes ✓ (Reference: ≤60)

Diagnosis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Normospermia ✅

All parameters are within normal range.

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sufficient sperm count
✅ Normal sperm motility
✅ Normal sperm morphology
✅ Good semen quality

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue attempting natural conception
✅ Maintain healthy lifestyle
✅ Avoid high-temperature environments (sauna, hot baths)
✅ Quit smoking and limit alcohol
✅ Balanced diet
✅ Regular exercise

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This semen analysis is normal.

Semen quality can fluctuate;
recommend follow-up in 2-3 months to confirm.

If partner is unable to conceive within 6-12 months,
further evaluation is recommended.

Data saved to: data/fertility-records/2025-06/2025-06-20_semen-analysis.json
```

**Abnormal Semen Analysis Warning:**
```
⚠️ Semen Analysis Abnormality Notice

Semen Analysis Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Date: June 20, 2025
Abstinence Period: 3 days

Semen Parameters:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Semen Volume: 1.2 mL ⚠️ (Reference: ≥1.5)
Sperm Concentration: 12 × 10⁶/mL ⚠️ (Reference: ≥15)
Total Sperm Count: 14.4 × 10⁶ ⚠️ (Reference: ≥39)

Sperm Motility:
  PR (Progressive): 25% ⚠️ (Reference: ≥32)
  NP (Non-progressive): 15% ⚠️ (Reference: ≥40)
  Total Motility: 40% ⚠️

Sperm Morphology: 3% ⚠️ (Reference: ≥4)
Semen pH: 7.3 ✓
Liquefaction Time: 45 minutes ✓

Diagnosis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Oligozoospermia + Asthenozoospermia + Teratozoospermia
⚠️ Abnormal semen quality

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Multiple parameters below normal values,
may affect fertility.

Possible Causes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Varicocele
• Endocrine abnormality
• Reproductive tract infection
• Immune factors
• Genetic factors
• Environmental factors
• Lifestyle factors

🏥 Recommended Medical Visit:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommend consulting urology or
andrology physician for further evaluation:

Further Tests:
• Varicocele ultrasound
• Hormone level testing
• Reproductive tract infection screening
• Genetic testing (if needed)

Lifestyle Adjustments:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Quit smoking (very important)
✅ Limit alcohol
✅ Avoid high-temperature environments
✅ Avoid tight underwear
✅ Balanced nutrition
✅ Regular exercise
✅ Adequate sleep
✅ Reduce stress

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Abnormal semen quality does not mean absolute infertility.

Mild abnormalities can be corrected through
lifestyle improvements and medical treatment.

Recommend follow-up in 2-3 months
and consult an andrologist.

Data saved
```

---

### 2. Record Hormone Levels - `hormone`

Record reproductive hormone test results.

**Parameter Description:**
- `info`: Hormone test results (required)
  - Hormone types: testosterone / lh (luteinizing hormone) / fsh (follicle-stimulating hormone) / prl (prolactin) / e2 (estradiol)
  - Values: numbers

**Examples:**
```
/fertility hormone testosterone 15.5
/fertility hormone lh 5.2
/fertility hormone fsh 8.1
/fertility hormone prl 12.5
/fertility hormone complete  # Complete hormone testing
```

**Execution Steps:**

#### 1. Hormone Reference Values

**Testosterone (T):**
- Total testosterone: 10-35 nmol/L
- Free testosterone: 0.22-0.65 nmol/L

**Luteinizing Hormone (LH):**
- Normal: 1.7-8.6 IU/L

**Follicle-Stimulating Hormone (FSH):**
- Normal: 1.5-12.4 IU/L

**Prolactin (PRL):**
- Normal: < 15 ng/mL (males)

**Estradiol (E2):**
- Normal: < 70 pg/mL (males)

#### 2. Parse Hormone Information

**Hormone Recognition:**
```javascript
hormones = {
  testosterone: {
    patterns: [/testosterone[:\s]+(\d+\.?\d*)/i],
    unit: "nmol/L",
    reference: "10-35"
  },
  lh: {
    patterns: [/\blh\b[:\s]+(\d+\.?\d*)/i, /luteinizing_hormone[:\s]+(\d+\.?\d*)/i],
    unit: "IU/L",
    reference: "1.7-8.6"
  },
  fsh: {
    patterns: [/\bfsh\b[:\s]+(\d+\.?\d*)/i, /follicle_stimulating[:\s]+(\d+\.?\d*)/i],
    unit: "IU/L",
    reference: "1.5-12.4"
  },
  prl: {
    patterns: [/prl[:\s]+(\d+\.?\d*)/i, /prolactin[:\s]+(\d+\.?\d*)/i],
    unit: "ng/mL",
    reference: "<15"
  },
  e2: {
    patterns: [/e2[:\s]+(\d+\.?\d*)/i, /estradiol[:\s]+(\d+\.?\d*)/i],
    unit: "pg/mL",
    reference: "<70"
  }
}
```

#### 3. Hormone Assessment

**Abnormal Patterns:**

**Primary Testicular Insufficiency:**
- Testosterone: Low
- LH: High
- FSH: High

**Secondary Testicular Insufficiency:**
- Testosterone: Low
- LH: Low or normal
- FSH: Low or normal

**Hyperprolactinemia:**
- Prolactin: >15 ng/mL
- Testosterone: May be reduced
- LH/FSH: May be reduced

#### 4. Update Hormone Records

**Hormone Data Structure:**
```json
{
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
  }
}
```

#### 5. Output Confirmation

```
✅ Hormone Testing Recorded

Hormone Test Report:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Date: June 15, 2025

Hormone Levels:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Testosterone (T): 15.5 nmol/L ✓ (Reference: 10-35)
LH: 5.2 IU/L ✓ (Reference: 1.7-8.6)
FSH: 8.1 IU/L ✓ (Reference: 1.5-12.4)
Prolactin (PRL): 12.5 ng/mL ✓ (Reference: <15)
Estradiol (E2): 35 pg/mL ✓ (Reference: <70)

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All hormone levels within normal range
✅ Hypothalamic-pituitary-testicular axis functioning normally
✅ No obvious endocrine abnormalities

Hormone-Sperm Relationship:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Normal hormone levels indicate:
• Normal testicular sperm production function
• Normal endocrine regulation
• Sperm quality issues may relate to local
  testicular factors

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Hormone levels normal
✅ Focus on sperm quality
✅ Consider varicocele examination
✅ Reproductive tract infection screening

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Normal hormones cannot rule out all causes of infertility.

Requires comprehensive assessment combining
semen analysis, physical examination, etc.

Data saved
```

---

### 3. Record Varicocele - `varicocele`

Record varicocele examination results.

**Parameter Description:**
- `info`: Varicocele information (required)
  - Presence: none / left / right / bilateral
  - Grade: I/II/III (optional)

**Examples:**
```
/fertility varicocele none
/fertility varicocele left grade II
/fertility varicocele bilateral
/fertility varicocele left grade_II
```

**Execution Steps:**

#### 1. Varicocele Grading

**Clinical Grading:**
- **Grade I**: Not palpable, visible on Valsalva maneuver
- **Grade II**: Palpable, worsens with Valsalva maneuver
- **Grade III**: Visually visible

#### 2. Update Records

**Varicocele Data Structure:**
```json
{
  "varicocele": {
    "present": true,
    "side": "left",
    "grade": "II",
    "confirmed_by": "ultrasound",
    "surgery": false,
    "surgery_date": null,
    "notes": ""
  }
}
```

#### 3. Output Confirmation

```
✅ Varicocele Recorded

Examination Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: Left
Grade: Grade II
Confirmed by: Ultrasound

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Left varicocele, Grade II

Varicocele Effects:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• May lead to reduced sperm quality
• One of the common causes of infertility
• Surgically treatable

⚠️ Recommended Medical Visit:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommend consulting urology for evaluation:

Treatment Options:
• Observation (mild)
• Surgical treatment (moderate to severe)
• Microsurgical varicocelectomy
• Interventional embolization

Surgical Indications:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Abnormal semen quality
• Reduced testicular volume
• Testicular pain
• Infertility for more than 2 years

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Varicocele is a treatable
cause of infertility.

Surgery can improve semen quality
and increase natural conception rates.

Data saved
```

---

### 4. Record Infection Testing - `infection`

Record reproductive tract infection test results.

**Parameter Description:**
- `info`: Infection test results (required)
  - Pathogens: chlamydia / gonorrhea / mycoplasma
  - Results: positive / negative

**Examples:**
```
/fertility infection chlamydia negative
/fertility infection gonorrhea negative
/fertility infection mycoplasma positive
```

**Execution Steps:**

#### 1. Common Pathogens

**Chlamydia trachomatis:**
- Can cause urethritis, prostatitis, epididymitis
- Affects sperm quality

**Neisseria gonorrhoeae:**
- Causes urethritis, epididymitis
- Affects sperm transport

**Mycoplasma/Ureaplasma:**
- May affect sperm motility
- Associated with infertility

#### 2. Update Infection Records

**Infection Data Structure:**
```json
{
  "infections": {
    "chlamydia": "negative",
    "gonorrhea": "negative",
    "mycoplasma": "not_tested",
    "ureaplasma": "not_tested",
    "date": "2025-06-10",
    "treated": false
  }
}
```

#### 3. Output Confirmation

```
✅ Infection Testing Recorded

Test Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Test Date: June 10, 2025

Chlamydia: Negative ✓
Gonorrhea: Negative ✓
Mycoplasma: Not tested
Ureaplasma: Not tested

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No evidence of common reproductive tract infection

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Infection screening negative
✅ Anti-infective treatment not needed

⚠️ Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Mycoplasma/Ureaplasma not tested;
if needed, recommend supplementary testing.

Data saved
```

---

### 5. View Status - `status`

Display reproductive health tracking status.

**Parameter Description:**
- No parameters

**Examples:**
```
/fertility status
```

**Execution Steps:**

#### 1. Read Reproductive Health Data

#### 2. Generate Status Report

```
📍 Male Reproductive Health Status

Basic Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Age: 35 years old
Infertility Type: Primary infertility
Partner's Age: 32 years old
Months Trying to Conceive: 18 months

Semen Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Most Recent Test: June 20, 2025

Semen Volume: 2.5 mL ✓
Sperm Concentration: 45 × 10⁶/mL ✓
Sperm Motility: PR 35% ✓
Sperm Morphology: 4% ✓

Diagnosis: Normospermia

Hormone Levels:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Testosterone: 15.5 nmol/L ✓
LH: 5.2 IU/L ✓
FSH: 8.1 IU/L ✓
Prolactin: 12.5 ng/mL ✓

Assessment: Hormone levels normal

Other Tests:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Varicocele: None ✓
Chlamydia: Negative ✓
Gonorrhea: Negative ✓

Comprehensive Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Normal semen analysis
✅ Normal hormone levels
✅ No obvious cause of infertility

Possible Factors:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Idiopathic infertility
• Partner factors (needs evaluation)
• Immune factors
• Genetic factors

Recommended Actions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue attempting natural conception
✅ Partner gynecology examination (if not done)
✅ Follow-up semen analysis in 2-3 months
✅ Consider chromosomal testing (if needed)
✅ Consider Y-chromosome microdeletion testing

💡 This Week's Focus:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Healthy lifestyle
• Avoid high-temperature environments
• Quit smoking and limit alcohol
• Regular sleep schedule

⚠️ Important Statement:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is for reproductive health tracking only and cannot replace professional medical advice.

Recommend consulting andrology or reproductive medicine center
for comprehensive evaluation and guidance.

Data saved
```

---

### 6. View Diagnosis - `diagnosis`

Display infertility diagnosis and assessment.

**Parameter Description:**
- No parameters

**Examples:**
```
/fertility diagnosis
```

**Execution Steps:**

#### 1. Infertility Classification

**Primary Infertility:**
- Has never fathered a child

**Secondary Infertility:**
- Has previously fathered a child, currently unable to

**Infertility Cause Classification:**
- Sperm factors
- Varicocele
- Endocrine abnormalities
- Reproductive tract infections
- Immune factors
- Genetic factors
- Idiopathic (unknown cause)

#### 2. Generate Diagnosis Report

```
📋 Male Infertility Diagnosis Report

Assessment Date: December 31, 2025

Infertility Type:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: Primary infertility
Months trying to conceive: 18 months

Semen Analysis Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Normal semen volume
✅ Normal sperm concentration
✅ Normal sperm motility
✅ Normal sperm morphology

Conclusion: Normal sperm analysis

Hormone Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Normal testosterone
✅ Normal LH
✅ Normal FSH
✅ Normal prolactin

Conclusion: Normal endocrine function

Other Tests:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No varicocele
✅ No reproductive tract infection

Comprehensive Diagnosis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Idiopathic Infertility

Diagnosis Explanation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Semen analysis and hormone levels are both normal,
no obvious cause of infertility found.

Idiopathic infertility accounts for approximately
30-40% of male infertility.

Possible Factors (Unconfirmed):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Elevated sperm DNA fragmentation index
• Oxidative stress
• Mitochondrial dysfunction
• Occult sperm quality defects
• Immune factors

Recommended Further Tests:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Sperm DNA fragmentation index test
📋 Anti-sperm antibody test
📋 Y-chromosome microdeletion test
📋 Chromosomal karyotype analysis
📋 Partner gynecology examination

Treatment Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue attempting natural conception
✅ Improve lifestyle
✅ Antioxidant therapy (if needed)
✅ Assisted reproductive technology (if needed)

Assisted Reproductive Technology Options:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Intrauterine insemination (IUI)
• In vitro fertilization (IVF)
• Intracytoplasmic sperm injection (ICSI)
• If persistent infertility, recommend consulting

Reproductive Medicine Center:

Prognosis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Idiopathic infertility prognosis:
• Natural conception is still possible
• Good success rate with assisted reproduction
• No impact on offspring health

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Infertility does not mean absolute inability to conceive.

Modern reproductive medicine technology can help
most infertile couples achieve conception.

Recommend consulting a reproductive medicine center
for an individualized treatment plan.

Data saved
```

---

## Data Structure

### Main File: data/fertility-tracker.json

```json
{
  "created_at": null,
  "last_updated": null,

  "fertility_assessment": {
    "user_id": null,
    "age": null,
    "infertility_type": null,
    "partner_age": null,
    "trying_to_conceive_months": null,

    "semen_analysis": {
      "date": null,
      "abstinence_period": null,
      "volume": {},
      "concentration": {},
      "total_count": {},
      "motility": {},
      "morphology": {},
      "ph": {},
      "liquefaction": {},
      "diagnosis": null
    },

    "hormones": {
      "date": null,
      "testosterone": {},
      "lh": {},
      "fsh": {},
      "prl": {},
      "e2": {}
    },

    "varicocele": {
      "present": null,
      "side": null,
      "grade": null,
      "surgery": null,
      "surgery_date": null
    },

    "infections": {
      "chlamydia": null,
      "gonorrhea": null,
      "mycoplasma": null,
      "date": null,
      "treated": null
    },

    "genetic_testing": {
      "karyotype": null,
      "y_chromosome_microdeletion": null,
      "cftr_mutation": null
    },

    "recommendations": []
  },

  "statistics": {
    "total_semen_analyses": 0,
    "last_analysis_date": null,
    "diagnosis": null,
    "tracking_duration_months": 0
  }
}
```

### Detailed Records: data/fertility-records/YYYY-MM/YYYY-MM-DD_semen-analysis.json

```json
{
  "record_id": "fertility_20250620_001",
  "record_type": "semen_analysis",
  "date": "2025-06-20",

  "semen_analysis": {
    "volume": 2.5,
    "concentration": 45,
    "motility_pr": 35,
    "motility_np": 20,
    "morphology": 4,
    "ph": 7.5,
    "liquefaction": 30
  },

  "diagnosis": "normospermia",

  "notes": "",
  "metadata": {
    "created_at": "2025-06-20T10:00:00.000Z"
  }
}
```

---

## Intelligent Recognition Rules

### Semen Parameter Recognition

| Parameter | Keywords | Extraction |
|------|--------|------|
| Semen volume | volume, ml, milliliter | Number + mL |
| Sperm concentration | concentration, density, 10⁶/mL | Number |
| Progressive motility | pr, progressive | Percentage |
| Morphology | morphology, normal_forms, % | Percentage |
| pH | ph, acidity | 7.0-8.0 |

### Hormone Recognition

| Hormone | Keywords | Unit |
|------|--------|------|
| Testosterone | testosterone, T | nmol/L |
| LH | LH, luteinizing_hormone | IU/L |
| FSH | FSH, follicle_stimulating | IU/L |
| Prolactin | PRL, prolactin | ng/mL |
| Estradiol | E2, estradiol | pg/mL |

---

## Error Handling

| Scenario | Error Message | Suggestion |
|------|---------|------|
| Sperm concentration = 0 | Azoospermia<br>Recommend further evaluation | Referral to andrology |
| Low testosterone | Significantly low testosterone<br>Recommend endocrinology evaluation | Check pituitary function |
| High prolactin | Hyperprolactinemia<br>Requires further evaluation | Check for pituitary tumor |

---

## Notes

- This system is for reproductive health tracking only and cannot replace professional medical diagnosis
- Semen analysis requires 2-3 confirmations
- Test after 3-7 days of abstinence
- Both partners should be evaluated simultaneously for infertility
- Idiopathic infertility still has the possibility of natural conception

**Situations Requiring Immediate Medical Attention:**
- Azoospermia
- Significantly abnormal hormones
- Grade III varicocele
- Positive reproductive tract infection

All data is stored locally only to ensure privacy.

---

## Example Usage

```
# Record semen analysis
/fertility semen volume 2.5
/fertility semen concentration 45
/fertility semen motility pr 35 np 20
/fertility semen morphology 4

# Record hormones
/fertility hormone testosterone 15.5
/fertility hormone lh 5.2

# Record examinations
/fertility varicocele none
/fertility infection chlamydia negative

# View status
/fertility status
/fertility diagnosis
```
