# Specialist Expert Consultation System User Guide

## System Overview

This system simulates real-world multidisciplinary team (MDT) consultations through multiple specialist Skills and Subagents, helping you comprehensively analyze medical data.

## Core Components

### 1. Specialist Skill Definitions (.claude/specialists/)

Each specialty has an independent Skill definition file containing:
- Role definition and area of expertise
- Analysis focus and key indicators
- Analysis principles and safety boundaries
- Output format specifications
- Sample analysis language

**Supported 13 specialties + 1 coordinator:**
- `cardiology.md` - Cardiology
- `endocrinology.md` - Endocrinology
- `gastroenterology.md` - Gastroenterology
- `nephrology.md` - Nephrology
- `hematology.md` - Hematology
- `respiratory.md` - Respiratory Medicine
- `neurology.md` - Neurology
- `oncology.md` - Oncology
- `orthopedics.md` - Orthopedics [NEW]
- `dermatology.md` - Dermatology [NEW]
- `pediatrics.md` - Pediatrics [NEW]
- `gynecology.md` - Gynecology [NEW]
- `psychiatry.md` - Psychiatry/Psychology
- `general.md` - General Practice (Coordinator)

### 2. Consultation Coordinator (consultation-coordinator.md)

Responsible for:
- Identifying which specialties need to participate in the consultation
- Launching multiple specialist subagents in parallel
- Integrating specialist opinions
- Generating a comprehensive consultation report

### 3. Slash Commands

#### `/consult` - Multidisciplinary Expert Consultation

```bash
# Analyze all data
/consult all

# Analyze the most recent 5 records
/consult recent 5

# Analyze a specific date
/consult date 2025-12-31

# Analyze a date range
/consult date 2025-12-01 to 2025-12-31

# Default: analyze the most recent 3 records
/consult
```

#### `/specialist` - Single Specialty Consultation

```bash
# View supported specialties
/specialist list

# Consult cardiology
/specialist cardio recent 3

# Consult endocrinology
/specialist endo all

# Consult oncology
/specialist onco date 2025-12-31
```

**Specialty code list:**
- `cardio` - Cardiology
- `endo` - Endocrinology
- `gastro` - Gastroenterology
- `nephro` - Nephrology
- `heme` - Hematology
- `resp` - Respiratory Medicine
- `neuro` - Neurology
- `onco` - Oncology
- `ortho` - Orthopedics [NEW]
- `derma` - Dermatology [NEW]
- `pedia` - Pediatrics [NEW]
- `gyne` - Gynecology [NEW]
- `psych` - Psychiatry/Psychology
- `general` - General Practice

## Workflow

### Consultation Process

```
User inputs /consult
    ↓
Read medical data
    ↓
Identify abnormal indicators
    ↓
Determine participating specialties
    ↓
Launch specialist subagents in parallel
    ↓  ↓  ↓
Cardiology  Endocrinology  Gastroenterology ...
    ↓  ↓  ↓
  Each specialty analyzes
    ↓  ↓  ↓
    Consultation Coordinator
    ↓
Integrate opinions → Generate report
```

### Single Specialty Consultation Process

```
User inputs /specialist cardio
    ↓
Read Cardiology Skill definition
    ↓
Read medical data
    ↓
Launch Cardiology subagent
    ↓
Generate Cardiology analysis report
```

## Safety Boundaries (Strictly Observed)

All specialist experts strictly adhere to the following principles:

### ❌ Prohibited Actions
1. **Do not specify exact medication dosages**
   - ×: "Take atorvastatin 20mg"
   - √: "Recommend consulting a doctor to adjust lipid-lowering medication"

2. **Do not directly prescribe medication names**
   - ×: "Prescribe enteric-coated aspirin"
   - √: "Recommend consulting a doctor about whether antiplatelet therapy is needed"

3. **Do not make life-or-death prognosis judgments**
   - ×: "Poor prognosis, short survival"
   - √: "Recommend active treatment and regular follow-up evaluation"

4. **Do not replace physician diagnosis**
   - ×: "Diagnosed with coronary artery disease"
   - √: "Suggests possible coronary artery disease risk; recommend further cardiology examination"

### ✅ Permitted Actions
- Interpret the clinical significance of medical test indicators
- Identify abnormal indicators and potential risks
- Provide healthy lifestyle recommendations
- Recommend targeted examination items
- Assist in developing follow-up plans
- Integrate multidisciplinary expert opinions

## Usage Examples

### Example 1: Initial Consultation

Suppose you just completed a physical examination with multiple test results:

```bash
/consult all
```

The system will:
1. Read all examination data
2. Identify abnormal indicators
3. Automatically invite relevant specialties (e.g., cardiology, endocrinology, gastroenterology)
4. Analyze in parallel
5. Generate a comprehensive report, including:
   - Analysis from each specialty
   - Priority ranking
   - Integrated recommendations
   - Follow-up plan

### Example 2: In-Depth Specialty Analysis

If dyslipidemia is particularly prominent and you want a deeper cardiology consultation:

```bash
/specialist cardio all
```

The cardiologist will:
1. Analyze each lipid indicator in detail
2. Assess cardiovascular risk
3. Provide targeted diet and exercise recommendations
4. Suggest follow-up timing and items

### Example 3: Post-Follow-Up Comparison

After a follow-up visit, to see trend changes:

```bash
/consult recent 10
```

The system will analyze the most recent 10 records, observing:
- Indicator change trends
- Treatment efficacy evaluation
- Adjustments to management recommendations

## Report Format

### Consultation Report Includes:

1. **Case Summary** - Data overview
2. **Specialty Analyses** - Independent analysis from each specialty
3. **Comprehensive Assessment** - Key issue ranking (Urgent/Important/Routine)
4. **Integrated Recommendations** - Lifestyle, examination plan, specialist consultation recommendations
5. **Health Reminders** - Symptoms to watch for, monitoring priorities
6. **Follow-Up Plan** - Re-examination timing and expected goals
7. **Important Disclaimer** - Disclaimer statement

### Single Specialty Report Includes:

1. **Data Overview** - Main abnormal indicators
2. **Detailed Analysis** - Analysis categorized by system/indicator
3. **Risk Assessment** - Risk level and factors
4. **Recommendations** - Diet, exercise, monitoring, and medical visit recommendations

## Best Practices

### 1. Regular Consultations
It is recommended to run `/consult` to update the comprehensive assessment each time new examination results are available.

### 2. In-Depth Specialty Review
For particularly notable abnormalities, use `/specialist` for in-depth analysis.

### 3. Trend Observation
Use the `recent` parameter to analyze multiple records and observe trends.

### 4. Consultation on Demand
Select the appropriate specialty based on the specific issue.

## Technical Architecture

```
Claude Code
    ↓
Slash Commands (/consult, /specialist)
    ↓
Subagent System
    ├─> Specialist Skill Definitions (Expert Knowledge Base)
    ├─> Consultation Coordinator (Parallel Scheduling + Opinion Integration)
    └─> Medical Data (data/*.json)
    ↓
Analysis Reports (Markdown format)
```

## Notes

1. **Data Quality**: Ensure accurate recognition of examination results and complete data
2. **Privacy Protection**: All data is stored locally and not uploaded to the cloud
3. **Rational Use**: Reports are for reference only and do not replace physician diagnosis
4. **Seek Timely Care**: If urgent symptoms occur, seek medical attention immediately

## Newly Added Specialties (2025-12-31)

### Orthopedics
**Specialty Code**: `ortho`

**Areas of Expertise**:
- Fractures and bone injuries
- Arthritis (osteoarthritis, rheumatoid arthritis, gout)
- Osteoporosis
- Sports injuries
- Spinal disorders

**Key Indicators**:
- Bone metabolism: calcium, phosphorus, vitamin D, ALP, bone density
- Inflammation: CRP, ESR, uric acid
- Imaging: X-ray, CT, MRI, bone densitometry

**Use Cases**:
- Post-fracture surgery follow-up
- Joint pain assessment
- Osteoporosis screening

### Dermatology
**Specialty Code**: `derma`

**Areas of Expertise**:
- Eczema, dermatitis
- Acne
- Psoriasis
- Skin infections
- Skin tumor screening

**Key Indicators**:
- Allergy: IgE, eosinophils
- Inflammation: CRP, white blood cells
- Examinations: dermatoscopy, pathological biopsy

**Use Cases**:
- Allergic skin diseases
- Acne treatment
- Skin tumor screening

### Pediatrics
**Specialty Code**: `pedia`

**Areas of Expertise**:
- Child growth and development
- Neonatal diseases
- Nutritional disorders
- Childhood infections
- Vaccination

**Key Indicators**:
- Growth and development: height, weight, bone age (**age-specific reference values**)
- Nutrition: blood routine, iron, zinc, vitamin D
- Infection: CRP, white blood cells

**Use Cases**:
- Child health assessment
- Developmental delay screening
- Nutritional guidance

### Gynecology
**Specialty Code**: `gyne`

**Areas of Expertise**:
- Menstrual disorders
- Gynecological inflammation
- Uterine fibroids, ovarian cysts
- Cervical cancer screening
- Menopausal syndrome

**Key Indicators**:
- Sex hormones: FSH, LH, E2, P, T, PRL
- Tumor markers: CA125, CA19-9
- Screening: HPV, TCT

**Use Cases**:
- Menstrual irregularities
- PCOS assessment
- Cervical cancer screening
- Menopause management

## Future Expansions

- [x] Add more specialties (completed: orthopedics, dermatology, pediatrics, gynecology)
- [ ] Add rheumatology and immunology
- [ ] Add ophthalmology
- [ ] Add otolaryngology (ENT)
- [ ] Add urology
- [ ] Support consultation record export
- [ ] Add health trend charts
- [ ] Support consultation record comparison
- [ ] Add smart reminder features
