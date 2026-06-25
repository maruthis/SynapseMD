---
description: Puberty development assessment and Tanner staging
arguments:
  - name: action
    description: "Action type: breast (breast development) / pubic (pubic hair) / menarche (first period) / testicular (testicles) / penis (penis) / voice (voice change) / bone-age (bone age) / status (status) / assessment (assessment) / check (precocious puberty check)"
    required: true
  - name: info
    description: Development information (stage, volume, age, etc., in natural language)
    required: false
---

# Puberty Development Assessment

Assess the degree of pubertal sexual development (Tanner staging) and identify precocious puberty or delayed development.

## Action Types

### 1. Girls' Puberty Assessment

#### 1.1 Record Breast Development - `breast`

**Examples:**
```
/growth puberty breast B3
/growth puberty breast stage 3
```

#### 1.2 Record Pubic Hair Development - `pubic`

**Examples:**
```
/growth puberty pubic P2
/growth puberty pubic hair stage 2
```

#### 1.3 Record First Period (Menarche) - `menarche`

**Examples:**
```
/growth puberty menarche true 11.5
/growth puberty menarche occurred at 11.5 years
```

### 2. Boys' Puberty Assessment

#### 2.1 Record Testicular Volume - `testicular`

**Examples:**
```
/growth puberty testicular 8ml
/growth puberty testicle volume 8
```

#### 2.2 Record Penis Development - `penis`

**Examples:**
```
/growth puberty penis 6.5cm
/growth puberty penis length 6.5
```

#### 2.3 Record Voice Change - `voice`

**Examples:**
```
/growth puberty voice true
/growth puberty voice changed
```

### 3. Bone Age Assessment - `bone-age`

**Examples:**
```
/growth puberty bone-age 10.8
```

### 4. Comprehensive Assessment - `assessment`

**Examples:**
```
/growth puberty assessment
```

### 5. Precocious Puberty Check - `check`

**Examples:**
```
/growth puberty check
```

---

## Tanner Staging Standards

### Girls' Breast Development (B staging)
- B1: Prepubertal
- B2: Breast bud emerges
- B3: Breast and areola enlarge
- B4: Areola protrudes
- B5: Mature breast

### Girls' Pubic Hair Development (P staging)
- P1: No pubic hair
- P2: Sparse, long, lightly pigmented
- P3: Coarser, curlier
- P4: Adult-type but smaller area
- P5: Adult-type

### Boys' Testicular Development
- 4–6 mL: G2 stage (onset)
- 6–10 mL: G3 stage
- 15–20 mL: G4 stage
- ≥20 mL: G5 stage (mature)

### Boys' Pubic Hair Development (P staging)
- P1–P5: Same as girls

---

## Precocious Puberty Standards

**Precocious puberty:**
- Girls: Breast development before age 8, or first period before age 10
- Boys: Testicular enlargement before age 9

**Delayed puberty:**
- Girls: No breast development by age 13, or no first period by age 16
- Boys: Testes not enlarged by age 14

---

## Bone Age Assessment

| Bone age vs. chronological age difference | Significance |
|------------------------------------------|--------------|
| < −1 year | Growth delay |
| −1 to +1 year | Normal range |
| > +1 year | Precocious puberty / accelerated growth |

---

## Data Structure

```json
{
  "puberty_tracking": {
    "female_development": {
      "breast_stage": "B3",
      "menarche": {
        "occurred": false,
        "age_at_menarche": null
      }
    },
    "male_development": {
      "testicular_volume": {
        "left": 8,
        "right": 8
      },
      "voice_break": false
    },
    "bone_age": {
      "chronological_age": 10.5,
      "bone_age": 10.8,
      "difference": "+0.3_years"
    },
    "assessment": "normal_progression"
  }
}
```

---

## Medical Safety Principles

### ⚠️ Hard Limits

1. **No medical diagnosis**
2. **No medication recommendations**
3. **No prediction of adult height**
4. **No replacement of professional medical advice**

### ✅ What This System Can Do

- Puberty development assessment (Tanner staging)
- Precocious puberty / delayed development screening
- Development progress tracking
- Bone age vs. chronological age difference calculation

---

## Example Usage

```
# Girls' puberty
/growth puberty breast B3
/growth puberty menarche true 11.2
/growth puberty assessment

# Boys' puberty
/growth puberty testicular 8ml
/growth puberty voice true
/growth puberty check
```

---

## Important Notice

This system is for puberty development assessment and record-keeping only. **It cannot replace professional medical advice.**

For all cases of precocious puberty, delayed development, or other abnormalities, **please consult a pediatric endocrinologist.**

Data is saved locally and is not uploaded to the cloud.
