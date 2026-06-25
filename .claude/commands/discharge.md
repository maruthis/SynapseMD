---
description: Save discharge summary information
arguments:
  - name: source
    description: Discharge summary source (image path or text description)
    required: true
  - name: admission_date
    description: "Admission date (format: YYYY-MM-DD, optional)"
    required: false
  - name: discharge_date
    description: "Discharge date (format: YYYY-MM-DD, optional)"
    required: false
---

# Discharge Summary Management

Used to save and structure discharge summary information, supporting extraction from images or direct processing from text descriptions.

## Parameter Description

- `source` (required): Discharge summary source, can be:
  - Image path: `@medical-reports/discharge-summary.jpg`
  - Text description: Paste the text content or summary of the discharge summary directly

- `admission_date` (optional): Admission date, format YYYY-MM-DD
- `discharge_date` (optional): Discharge date, format YYYY-MM-DD

## Execution Steps

### Case 1: Extract from Image

If the user provides an image path:

1. **Read and analyze the image**
   - Use the Read tool to read the discharge summary image
   - Use the mcp__4_5v_mcp__analyze_image tool to analyze the image content

   **Image analysis prompt template:**
   ```
   Please carefully identify all content in this discharge summary, including:

   1. **Basic Information:**
      - Patient name
      - Gender, age
      - Admission date, discharge date
      - Days of hospitalization
      - Department, bed number
      - Insurance type

   2. **Diagnosis Information:**
      - Admission diagnosis (main diagnosis and other diagnoses)
      - Discharge diagnosis (main diagnosis and other diagnoses)
      - Diagnosis codes (ICD-10, if available)

   3. **Treatment Course:**
      - Main treatment measures
      - Surgical records (if any)
      - Drug treatment plan
      - Summary of examination results

   4. **Discharge Status:**
      - Condition status at discharge
      - Symptom improvement
      - Vital signs

   5. **Discharge Orders:**
      - Medication instructions (drug name, dosage, usage, duration)
      - Dietary guidance
      - Activity guidance
      - Wound care (if any)
      - Follow-up plan and timing
      - Precautions

   6. **Other Information:**
      - Attending physician
      - Hospital name
      - Hospitalization costs (if available)
      - Follow-up phone number

   Please list all information in a structured manner, maintaining accuracy of the original text.
   ```

2. **Extract and structure data**
   - Extract all key fields from image recognition results
   - Organize into structured JSON format

### Case 2: Process from Text Description

If the user provides text content directly:

1. **Analyze text content**
   - Extract information from the user-provided text
   - Classify according to the data structure below

2. **Ask for missing information**
   - If key information is missing, ask the user to supplement

### 2. Generate Data File

**File path format:**
`data/discharge-summaries/YYYY-MM/YYYY-MM-DD_main-diagnosis.json`

**JSON data structure:**
```json
{
  "id": "{{Generate unique ID using date+timestamp}}",
  "basic_info": {
    "hospital": "General Hospital",
    "department": "Gastroenterology",
    "admission_date": "2024-08-10",
    "discharge_date": "2024-08-15",
    "hospitalization_days": 5,
    "bed_number": "Bed 23",
    "insurance_type": "Employee Insurance"
  },
  "diagnosis": {
    "admission_diagnosis": {
      "main": "Acute Cholecystitis",
      "secondary": [
        "Gallstones",
        "Hypertension (Grade 2, moderate risk)"
      ],
      "icd_codes": {
        "main": "K80.0",
        "secondary": ["I10"]
      }
    },
    "discharge_diagnosis": {
      "main": "Acute Cholecystitis",
      "secondary": [
        "Gallstones",
        "Hypertension (Grade 2, moderate risk)",
        "Type 2 Diabetes"
      ],
      "icd_codes": {
        "main": "K80.0",
        "secondary": ["I10", "E11.9"]
      }
    }
  },
  "treatment_summary": {
    "main_treatments": [
      "NPO, gastrointestinal decompression",
      "Anti-infection treatment (Cefoperazone Sodium Sulbactam Sodium)",
      "Antispasmodic and analgesic treatment",
      "IV fluid support treatment"
    ],
    "medications": [
      {
        "drug_name": "Cefoperazone Sodium Sulbactam Sodium",
        "dosage": "2.0g",
        "frequency": "Every 12 hours",
        "route": "IV drip",
        "duration": "5 days"
      },
      {
        "drug_name": "Atropine",
        "dosage": "0.5mg",
        "frequency": "As needed",
        "route": "Intramuscular injection"
      }
    ],
    "procedures": [],
    "surgeries": [
      {
        "surgery_name": "Laparoscopic Cholecystectomy",
        "surgery_date": "2024-08-12",
        "anesthesia": "General anesthesia",
        "surgeon": "Dr. Zhang"
      }
    ],
    "examination_results": "CBC: WBC 12.5×10^9/L, N% 85%; Abdominal ultrasound: thickened gallbladder wall, gallstones"
  },
  "discharge_status": {
    "condition": "Improved",
    "symptoms": "Abdominal pain relieved, no fever, diet restored",
    "vital_signs": {
      "blood_pressure": "130/80 mmHg",
      "heart_rate": "78 bpm",
      "temperature": "36.5°C",
      "respiration": "18 breaths/min"
    },
    "activity_level": "Can get out of bed"
  },
  "discharge_orders": {
    "medication_instructions": [
      {
        "drug_name": "Amoxicillin Capsules",
        "dosage": "0.5g",
        "frequency": "3 times daily",
        "route": "Oral",
        "duration": "7 days",
        "notes": "Take after meals"
      }
    ],
    "dietary_guidance": "Low-fat diet, small frequent meals, avoid greasy foods",
    "activity_guidance": "Moderate activity, avoid strenuous exercise and heavy physical labor",
    "wound_care": "Keep wound dry and clean, change dressing every 3 days, seek medical attention immediately if redness, swelling, heat, or pain occurs",
    "follow_up_plan": [
      {
        "item": "Post-operative check-up",
        "timing": "2 weeks post-surgery",
        "location": "General Surgery Outpatient",
        "purpose": "Suture removal, assessment of recovery"
      },
      {
        "item": "Abdominal ultrasound",
        "timing": "1 month post-surgery",
        "purpose": "Assess abdominal condition"
      }
    ],
    "warnings": [
      "If fever, abdominal pain, jaundice, or other symptoms occur, seek medical attention promptly",
      "Avoid overeating and high-fat diet",
      "Take medication regularly, do not stop on your own"
    ]
  },
  "attending_physician": {
    "name": "Dr. Zhang",
    "title": "Attending Physician"
  },
  "financial_info": {
    "total_cost": 18500.50,
    "insurance_coverage": 12000.00,
    "self_payment": 6500.50
  },
  "original_source": {
    "type": "image/text",
    "file_path": "images/discharge-summary.jpg",
    "created_at": "2024-08-15"
  },
  "notes": "Other supplementary information or special notes"
}
```

### 3. Save Data

- If it's an image, copy it to `data/discharge-summaries/YYYY-MM/images/`
- Create monthly directory (if it doesn't exist)
- Save JSON data file
- Update global index `data/index.json`

### 4. Update Index

Add new record in `data/index.json`:
```json
{
  "records": [
    {
      "id": "Record ID",
      "type": "Discharge Summary",
      "admission_date": "YYYY-MM-DD",
      "discharge_date": "YYYY-MM-DD",
      "main_diagnosis": "Main Diagnosis",
      "file_path": "discharge-summaries/YYYY-MM/YYYY-MM-DD_main-diagnosis.json"
    }
  ]
}
```

### 5. Report Results

```
✅ Discharge summary saved

Hospitalization Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Hospital: General Hospital
Department: Gastroenterology
Admission date: 2024-08-10
Discharge date: 2024-08-15
Days hospitalized: 5 days

Main Diagnosis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Admission diagnosis: Acute Cholecystitis
Discharge diagnosis: Acute Cholecystitis

Main Treatment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Laparoscopic Cholecystectomy (2024-08-12)
- Anti-infection treatment
- Antispasmodic and analgesic treatment

Discharge Orders:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Medication: Amoxicillin Capsules 0.5g 3 times daily × 7 days
Diet: Low-fat diet, small frequent meals
Follow-up: Outpatient check-up 2 weeks post-surgery

Data saved to:
data/discharge-summaries/2024-08/2024-08-15_acute-cholecystitis.json
```

## Smart Extraction Rules

### Diagnosis Information Extraction

- **Main diagnosis**: Usually the first diagnosis listed
- **Secondary diagnosis**: Comorbidities, complications
- **ICD-10 codes**: Automatically extracted if available

### Surgical Information Extraction

- Identify "surgery name," "surgery date," "anesthesia method"
- Automatically link to surgical records (if they already exist)

### Drug Information Extraction

Extract from discharge orders:
- Drug name (generic name)
- Dosage (e.g., 0.5g, 10mg)
- Usage (3 times daily, as needed)
- Administration route (oral, IV drip)
- Duration (7 days, as directed)

### Follow-up Plan Extraction

Identify:
- Follow-up time points (e.g., "2 weeks post-surgery," "1 month later")
- Follow-up items (e.g., "CBC," "ultrasound")
- Follow-up location (e.g., "outpatient," "specific department")

## Usage Examples

### Extract from image:

```bash
# Automatically extract dates
/discharge @medical-reports/discharge-summary.jpg

# Manually specify dates
/discharge @medical-reports/discharge-summary.jpg 2024-08-10 2024-08-15
```

### From text description:

```bash
# Paste discharge summary content directly
/discharge I was hospitalized for acute cholecystitis on August 10 and discharged on August 15, had laparoscopic surgery, doctor told me low-fat diet, check-up in 2 weeks

# Brief description
/discharge Hospitalized for 5 days in August 2024 due to pneumonia, need to continue antibiotics for 3 days after discharge, chest X-ray follow-up in one week
```

## Extended Features

### Auto-linking

- If the discharge summary mentions surgery, automatically link to or create the corresponding surgical record
- If there are abnormal lab/examination results, automatically link to examination records

### Data Validation

- Validate date logic (discharge date cannot be earlier than admission date)
- Validate drug dosage reasonableness
- Check completeness of required fields

### Reminder Features

- Based on discharge orders, remind of follow-up times
- Remind of medication completion status
- Remind of precautions

## Notes

- If the image is blurry or some content cannot be recognized, make the best effort to extract recognizable information
- Key information (diagnosis, treatment, orders) must be accurately extracted
- If unable to recognize, ask the user to supplement
- Drug information should be as complete as possible, including generic name and dosage
- Follow-up plans should accurately capture time points
- All dates should use YYYY-MM-DD format uniformly
- Maintain accuracy of the original text, do not add content on your own

## Data Query

Discharge summaries can be queried via the `/query discharge` command:
- Query all discharge records
- Query by time range
- Query by diagnosis
- Query by hospital
- Query by department

## Special Scenario Handling

### Multiple Hospitalizations

For the same illness with multiple hospitalizations, each discharge summary is saved separately and linked through association fields

### Department Transfer Records

If there were department transfers during hospitalization, record all departments and corresponding times

### Critical Care Records

Specially mark rescue records and rescue times

### Deceased Cases

If the patient died, specially annotate and record the cause and time of death
