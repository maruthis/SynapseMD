---
description: Cognitive function assessment command - Record MMSE/MoCA tests, cognitive domain assessments, and daily function assessments
arguments:
  - name: action
    description: Action type (mmse, moca, domain, adl, iadl, status, trend, risk)
    required: true
  - name: info
    description: Specific information (test scores, cognitive domain status, functional assessment, etc.)
    required: false
---

# Cognitive Function Assessment Command (Cognitive Assessment)

## Feature Overview

Used to manage cognitive function assessments for elderly individuals, including MMSE, MoCA tests, cognitive domain assessments, and daily function assessments.

---

## ⚠️ Safety Red Lines

1. **No diagnosis of cognitive impairment or dementia**
   - Does not diagnose Alzheimer's disease or other forms of dementia
   - Diagnosis requires a neurologist or geriatrician

2. **Not a replacement for professional neurological/geriatric assessments**
   - The system is for screening and tracking only
   - Abnormal results require medical confirmation

3. **No specific medication treatment plans**
   - Does not recommend cholinesterase inhibitors or other medications
   - Medications require a doctor's prescription

---

## ✅ What the system can do

- Cognitive function screening (MMSE/MoCA)
- Tracking cognitive decline trends
- Daily living function assessment (ADL/IADL)
- Cognitive domain function assessment
- Risk alerts and medical consultation recommendations

---

## Available Operations

### 1. MMSE Test - `mmse`

Record Mini-Mental State Examination (MMSE) results.

**Parameter Description:**
- `info`: MMSE test results (required)
  - Total score (0-30 points)
  - Sub-scores (optional)
- `date`: Test date (optional, defaults to today)

**Execution Steps:**
#### 1. Parameter identification
- Extract MMSE total score from info
- Recognize format: `mmse[:\s]+(\d+)` or `score[:\s]+(\d+)`
- Extract sub-scores if available

#### 2. Result interpretation
- 27-30 points: Normal
- 21-26 points: Mild cognitive impairment
- 10-20 points: Moderate cognitive impairment
- ≤9 points: Severe cognitive impairment

#### 3. Record update
- Update `data/cognitive-assessment.json`
- Record test date, total score, sub-scores
- Calculate trends and annual decline rate
- Update statistics

#### 4. Output confirmation
- Display current test results
- Display historical comparison (if available)
- Display next assessment date (12 months later)

**Examples:**
```
/cognitive mmse score 27
/cognitive mmse 24 orientation 9 memory 6
```

---

### 2. MoCA Test - `moca`

Record Montreal Cognitive Assessment (MoCA) results.

**Parameter Description:**
- `info`: MoCA test results (required)
  - Total score (0-30 points)
  - Education level (optional, used for score adjustment)
- `date`: Test date (optional, defaults to today)

**Execution Steps:**
#### 1. Parameter identification
- Extract MoCA total score from info
- Recognize format: `moca[:\s]+(\d+)` or `score[:\s]+(\d+)`
- Extract education level (optional)

#### 2. Result interpretation
- ≥26 points: Normal
- 18-25 points: Mild cognitive impairment
- 10-17 points: Moderate cognitive impairment
- <10 points: Severe cognitive impairment
- Education level adjustment: Add 1 point for ≤12 years of education

#### 3. Record update
- Update `data/cognitive-assessment.json`
- Record test date, total score, adjusted score
- Update statistics

#### 4. Output confirmation
- Display current test results
- Display education level adjustment
- Display next assessment date

**Examples:**
```
/cognitive moca score 24
/cognitive moca 25 education 12years
```

---

### 3. Cognitive Domain Assessment - `domain`

Record the functional status of specific cognitive domains.

**Parameter Description:**
- `info`: Cognitive domain assessment results (required)
  - Cognitive domain name (memory/executive/language/visuospatial)
  - Functional status (normal/mild_impairment/moderate_impairment/severe_impairment)
- `date`: Assessment date (optional, defaults to today)

**Assessable cognitive domains:**
- `memory` - Memory (immediate memory, short-term memory, long-term memory)
- `executive` - Executive function (planning, problem solving, abstract thinking)
- `language` - Language ability (comprehension, expression, naming)
- `visuospatial` - Visuospatial ability (object recognition, spatial orientation)

**Execution Steps:**
#### 1. Parameter identification
- Extract cognitive domain name from info
- Recognize format: `(memory|executive|language|visuospatial)[:\s]+(\w+)`
- Identify functional status keywords

#### 2. Record update
- Update `cognitive_domains` section
- Record the status of the cognitive domain
- Update impaired_domains count

#### 3. Output confirmation
- Display assessment results for the cognitive domain
- Display all impaired cognitive domains

**Examples:**
```
/cognitive domain memory mild_impairment
/cognitive domain executive normal
/cognitive domain language mild_impairment
```

---

### 4. Activities of Daily Living Assessment - `adl`

Record Activities of Daily Living (ADL) functional status.

**Parameter Description:**
- `info`: ADL assessment results (required)
  - 6 basic activities (bathing/dressing/toileting/transferring/continence/feeding)
  - Functional status (independent/needs_assistance/dependent)
- `date`: Assessment date (optional, defaults to today)

**ADL 6 basic activities:**
- `bathing` - Bathing
- `dressing` - Dressing
- `toileting` - Toileting
- `transferring` - Transferring (from bed to chair)
- `continence` - Bowel and bladder control
- `feeding` - Feeding

**Execution Steps:**
#### 1. Parameter identification
- Extract ADL items and status from info
- Recognize format: `(bathing|dressing|toileting|transferring|continence|feeding)[:\s]+(\w+)`

#### 2. Record update
- Update `functional_impact.activities_of_daily_living` section
- Record the functional status of each activity

#### 3. Output confirmation
- Display ADL assessment results
- Display dependency score

**Examples:**
```
/cognitive adl independent
/cognitive adl bathing independent dressing needs_assistance
```

---

### 5. Instrumental Activities of Daily Living Assessment - `iadl`

Record Instrumental Activities of Daily Living (IADL) functional status.

**Parameter Description:**
- `info`: IADL assessment results (required)
  - 8 instrumental activities (shopping/cooking/managing_medications/using_telephone/managing_finances, etc.)
  - Functional status (independent/needs_assistance/supervision_needed/dependent)
- `date`: Assessment date (optional, defaults to today)

**IADL 8 instrumental activities:**
- `shopping` - Shopping
- `cooking` - Cooking
- `managing_medications` - Managing medications
- `using_telephone` - Using the telephone
- `managing_finances` - Managing finances
- `housekeeping` - Housekeeping
- `transportation` - Transportation
- `laundry` - Laundry

**Execution Steps:**
#### 1. Parameter identification
- Extract IADL items and status from info
- Recognize format: `(shopping|cooking|managing_medications|using_telephone|managing_finances|housekeeping|transportation|laundry)[:\s]+(\w+)`

#### 2. Record update
- Update `functional_impact.instrumental_activities` section
- Record the functional status of each activity

#### 3. Output confirmation
- Display IADL assessment results
- Display items requiring assistance

**Examples:**
```
/cognitive iadl shopping needs_assistance
/cognitive iadl managing_medications supervision_needed
```

---

### 6. View Cognitive Status - `status`

View the current cognitive function assessment status.

**Execution Steps:**
#### 1. Read data
- Read `data/cognitive-assessment.json`

#### 2. Display status report
- Most recent MMSE/MoCA results
- Status of each cognitive domain
- ADL/IADL functional status
- Statistics

**Examples:**
```
/cognitive status
```

---

### 7. View Change Trends - `trend`

View cognitive function change trends.

**Execution Steps:**
#### 1. Read historical data
- Extract MMSE/MoCA historical records

#### 2. Trend analysis
- Calculate annual decline rate
- Identify rate of decline (stable/slow_decline/rapid_decline)

#### 3. Display trend report
- Comparison of historical test results
- Decline trend chart
- Risk alerts

**Examples:**
```
/cognitive trend
```

---

### 8. Cognitive Function Risk Assessment - `risk`

Comprehensively assess the risk of cognitive function decline.

**Execution Steps:**
#### 1. Risk factor identification
- Age factor (>75 years is high risk)
- Education level (≤12 years increases risk)
- Vascular risk factors (hypertension, diabetes, etc.)
- MMSE/MoCA scores
- Cognitive domain impairment status
- ADL/IADL functional status

#### 2. Risk classification
- Low risk
- Moderate risk
- High risk

#### 3. Display risk assessment
- Current risk level
- Main risk factors
- Recommended measures
- Medical consultation advice

**Examples:**
```
/cognitive risk
```

---

## Notes

### Test Standardization
- MMSE/MoCA should be conducted in a standardized environment
- Consider the effects of education level and cultural background
- Test administrators should be professionally trained

### Result Interpretation
- A single abnormal test does not equal cognitive impairment
- Must be evaluated in conjunction with daily function assessment
- Trends are more important than a single score

### Medical Consultation Advice
Seek medical attention in the following situations:
- MMSE ≤ 26 points
- MoCA ≤ 25 points
- Multiple cognitive domains impaired
- Decline in ADL/IADL function
- Rapid cognitive decline

---

## Reference Resources

- MMSE: Folstein et al. (1975)
- MoCA: Nasreddine et al. (2005)
- NIA-AA Dementia Diagnostic Criteria
- Chinese Dementia Diagnosis and Treatment Guidelines
