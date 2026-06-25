---
description: Manage family member health information, record family medical history, assess genetic risks, generate family health reports
arguments:
  - name: action
    description: "Action type: add-member (add member) / add-history (record history) / track (track health) / report (generate report) / list (list members) / risk (risk assessment)"
    required: true
  - name: info
    description: Detailed information (member info, medical history description, etc., in natural language)
    required: false
---

# Family Health Management

Comprehensive family health record management to help record family medical history, assess genetic risks, and maintain family health.

## ⚠️ Medical Safety Statement

**Important: This system is for health records and family medical history management only and cannot replace professional medical diagnosis and treatment.**

- ❌ Does not provide genetic disease diagnosis
- ❌ Does not predict individual disease probability
- ❌ Does not recommend specific treatment plans
- ❌ Does not replace genetic counselors
- ✅ Records family medical history
- ✅ Assesses genetic risk (for reference only)
- ✅ Generates family health reports
- ✅ Provides prevention recommendations and screening reminders

All medical decisions should follow physician guidance. Genetic risk assessment results are for reference only; please consult a professional physician or genetic counselor for specific risks.

## Action Types

### 1. Add Family Member - `add-member`

Add a family member to the health record.

**Parameter Description:**
- `info`: Member information (required), describe in natural language

**Examples:**
```
/family add-member father Zhang San 1960-05-15 blood_type_A
/family add-member mother Li Si 1962-08-20 blood_type_B
/family add-member son Xiao Ming 2010-03-10 blood_type_A
/family add-member spouse Wang Wu 1988-12-05 blood_type_O
```

**Supported Information:**
- Relationship: father/mother/spouse/son/daughter/brother/sister, etc.
- Name: member's name
- Date of birth: YYYY-MM-DD format or age
- Blood type: A/B/AB/O
- Gender: male/female (usually inferred from relationship)

**Execution Steps:**
1. Parse relationship type and member information
2. Generate unique member_id
3. Validate relationship integrity and age reasonableness
4. Save to `data/family-health-tracker.json`
5. Output confirmation information

**Data Structure:**
```json
{
  "member_id": "mem_20250108_001",
  "name": "Zhang San",
  "relationship": "father",
  "gender": "male",
  "birth_date": "1960-05-15",
  "blood_type": "A",
  "status": "living",
  "created_at": "2025-01-08T10:00:00.000Z"
}
```

### 2. Record Family Medical History - `add-history`

Record disease history of family members.

**Parameter Description:**
- `info`: Medical history information (required), describe in natural language

**Examples:**
```
/family add-history father hypertension diagnosed_at_50
/family add-history mother diabetes onset_at_55
/family add-history paternal_grandfather coronary_heart_disease age_60
/family add-history maternal_grandmother breast_cancer age_58
```

**Supported Information:**
- Member: family member name or relationship
- Disease name: hypertension, diabetes, coronary heart disease, etc.
- Age at onset: age at diagnosis or onset
- Severity: mild/moderate/severe (optional)
- Notes: other relevant information (optional)

**Execution Steps:**
1. Parse member and disease information
2. Identify disease category (cardiovascular/metabolic/tumor, etc.)
3. Record age at onset and severity
4. Update family_medical_history
5. Output confirmation information

**Data Structure:**
```json
{
  "history_id": "hist_20250108_001",
  "disease_name": "Hypertension",
  "disease_category": "cardiovascular",
  "affected_member_id": "mem_20250108_001",
  "age_at_onset": 50,
  "severity": "moderate",
  "notes": "Well controlled with medication",
  "reported_date": "2025-01-08"
}
```

### 3. Track Member Health - `track`

Track health data for family members (blood pressure, blood glucose, medications, etc.).

**Parameter Description:**
- `info`: Health data (required), specify member and data type

**Examples:**
```
/family track father blood_pressure 135/85
/family track mother blood_glucose 7.2
/family track son height weight 120cm 25kg
/family track list
```

**Supported Data Types:**
- Blood pressure: systolic/diastolic
- Blood glucose: fasting blood glucose value
- Weight: weight/BMI
- Height: height value
- Medications: medication name and dosage

**Execution Steps:**
1. Identify member and data type
2. Integrate existing health module data
3. Record to member health file
4. Update health trends
5. Output record results

**Integrated Modules:**
- hypertension-tracker.json (blood pressure)
- diabetes-tracker.json (blood glucose)
- nutrition-tracker.json (weight)

### 4. List Family Members - `list`

Display all family member information.

**Examples:**
```
/family list
/family list brief
/family list detailed
```

**Output Content:**
- Member list
- Relationship and age
- Health status overview
- Family medical history summary

### 5. Genetic Risk Assessment - `risk`

Assess and display family genetic risks.

**Examples:**
```
/family risk
/family risk hypertension
/family risk diabetes
/family risk all
```

**Output Content:**
- Genetic risk level (high/medium/low)
- Affected family members
- Risk factor analysis
- Prevention recommendations

**Risk Calculation:**
```
Genetic Risk Score = (Number of first-degree relatives affected × 0.4) +
                    (Number of early-onset cases × 0.3) +
                    (Family clustering degree × 0.3)

Risk Level:
- High risk: ≥70%
- Moderate risk: 40%-69%
- Low risk: <40%
```

**Note:** Risk assessment is based on family medical history statistics, for reference only, and does not predict individual disease occurrence.

### 6. Generate Family Health Report - `report`

Generate a complete family health analysis report.

**Examples:**
```
/family report
/family report html
/family report genetic_risk
```

**Report Content:**
- Family member health overview
- Family medical history summary
- Genetic risk analysis
- Common health issues
- Prevention recommendation checklist
- Screening recommendation schedule

**Output Formats:**
- Text report: command-line output
- HTML report: visual charts (family tree, risk charts, etc.)

**HTML Visualization Includes:**
- Family tree (multi-generation display)
- Genetic risk heat map
- Disease distribution charts
- Prevention recommendation timeline

## Disease Category Reference

### Cardiovascular Diseases
- Hypertension
- Coronary heart disease
- Cardiomyopathy
- Arrhythmia
- Stroke

### Metabolic Diseases
- Diabetes (type 1/type 2)
- Hyperlipidemia
- Gout
- Metabolic syndrome

### Tumors
- Lung cancer
- Breast cancer
- Colorectal cancer
- Gastric cancer
- Liver cancer

### Respiratory System
- Asthma
- COPD
- Pulmonary fibrosis

### Other
- Glaucoma
- Mental illness
- Autoimmune diseases

## Relationship Type Standards

### Direct Relatives
- self: self
- father: father
- mother: mother
- spouse: spouse
- son: son
- daughter: daughter

### Collateral Relatives
- brother: brother
- sister: sister
- paternal_grandfather: paternal grandfather
- paternal_grandmother: paternal grandmother
- maternal_grandfather: maternal grandfather
- maternal_grandmother: maternal grandmother

### Complex Relationships
- half_brother: half-brother
- half_sister: half-sister
- adopted: adoptive relationship

## Genetic Risk Reference

### High Risk Characteristics
- Multiple first-degree relatives affected
- Early-onset cases (<50 years old)
- Obvious family clustering
- Clear inheritance pattern

### Moderate Risk Characteristics
- 1-2 first-degree relatives affected
- Middle-age onset (50-65 years old)
- Mild family clustering

### Low Risk Characteristics
- Only distant relatives affected
- Late-onset cases (>65 years old)
- Sporadic cases

## Prevention Recommendation Reference

### High Risk for Cardiovascular Disease
- Regular blood pressure monitoring (3 times per week)
- Limit sodium intake (<5g/day)
- Regular aerobic exercise (150 minutes per week)
- Weight management (BMI<24)
- Regular health checkups starting at age 35

### High Risk for Diabetes
- Control weight and waist circumference
- Low-sugar, low-fat diet
- Increase dietary fiber
- Regular exercise
- Annual blood glucose testing starting at age 40

### High Risk for Tumors
- Regular screening as directed by physician
- Avoid carcinogens (smoking, alcohol)
- Healthy lifestyle
- Vaccinations (e.g., hepatitis B vaccine)
- Watch for early symptoms

## Data Structure

### Family Information Structure
```json
{
  "family_info": {
    "family_id": "fam_20250108_001",
    "created_date": "2025-01-08",
    "last_updated": "2025-01-08"
  }
}
```

### Member Array Structure
```json
{
  "members": [
    {
      "member_id": "mem_20250108_001",
      "name": "Zhang San",
      "relationship": "father",
      "gender": "male",
      "birth_date": "1960-05-15",
      "blood_type": "A",
      "status": "living",
      "created_at": "2025-01-08T10:00:00.000Z",
      "personal_health": {
        "chronic_conditions": ["Hypertension"],
        "allergies": [],
        "medications": ["Amlodipine"],
        "genetic_tests": []
      }
    }
  ]
}
```

### Family Medical History Structure
```json
{
  "family_medical_history": {
    "hereditary_diseases": [
      {
        "disease_name": "Hypertension",
        "category": "cardiovascular",
        "affected_members": ["mem_001", "mem_002"],
        "inheritance_pattern": "complex",
        "age_range": {"min": 40, "max": 65, "avg": 52}
      }
    ],
    "common_conditions": [],
    "genetic_disorders": []
  }
}
```

### Risk Assessment Structure
```json
{
  "risk_assessment": {
    "last_assessment_date": "2025-01-08",
    "hereditary_risks": [
      {
        "disease": "Hypertension",
        "risk_level": "high",
        "confidence": "medium",
        "affected_members": ["Father"],
        "risk_factors": ["First-degree relative affected", "Early onset (<50 years)"]
      }
    ],
    "preventive_recommendations": [
      {
        "category": "screening",
        "action": "Regular blood pressure monitoring",
        "frequency": "3 times per week",
        "start_age": 35,
        "priority": "high"
      }
    ]
  }
}
```

## Error Handling

- **Member not found**: "Member XXX not found, please use /family add-member to add first"
- **Invalid relationship**: "Relationship type XXX not supported, please use: father/mother/spouse/child, etc."
- **Unreasonable age**: "Parents should be at least 15 years older than children"
- **Incomplete data**: "Please provide complete member information, e.g.: /family add-member father Zhang San 1960-05-15"
- **No data**: "No family health records yet, please add family members first"
- **File read failure**: "Unable to read family health data, please check data file"

## Example Usage

```
# Add family members
/family add-member father Zhang San 1960-05-15 blood_type_A
/family add-member mother Li Si 1962-08-20 blood_type_B
/family add-member spouse Wang Wu 1988-12-05 blood_type_O

# Record family medical history
/family add-history father hypertension diagnosed_at_50
/family add-history mother diabetes onset_at_55
/family add-history paternal_grandfather coronary_heart_disease age_60

# View family members
/family list

# Assess genetic risk
/family risk hypertension
/family risk

# Track health data
/family track father blood_pressure 135/85
/family track mother blood_glucose 7.2

# Generate report
/family report
/family report html
```

## Notes

- Family medical history information is important; record as completely as possible
- Genetic risk is for reference only and does not predict individual disease occurrence
- It is recommended to regularly update family medical history information
- High-risk individuals should start screening earlier
- All medical decisions should consult a professional physician
- For genetic counseling, consult a professional genetic counselor
- Data privacy protection: all information is stored locally only

## Integrated Modules

This module integrates with the following health modules:

- **Hypertension Management** (`/bp`): Track blood pressure data
- **Diabetes Management** (`/diabetes`): Track blood glucose data
- **Medication Management** (`/medication`): Track medication records
- **Nutrition Management** (`/nutrition`): Track weight data
- **Health Trend Analysis** (`health-trend-analyzer`): Analyze family health trends

---

**Disclaimer: This system is for health records only and does not replace professional medical diagnosis and treatment. Genetic risk assessment is for reference only; please consult a professional physician or genetic counselor for specific risks.**
