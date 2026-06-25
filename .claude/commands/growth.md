---
description: Child growth curve tracking and WHO standard assessment
arguments:
  - name: action
    description: "Action type: record (record measurement) / status (assessment) / percentile (percentile) / velocity (growth velocity) / check (abnormality check) / history (history)"
    required: true
  - name: info
    description: Measurement information (height/weight/head circumference, etc., in natural language)
    required: false
  - name: date
    description: "Measurement date (format: YYYY-MM-DD, default today)"
    required: false
---

# Growth Curve Tracking

Child growth monitoring and assessment based on WHO Child Growth Standards, providing percentile analysis and growth abnormality alerts.

## Action Types

### 1. Record Growth Data - `record`

Record child's height, weight, head circumference and other growth metrics.

**Parameter Description:**
- `info`: Measurement information (required)
  - Height: height 112.5, 112.5cm
  - Weight: weight 20.5, 20.5kg
  - Head circumference: head 48, 48cm (0-3 years)
- `date`: Measurement date (optional, defaults to today)

**Examples:**
```
/growth record 112.5cm 20.5kg
/growth record height 112.5 weight 20.5
/growth record head 48
/growth record height 110 weight 18.5 date 2025-06-15
```

**Execution Steps:**

#### 1. Parse Measurement Information

**Parameter Recognition:**
- Height: `height[:\s]+(\d+\.?\d*)` or `(\d+\.?\d*)\s*cm`
- Weight: `weight[:\s]+(\d+\.?\d*)` or `(\d+\.?\d*)\s*kg`
- Head circumference: `head[:\s]+(\d+\.?\d*)` or `(\d+\.?\d*)\s*cm`

#### 2. Read Child Basic Information

Read from `data/profile.json`:
- Date of birth
- Gender

If missing, prompt:
```
⚠️ Missing child basic information

Please set first:
/profile child-name Xiao Ming
/profile child-birth-date 2020-01-01
/profile child-gender male
```

#### 3. Calculate Age and Age in Months

```javascript
birthDate = profile.child_birth_date
measurementDate = date || today

ageMonths = (measurementDate - birthDate) / 30.44
ageYears = ageMonths / 12

// Premature infant correction (if needed)
if gestational_age < 37 weeks and age < 2 years:
  correctedAge = chronologicalAge - (40 - gestational_age)
```

#### 4. Calculate BMI

```javascript
if height && weight:
  bmi = weight / (height / 100)²
```

#### 5. Look Up WHO Percentiles

Look up from `data/who-growth-standards.json`:
- `height_for_age` → Height-for-age percentile
- `weight_for_age` → Weight-for-age percentile
- `bmi_for_age` → BMI-for-age percentile
- `head_circumference_for_age` → Head circumference-for-age percentile (0-3 years)

**Percentile Lookup Algorithm:**
```javascript
// 1. Select gender and measurement type
whoData = loadWHOStandards()[measurementType][gender]

// 2. Find percentile for age
ageKey = findNearestAge(whoData, ageMonths)
percentiles = whoData[ageKey]

// 3. Calculate percentile and Z-score
percentile = calculatePercentile(value, percentiles)
zScore = calculateZScore(value, percentiles)
```

#### 6. Calculate Z-score (Standard Deviation Units)

```javascript
zScore = (value - median) / standardDeviation

// Z-score classification:
// < -3: Severely below average
// -3 to -2: Notably below average
// -2 to -1: Mildly below average
// -1 to +1: Normal
// +1 to +2: Mildly above average
// +2 to +3: Notably above average
// > +3: Severely above average
```

#### 7. Calculate Growth Velocity (If Historical Data Available)

```javascript
if measurements.length >= 2:
  previous = measurements[measurements.length - 2]
  current = measurements[measurements.length - 1]

  monthsDiff = calculateMonthsDifference(previous.date, current.date)
  heightVelocity = (current.height - previous.height) / (monthsDiff / 12)
  weightVelocity = (current.weight - previous.weight) / (monthsDiff / 12)
```

#### 8. Assess Growth Status

**Height Assessment (HAZ):**
- HAZ < -2: Growth retardation ⚠️
- HAZ -2 to -1: Mild growth retardation
- HAZ -1 to +1: Normal ✓
- HAZ > +1: Tall stature

**Weight Assessment (WAZ):**
- WAZ < -3: Severe underweight ⚠️⚠️
- WAZ -3 to -2: Moderate underweight ⚠️
- WAZ -2 to -1: Mild underweight
- WAZ -1 to +2: Normal ✓
- WAZ > +2: Overweight ⚠️

**BMI Assessment (BAZ):**
- BAZ < -2: Wasting ⚠️
- BAZ -2 to +1: Normal ✓
- BAZ > +1: Overweight risk ⚠️
- BAZ > +2: Obese ⚠️⚠️

#### 9. Growth Abnormality Alerts

**Alert Conditions:**
- Height < -2SD (growth retardation)
- Weight < -2SD (underweight)
- BMI > +2SD (obesity)
- Growth velocity < 5th percentile

#### 10. Update Tracker File

**Data Structure:**
```json
{
  "date": "2025-06-20",
  "age": "5y5m",
  "age_months": 65,

  "height": {
    "value": 112.5,
    "percentile": 50,
    "z_score": 0.0,
    "velocity": 6.5,
    "velocity_period": "12_months",
    "velocity_percentile": 50
  },

  "weight": {
    "value": 20.5,
    "percentile": 55,
    "z_score": 0.13,
    "velocity": 2.8,
    "velocity_percentile": 60
  },

  "bmi": {
    "value": 16.2,
    "percentile": 60,
    "z_score": 0.25
  },

  "head_circumference": null,
  "comments": ""
}
```

#### 11. Output Confirmation

**Normal Growth:**
```
✅ Growth data recorded

Measurement Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: June 20, 2025
Age: 5 years 5 months (65 months)

Height: 112.5 cm
  Percentile: 50th percentile (P50) ✓
  Z-score: 0.0
  Growth velocity: 6.5 cm/year (50th percentile)

Weight: 20.5 kg
  Percentile: 55th percentile (P55) ✓
  Z-score: +0.13
  Growth velocity: 2.8 kg/year (60th percentile)

BMI: 16.2
  Percentile: 60th percentile (P60) ✓
  Z-score: +0.25

Growth Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Height: Normal (50th percentile)
✅ Weight: Normal (55th percentile)
✅ BMI: Normal (60th percentile)
✅ Growth velocity: Normal (50th percentile)
✅ Proportions: Well-proportioned

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Growth is normal

Child's height, weight, and BMI are all within
normal ranges, growth velocity is normal,
and body proportions are well-balanced.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue maintaining healthy lifestyle
✅ Balanced nutrition
✅ Moderate exercise
✅ Adequate sleep
✅ Regular health checkups

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This assessment is based on WHO Child Growth Standards,
for reference only and cannot replace professional medical diagnosis.

If you have questions about growth and development,
consult a pediatrician.

Data saved to: data/growth-records/2025-06/2025-06-20_growth-measurement.json
```

**Growth Abnormality Warning:**
```
⚠️ Growth Abnormality Notice

Measurement Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: June 20, 2025
Age: 5 years 5 months (65 months)

Height: 105.0 cm
  Percentile: 3rd percentile (P3) ⚠️
  Z-score: -1.9
  Growth velocity: 4.5 cm/year (3rd percentile) ⚠️

Weight: 16.5 kg
  Percentile: 5th percentile (P5) ⚠️
  Z-score: -1.6

BMI: 15.0
  Percentile: 15th percentile (P15) ⚠️

Growth Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Height: Growth retardation (3rd percentile)
⚠️ Weight: Underweight (5th percentile)
⚠️ Growth velocity: Slow growth velocity

Possible Causes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Genetic factors
• Malnutrition
• Chronic disease
• Endocrine abnormality
• Absorption disorder

🏥 Recommended Medical Visit:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommend consulting pediatrics or child health department:

Further Tests:
• Bone age assessment
• Nutritional assessment
• Endocrine tests
• Chromosome testing if necessary

Lifestyle Guidance:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Strengthen nutrition (quality protein)
✅ Supplement vitamin D
✅ Moderate exercise
✅ Adequate sleep
✅ Disease prevention

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Growth retardation requires professional assessment and intervention,
please seek medical attention promptly.

Data saved
```

---

### 2. View Growth Assessment - `status`

Display comprehensive assessment of current growth status.

**Parameter Description:**
- No parameters

**Examples:**
```
/growth status
```

**Execution Steps:**

#### 1. Read Latest Measurement Data

#### 2. Calculate Current Status

#### 3. Generate Assessment Report

```
📍 Child Growth Status Report

Basic Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: Xiao Ming
Gender: Male
Date of Birth: January 1, 2020
Current Age: 5 years 5 months

Latest Measurement (June 20, 2025):
━━━━━━━━━━━━━━━━━━━━━━━━━━
Height: 112.5 cm (50th percentile) ✓
Weight: 20.5 kg (55th percentile) ✓
BMI: 16.2 (60th percentile) ✓

Growth Trend:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Height velocity: 6.5 cm/year (normal)
Weight velocity: 2.8 kg/year (normal)

Growth Trajectory:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Height growing along 50th percentile
✓ Weight slightly above height percentile
✓ BMI within normal range

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Growth is normal

All metrics are within normal ranges,
growth velocity is normal, and the growth curve
rises steadily along the percentile line.

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This assessment is based on WHO Child Growth Standards,
for reference only and cannot replace professional medical diagnosis.

Data saved
```

---

### 3. View Percentile Analysis - `percentile`

Display detailed percentile and Z-score analysis.

**Parameter Description:**
- No parameters

**Examples:**
```
/growth percentile
```

**Execution Steps:**

#### 1. Read Latest Measurement Data

#### 2. Generate Percentile Report

```
📊 Growth Percentile Analysis Report

Measurement Date: June 20, 2025
Age: 5 years 5 months (Male)

Height Percentile:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Measured value: 112.5 cm
3rd percentile (P3): 102.1 cm
15th percentile (P15): 106.1 cm
50th percentile (P50): 110.0 cm ← current value
85th percentile (P85): 114.3 cm
97th percentile (P97): 117.9 cm

Current percentile: 50th percentile ✓
Z-score: 0.0 (normal)
Interpretation: Height is at the average level for boys of the same age

Weight Percentile:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Measured value: 20.5 kg
3rd percentile (P3): 13.7 kg
15th percentile (P15): 15.0 kg
50th percentile (P50): 16.7 kg
85th percentile (P85): 18.8 kg ← current value
97th percentile (P97): 20.9 kg

Current percentile: 55th percentile ✓
Z-score: +0.13 (normal)
Interpretation: Weight slightly above height percentile, within normal range

BMI Percentile:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Measured value: 16.2
3rd percentile (P3): 13.3
85th percentile (P85): 16.3 ← current value
97th percentile (P97): 16.4

Current percentile: 60th percentile ✓
Z-score: +0.25 (normal)
Interpretation: BMI within normal range, well-proportioned body

Overall Percentile:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Height, weight, and BMI all within normal range
✅ Weight slightly above height percentile, good nutritional status
✅ No obvious growth deviation

Data saved
```

---

### 4. View Growth Velocity - `velocity`

Display growth velocity analysis.

**Parameter Description:**
- No parameters

**Examples:**
```
/growth velocity
```

**Execution Steps:**

#### 1. Calculate Growth Velocity

Compare the two most recent measurements and calculate annual growth rate.

#### 2. Look Up WHO Velocity Standards

#### 3. Generate Velocity Report

```
📈 Growth Velocity Analysis Report

Current Age: 5 years 5 months
Gender: Male

Height Velocity:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Height increase: 6.5 cm/year
WHO standard reference:
  5th percentile: 4.7 cm/year
  50th percentile: 6.3 cm/year
  95th percentile: 7.9 cm/year

Assessment: Normal ✓
Velocity percentile: 50th percentile

Weight Velocity:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Weight increase: 2.8 kg/year
Assessment: Normal ✓

Growth Velocity Trend:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Height velocity normal
✅ Weight velocity normal
✅ No decline in growth velocity

Age-specific Growth Velocity Reference (Male):
━━━━━━━━━━━━━━━━━━━━━━━━━━
0-1 year: 20-30 cm/year
1-2 years: 10-14 cm/year
2-3 years: 8-11 cm/year
3-4 years: 7-9 cm/year
4-5 years: 6-8 cm/year
5-6 years: 6-7 cm/year ← current stage

Data saved
```

---

### 5. Growth Abnormality Check - `check`

Check for growth abnormalities and provide alerts.

**Parameter Description:**
- No parameters

**Examples:**
```
/growth check
```

**Execution Steps:**

#### 1. Check Various Growth Abnormalities

**Check Items:**
- Growth retardation: HAZ < -2
- Underweight: WAZ < -2
- Wasting: WHZ < -2
- Overweight: WAZ > +1
- Obesity: BAZ > +2
- Abnormal growth velocity: velocity < P5

#### 2. Generate Check Report

**No Abnormalities:**
```
✅ Growth Check Normal

Check Date: June 20, 2025
Age: 5 years 5 months

Check Items:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No growth retardation (height at 50th percentile)
✅ No underweight (weight at 55th percentile)
✅ No wasting (BMI at 60th percentile)
✅ No overweight (BMI at 60th percentile)
✅ No obesity (BMI at 60th percentile)
✅ Normal growth velocity (50th percentile)

Conclusion:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No growth abnormalities found

All check items are normal,
child's growth and development is good.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue regular monitoring
✅ Maintain healthy lifestyle
✅ Measure every 3-6 months

Data saved
```

**Abnormalities Found:**
```
⚠️ Growth Abnormalities Found

Check Date: June 20, 2025
Age: 5 years 5 months

Abnormal Items:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Growth Retardation
   Height: 105 cm (3rd percentile)
   Z-score: -1.9
   Cause requires further assessment

⚠️ Slow Growth Velocity
   Velocity: 4.5 cm/year (3rd percentile)
   Below normal range

Risk Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Possible causes:
• Malnutrition
• Endocrine abnormality
• Genetic factors
• Chronic disease
• Absorption disorder

🏥 Recommended Medical Visit:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommend consulting promptly:
• Pediatrics
• Child health department
• Endocrinology (if needed)

Tests:
• Bone age assessment
• Nutritional assessment
• Thyroid function
• Growth hormone levels

Lifestyle Guidance:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Strengthen nutrition
✅ Supplement vitamin D and calcium
✅ Moderate exercise
✅ Adequate sleep

⚠️ Important Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Growth retardation requires professional assessment and intervention,
please seek medical attention promptly.

Data saved
```

---

### 6. View History Data - `history`

Display historical measurement records.

**Parameter Description:**
- `count`: Number of records to display (optional, defaults to last 10)

**Examples:**
```
/growth history 12
```

**Execution Steps:**

#### 1. Read Historical Records

#### 2. Generate History Report

```
📋 Growth Measurement History

Last 12 records:

Date        Age       Height    Weight    BMI
────────────────────────────────────────
2025-06-20  5y5m    112.5    20.5    16.2
2025-03-15  5y2m    111.0    19.8    16.1
2024-12-10  4y11m   109.2    19.0    15.9
2024-09-05  4y8m    107.5    18.2    15.7
2024-06-01  4y5m    105.8    17.5    15.6
2024-03-01  4y2m    104.0    16.8    15.5
2023-12-01  3y11m   102.0    16.0    15.4
2023-09-01  3y8m    100.0    15.2    15.2
2023-06-01  3y5m    97.8     14.4    15.1
2023-03-01  3y2m    95.5     13.6    14.9
2022-12-01  2y11m   93.0     12.8    14.8
2022-09-01  2y8m    90.4     12.0    14.7

Growth Trend:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Height growing steadily
✅ Weight increasing steadily
✅ BMI remaining stable
✅ Normal growth velocity

Total measurements: 12
Tracking duration: 2 years 9 months

Data saved
```

---

## Data Structure

### Main File: data/growth-tracker.json

```json
{
  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male"
  },

  "growth_tracking": {
    "measurements": [
      {
        "date": "2025-06-20",
        "age_months": 65,
        "height": {
          "value": 112.5,
          "percentile": 50,
          "z_score": 0.0
        },
        "weight": {
          "value": 20.5,
          "percentile": 55,
          "z_score": 0.13
        },
        "bmi": {
          "value": 16.2,
          "percentile": 60,
          "z_score": 0.25
        }
      }
    ],

    "growth_assessment": {
      "overall": "normal",
      "height_status": "normal",
      "weight_status": "normal",
      "bmi_status": "normal"
    },

    "alerts": []
  },

  "statistics": {
    "total_measurements": 1,
    "tracking_duration_months": 65
  }
}
```

---

## Error Handling

| Scenario | Error Message | Suggestion |
|------|---------|------|
| Missing profile data | Missing child basic information<br>Please set /profile first | Guide to set basic information |
| Invalid measurement date | Measurement date cannot be a future date | Validate date |
| Abnormal measurement value | Measurement value exceeds reasonable range | Re-measure |
| No historical data | No historical records | Guide to record data first |

---

## Notes

- This system is based on WHO Child Growth Standards
- Premature infants (<37 weeks) need age correction until 2 years old
- Growth velocity is more important than a single measurement
- Regular monitoring recommended, every 3-6 months
- Cannot replace professional medical diagnosis
- Seek medical attention promptly for abnormal situations

---

## Example Usage

```
# Record growth data
/growth record 112.5cm 20.5kg
/growth record height 110 weight 18.5

# View assessment
/growth status
/growth percentile
/growth velocity
/growth check

# View history
/growth history 12
```
