---
description: Record personal surgical history
arguments:
  - name: description
    description: Surgery description (one sentence including surgery name, date, reason, and other information)
    required: true
---

# Personal Surgical History Records

Used to record personal surgical history, extracting structured surgery information from natural language descriptions.

## Parameter Description

- `description` (required): A one-sentence description of the surgery, which may include:
  - Surgery name (medical term or common name)
  - Surgery date
  - Reason / diagnosis for surgery
  - Body part operated on
  - Other relevant information

## Execution Steps

### 1. Parse User Input

Extract the following information from the user's natural language description:

**Required fields:**
- **Full surgery name (medical term)**: e.g. "Laparoscopic cholecystectomy"
- **Common name**: e.g. "Minimally invasive gallbladder surgery"
- **Reason for surgery / preoperative diagnosis**: e.g. "Chronic calculous cholecystitis"
- **Surgery date (year-month-day)**: e.g. "2024-08-15"
- **Body part**: e.g. "Abdomen"

**Optional fields (extracted from description or asked):**
- Surgery type: elective / emergency / day_surgery
- Anesthesia type: general / local / spinal / nerve block
- Surgery duration: minutes
- Intraoperative blood loss: mL
- Surgeon: doctor's name
- Hospital: hospital name
- Days hospitalized: number of days

### 2. Ask About Implants

**Must ask the user:**
```
📋 Implant Information Confirmation

Were any of the following medical materials implanted during this surgery?
- Artificial joint / implant
- Stent / catheter
- Metal internal fixation (plate, screw, pin, etc.)
- Artificial valve / pacemaker
- Hernia mesh / patch
- Other implants

A. Implants were used
B. No implants
```

If "Implants were used" is selected, ask for details:
```
Please provide implant information:
1. Implant name: e.g. "Titanium plate", "Coronary artery stent"
2. Implant model / specification: e.g. "Brand X, Model Y"
3. Implant location: specific position
4. Quantity: number
5. Planned removal time: if applicable (e.g. "remove in 3 months", "permanent")
```

### 3. Generate Data File

**File path format:**
`data/surgery-records/YYYY-MM/YYYY-MM-DD_surgery-name.json`

**JSON data structure:**
```json
{
  "id": "{{generate unique ID using date + timestamp}}",
  "basic_info": {
    "surgery_name": "Laparoscopic cholecystectomy",
    "surgery_alias": "Minimally invasive gallbladder surgery",
    "surgery_date": "2024-08-15",
    "preoperative_diagnosis": "Chronic calculous cholecystitis",
    "body_part": "Abdomen",
    "surgery_type": "elective",
    "anesthesia_type": "general",
    "duration_minutes": 90,
    "blood_loss_ml": 50,
    "surgeon": "Dr. Zhang",
    "hospital": "General Hospital",
    "hospitalization_days": 3
  },
  "implants": {
    "has_implants": false,
    "implants_list": []
  },
  "postoperative_info": {
    "complications": null,
    "recovery_status": "Good",
    "follow_up_plan": null
  },
  "notes": "User's supplementary notes or other important information",
  "created_at": "2024-08-15",
  "original_input": "User's original input description"
}
```

**If implants are included, example implants structure:**
```json
{
  "has_implants": true,
  "implants_list": [
    {
      "implant_name": "Titanium alloy plate",
      "model": "Brand X, Model Y",
      "location": "Right tibia, mid-shaft",
      "quantity": 1,
      "removal_plan": "Remove in 12 months",
      "implant_date": "2024-08-15"
    }
  ]
}
```

### 4. Save Data

- Create the monthly directory (if it does not exist)
- Save the JSON data file
- Update the global index `data/index.json`

### 5. Update Index

Add a new record in `data/index.json`:
```json
{
  "records": [
    {
      "id": "record ID",
      "type": "surgery record",
      "date": "YYYY-MM-DD",
      "file_path": "surgery-records/YYYY-MM/YYYY-MM-DD_surgery-name.json"
    }
  ]
}
```

### 6. Report Results

```
✅ Surgery record saved

Basic information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Surgery name: Laparoscopic cholecystectomy (Minimally invasive gallbladder surgery)
Surgery date: 2024-08-15
Preoperative diagnosis: Chronic calculous cholecystitis
Body part: Abdomen
Surgery type: Elective surgery
Anesthesia: General anesthesia
Duration: 90 minutes
Blood loss: 50 mL

Implant information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
No implants

Data saved to:
data/surgery-records/2024-08/2024-08-15_laparoscopic-cholecystectomy.json
```

## Surgery Type Classification

- **elective**: Surgery that can be scheduled in advance; non-urgent
- **emergency**: Urgent surgery that must be performed immediately
- **day_surgery**: Surgery where the patient is admitted and discharged on the same day
- **diagnostic**: Surgery performed primarily to clarify a diagnosis
- **therapeutic**: Surgery performed primarily for treatment
- **palliative**: Surgery that relieves symptoms but cannot cure the condition
- **reconstructive**: Surgery that rebuilds or restores function

## Anesthesia Type Classification

- **General anesthesia**: Using intravenous or inhaled anesthetic agents
- **Local anesthesia**: Anesthesia of a local area
- **Spinal / epidural anesthesia**: Includes spinal block and epidural anesthesia
- **Nerve block anesthesia**: Block of specific nerves
- **Monitored anesthesia care (MAC)**: Mild sedation

## Intelligent Extraction Rules

### Date Extraction

Priority:
1. Explicit date formats: 2024-08-15, August 15 2024, last August
2. Relative time: 3 months ago, last year, June this year
3. If unable to extract, ask the user

### Surgery Name Recognition

- Medical terms: e.g. "Laparoscopic appendectomy"
- Common names: e.g. "appendix removal", "gallbladder removal"
- Automatic matching: Build a mapping table of common surgery names

### Body Part Recognition

Common body part mapping:
- Abdominal surgery: abdomen, stomach, liver, gallbladder, etc.
- Orthopedic surgery: limbs, joints, spine, etc.
- Thoracic surgery: chest, heart, lungs, etc.
- Neurosurgery: head, brain, etc.
- ENT / Ophthalmology: ear, nose, throat, eyes, etc.

## Common Surgery Examples

```
# Example 1: Gallbladder surgery
/surgery had laparoscopic cholecystectomy on August 15 last year, due to chronic calculous cholecystitis

# Example 2: Fracture surgery
/surgery right tibia fracture internal fixation on March 10, 2024, car accident

# Example 3: Eye surgery
/surgery had laser eye surgery for myopia correction in June this year

# Example 4: Dental surgery
/surgery had a wisdom tooth extracted last month

# Example 5: Cardiac surgery
/surgery coronary artery stent placement in December 2023 for angina

# Example 6: Gynecologic surgery
/surgery uterine fibroid resection in May 2022
```

## Extended Fields

If the user provides more information, automatically extract and record:

- **Preoperative tests**: Important preoperative test results
- **Intraoperative findings**: Special findings or complications
- **Postoperative recovery**: Description of recovery
- **Pathology results**: If a pathology examination was performed
- **Follow-up plan**: Subsequent follow-up arrangements
- **Notes**: Any other important information

## Notes

- If key information is missing, proactively ask the user
- Standardize date format to YYYY-MM-DD
- Record surgery information as completely as possible
- Implant information is especially important; must be confirmed
- Keep data structured for easy future querying and analysis
- All data is stored locally only

## Data Querying

Surgery records can be queried using the `/query surgery` command:
- Query all surgery records
- Query by time range
- Query by body part
- Query by surgery name
