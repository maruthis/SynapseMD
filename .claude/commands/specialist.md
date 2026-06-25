---
description: Consult a specific specialist for targeted analysis
---

Based on the specialty specified by the user, launch the corresponding specialist expert for in-depth analysis.

## Supported Specialties

### Internal Medicine
| Specialty code | Specialty name | Skill file | Area of expertise |
|---------------|---------------|------------|-------------------|
| cardio | Cardiology | cardiology.md | Heart disease, hypertension, dyslipidemia |
| endo | Endocrinology | endocrinology.md | Diabetes, thyroid disease |
| gastro | Gastroenterology | gastroenterology.md | Liver disease, gastrointestinal conditions |
| nephro | Nephrology | nephrology.md | Kidney disease, electrolyte disorders |
| heme | Hematology | hematology.md | Anemia, coagulation disorders |
| resp | Pulmonology | respiratory.md | Pulmonary infections, lung nodules |
| neuro | Neurology | neurology.md | Cerebrovascular disease, headache, dizziness |
| onco | Oncology | oncology.md | Tumor markers, cancer screening |

### Surgery and Specialist Systems
| Specialty code | Specialty name | Skill file | Area of expertise |
|---------------|---------------|------------|-------------------|
| ortho | Orthopedics | orthopedics.md | Fractures, arthritis, osteoporosis |
| derma | Dermatology | dermatology.md | Eczema, acne, skin tumors |
| pedia | Pediatrics | pediatrics.md | Child development, neonatal conditions |
| gyne | Gynecology | gynecology.md | Menstrual disorders, gynecologic tumors |

### General Systems
| Specialty code | Specialty name | Skill file | Area of expertise |
|---------------|---------------|------------|-------------------|
| general | General Practice | general.md | Comprehensive assessment, chronic disease management |
| psych | Psychiatry | psychiatry.md | Mood disorders, mental health |

## How to Use

```bash
# List all supported specialties
/specialist list

# Consult a specific specialty
/specialist <specialty_code> [parameters]

# Examples:
/specialist cardio recent 3
/specialist endo all
/specialist ortho all
/specialist derma date 2025-12-31
/specialist pedia recent 5
/specialist gyne all
```

## Execution Process

### 1. Validate Specialty Code
Check whether the specialty code specified by the user is valid. If invalid, list all available specialties.

### 2. Read Specialty Skill Definition
Based on the specialty code, read the corresponding skill definition file:
```
.claude/specialists/<corresponding md file>
```

### 3. Collect Medical Data
Read relevant medical data based on user parameters:
- `all`: All data
- `recent N`: Most recent N records
- `date YYYY-MM-DD`: Specified date
- No parameter: Most recent 3 records

**Added: Chronic disease data reading**
For specific specialties, also read relevant chronic disease management data:
- **cardio (Cardiology)**: Read `data/hypertension-tracker.json` (hypertension management data)
- **endo (Endocrinology)**: Read `data/diabetes-tracker.json` (diabetes management data)
- **resp (Pulmonology)**: Read `data/copd-tracker.json` (COPD management data)
- **nephro (Nephrology)**: Read hypertension and diabetes management data (assess renal risk)

**Data reading priority:**
1. Chronic disease management data (if available)
2. Examination report data (saved via /save-report)
3. Other relevant medical records

### 4. Launch Specialist Analysis
Use the Task tool to launch the specialty's subagent, passing:
- Specialty skill definition content
- Medical data content
- Analysis requirements

to the subagent.

### 5. Display Analysis Report
Present the specialist analysis report returned by the subagent directly to the user.

## Example Prompt (for launching subagent)

```
You are a {{specialty name}} specialist. Please perform a medical data analysis according to the following Skill definition:

## Skill Definition
{{Read the complete content of .claude/specialists/{{corresponding md file}}}}

## Patient Medical Data

### Chronic Disease Management (if available)
{{Read the corresponding chronic disease data file:
- cardio: data/hypertension-tracker.json
- endo: data/diabetes-tracker.json
- resp: data/copd-tracker.json
- nephro: data/hypertension-tracker.json + data/diabetes-tracker.json
}}

### Recent Examination Data
{{Read relevant examination report data}}

## Analysis Requirements
1. Output the analysis report strictly in the format defined in the Skill
2. **Prioritize analysis of chronic disease management (if available)**:
   - Date of diagnosis and classification
   - Control status (attainment rate, averages, etc.)
   - Target organ damage / complication status
   - Risk assessment
3. Conduct a comprehensive analysis integrating examination report data
4. Strictly adhere to the following safety guidelines:
   - Do not provide specific medication dosages
   - Do not directly prescribe medication names
   - Do not make prognosis judgments about life or death
   - Do not replace physician diagnosis
5. Provide specific and actionable recommendations
```

**Specialist analysis report format (enhanced):**

```markdown
## {{Specialty name}} Analysis Report

### Chronic Disease Management (if available)
**{{Chronic disease name}} Control Status**: [Based on chronic disease management data]
- Diagnosis date: YYYY-MM-DD
- Grade / Classification: {{classification}}
- Recent control indicators: {{key metrics}}
- Target attainment: {{achievement status}}
- Target organ damage / complications: {{status}}
- Risk assessment: {{risk level}}

### Recent Examination Data
[Other examination data analysis...]

### Comprehensive Assessment
[Comprehensive analysis combining chronic disease and examination data]

### Recommendations
- Lifestyle: [Specific recommendations]
- Dietary adjustments: [Specific recommendations]
- Medical consultation: [Whether a visit or follow-up is needed]
```

Please begin the analysis and return a complete report.

## Safety Guidelines (emphasized in every consultation)

- ❌ Do not provide specific medication dosages
- ❌ Do not directly prescribe medication names
- ❌ Do not make prognosis judgments about life or death
- ❌ Do not replace physician diagnosis

## Error Handling

### Invalid Specialty Code
```
❌ Specialty "xyz" not found

Available specialties:

**Internal Medicine**
- cardio: Cardiology
- endo: Endocrinology
- gastro: Gastroenterology
- nephro: Nephrology
- heme: Hematology
- resp: Pulmonology
- neuro: Neurology
- onco: Oncology

**Surgery and Specialist Systems**
- ortho: Orthopedics
- derma: Dermatology
- pedia: Pediatrics
- gyne: Gynecology

**General Systems**
- general: General Practice
- psych: Psychiatry

Use /specialist list for detailed information
```

### No Medical Data Available
```
⚠️ No medical data is currently in the system

Please use /save-report to save your medical examination records first, then proceed with the specialist consultation.
```

## Usage Recommendations and Best Practices

### 1. Specialty Selection Guide

#### Choose by Symptom
- **Chest pain, palpitations** → cardio (Cardiology)
- **Joint pain, fracture** → ortho (Orthopedics)
- **Rash, itching** → derma (Dermatology)
- **Irregular periods** → gyne (Gynecology)
- **Children's health** → pedia (Pediatrics)

#### Choose by Test Result
- **Abnormal blood lipids** → cardio (Cardiology)
- **Abnormal bone density** → ortho (Orthopedics)
- **Abnormal sex hormones** → gyne (Gynecology)

### 2. Parameter Selection Guide
- **First visit / comprehensive examination**: Use `all` parameter
- **Follow-up comparison**: Use `recent N` (N = 5–10)
- **Specific date**: Use `date YYYY-MM-DD`

### 3. Common Use Cases

#### Case 1: Post-physical-exam Comprehensive Assessment
```bash
/consult all
/specialist cardio all
/specialist ortho all
```

#### Case 2: Child Health Check
```bash
/specialist pedia all
```

#### Case 3: Women's Health
```bash
/specialist gyne all
```

## Start Execution

Based on the specialty specified by the user, launch the corresponding specialist expert for in-depth analysis.

If the user does not specify parameters, analyze the most recent 3 records by default.
