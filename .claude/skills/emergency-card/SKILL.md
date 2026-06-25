---
name: emergency-card
description: Generates a quick-access medical information summary card for emergencies. Use this skill when the user needs to travel, prepare for a medical visit, handle an emergency, or asks for "emergency information," "medical card," or "first aid information." Extracts key information (allergies, medications, acute conditions, implants), supports multiple output formats (JSON, text, QR code), for use in emergency care or quick medical access.
---

# Emergency Medical Information Card Generator

Generates a quick-access medical information summary for emergencies and medical visits.

## Core Features

### 1. Emergency Information Extraction
Extracts the most critical information from the user's health data:
- **Severe allergies**: Priority extraction of Grade 4 (anaphylaxis) and Grade 3 allergies
- **Current medications**: Name, dosage, and frequency of active drugs
- **Acute conditions**: Medical conditions requiring urgent attention
- **Implants**: Cardiac pacemakers, stents, etc. (affects examinations and treatments)
- **Emergency contacts**: Family member information for quick contact

### 2. Information Priority Sorting
Sorts information by medical urgency:
1. **P0 - Critical information**: Anaphylaxis, severe drug allergies, life-threatening conditions
2. **P1 - Important information**: Current medications, chronic diseases, implants
3. **P2 - General information**: Blood type, age, weight, recent tests

### 3. Multiple Output Formats
Supports multiple output formats for different scenarios:
- **HTML format**: Printable webpage using Tailwind CSS and Lucide icons (recommended)
- **JSON format**: Structured data for easy system integration
- **Text format**: Simple and readable, suitable for printing and carrying
- **PDF format**: Professional print quality, suitable for long-term storage

#### HTML Format (New)
Generates a standalone HTML file containing:
- Tailwind CSS styling (via CDN)
- Lucide icons (via CDN)
- Responsive design
- Print optimization
- Multiple size variants (A4, wallet card, large-print)
- Automatic card type detection (standard, child, elderly, severe allergy)

Usage:
```bash
# Generate standard card
python scripts/generate_emergency_card.py

# Specify card type
python scripts/generate_emergency_card.py standard
python scripts/generate_emergency_card.py child
python scripts/generate_emergency_card.py elderly
python scripts/generate_emergency_card.py severe

# Specify print size
python scripts/generate_emergency_card.py standard a4       # A4 standard
python scripts/generate_emergency_card.py standard wallet   # Wallet card
python scripts/generate_emergency_card.py standard large    # Large print (elderly)
```

Output file: `emergency-cards/emergency-card-{variant}-{YYYY-MM-DD}.html`

### 4. Offline Availability
- Supports saving to phone (photo album, files)
- Supports printed copies (wallet, bag)
- Supports cloud backup (optional)

## Usage Guide

### Trigger Conditions
Use this skill when the user mentions the following scenarios:
- ✅ "Generate an emergency medical information card"
- ✅ "I'm traveling next week, how do I quickly share my medical information"
- ✅ "Organize my allergy information into a card"
- ✅ "Emergency first aid information"
- ✅ "Prepare materials for a medical visit"
- ✅ "Medical information summary"

### Execution Steps

#### Step 1: Read User Basic Data
Read information from the following data sources:

```javascript
// 1. User profile
const profile = readFile('data/profile.json');

// 2. Allergy history
const allergies = readFile('data/allergies.json');

// 3. Current medications
const medications = readFile('data/medications/medications.json');

// 4. Radiation records
const radiation = readFile('data/radiation-records.json');

// 5. Surgery records (to find implants)
const surgeries = glob('data/surgery-records/**/*.json');

// 6. Discharge summaries (to find acute conditions)
const dischargeSummaries = glob('data/discharge-summaries/**/*.json');
```

#### Step 2: Extract Key Information

##### 2.1 Basic Information
```javascript
const basicInfo = {
  name: profile.basic_info?.name || "Not set",
  age: calculateAge(profile.basic_info?.birth_date),
  gender: profile.basic_info?.gender || "Not set",
  blood_type: profile.basic_info?.blood_type || "Unknown",
  weight: `${profile.basic_info?.weight} ${profile.basic_info?.weight_unit}`,
  height: `${profile.basic_info?.height} ${profile.basic_info?.height_unit}`,
  bmi: profile.calculated?.bmi,
  emergency_contacts: profile.emergency_contacts || []
};
```

#### 2.2 Severe Allergies
```javascript
// Filter for Grade 3-4 severe allergies
const criticalAllergies = allergies.allergies
  .filter(a => a.severity_level >= 3 && a.current_status.status === 'active')
  .map(a => ({
    allergen: a.allergen.name,
    severity: `Allergy ${getSeverityLabel(a.severity_level)} (Grade ${a.severity_level})`,
    reaction: a.reaction_description,
    diagnosed_date: a.diagnosis_date
  }));
```

#### 2.3 Chronic Disease Diagnoses (New)
```javascript
// Extract diagnosis information from chronic disease management data
const chronicConditions = [];

// Hypertension
try {
  const hypertensionData = readFile('data/hypertension-tracker.json');
  if (hypertensionData.hypertension_management?.diagnosis_date) {
    chronicConditions.push({
      condition: 'Hypertension',
      diagnosis_date: hypertensionData.hypertension_management.diagnosis_date,
      classification: hypertensionData.hypertension_management.classification,
      current_bp: hypertensionData.hypertension_management.average_bp,
      risk_level: hypertensionData.hypertension_management.cardiovascular_risk?.risk_level
    });
  }
} catch (e) {
  // File does not exist or read failed, skip
}

// Diabetes
try {
  const diabetesData = readFile('data/diabetes-tracker.json');
  if (diabetesData.diabetes_management?.diagnosis_date) {
    chronicConditions.push({
      condition: diabetesData.diabetes_management.type === 'type_1' ? 'Type 1 Diabetes' : 'Type 2 Diabetes',
      diagnosis_date: diabetesData.diabetes_management.diagnosis_date,
      duration_years: diabetesData.diabetes_management.duration_years,
      hba1c: diabetesData.diabetes_management.hba1c?.history?.[0]?.value,
      control_status: diabetesData.diabetes_management.hba1c?.achievement ? 'Well controlled' : 'Needs improvement'
    });
  }
} catch (e) {
  // File does not exist or read failed, skip
}

// COPD
try {
  const copdData = readFile('data/copd-tracker.json');
  if (copdData.copd_management?.diagnosis_date) {
    chronicConditions.push({
      condition: 'COPD (Chronic Obstructive Pulmonary Disease)',
      diagnosis_date: copdData.copd_management.diagnosis_date,
      gold_grade: `GOLD Grade ${copdData.copd_management.gold_grade}`,
      cat_score: copdData.copd_management.symptom_assessment?.cat_score?.total_score,
      exacerbations_last_year: copdData.copd_management.exacerbations?.last_year
    });
  }
} catch (e) {
  // File does not exist or read failed, skip
}
```

#### 2.4 Current Medications
```javascript
// Only include active medications
const currentMedications = medications.medications
  .filter(m => m.active === true)
  .map(m => ({
    name: m.name,
    dosage: `${m.dosage.value}${m.dosage.unit}`,
    frequency: getFrequencyLabel(m.frequency),
    instructions: m.instructions,
    warnings: m.warnings || []
  }));
```

##### 2.4 Medical Conditions
Extract diagnosis information from discharge summaries:
```javascript
const medicalConditions = dischargeSummaries
  .flatMap(ds => {
    const data = readFile(ds.file_path);
    return data.diagnoses || [];
  })
  .map(d => ({
    condition: d.condition,
    diagnosis_date: d.date,
    status: d.status || "Under follow-up"
  }));
```

##### 2.5 Implants
Extract implant information from surgery records:
```javascript
const implants = surgeries
  .flatMap(s => {
    const data = readFile(s.file_path);
    return data.procedure?.implants || [];
  })
  .map(i => ({
    type: i.type,
    implant_date: i.date,
    hospital: i.hospital,
    notes: i.notes
  }));
```

##### 2.6 Recent Radiation Exposure
```javascript
const recentRadiation = {
  total_dose_last_year: calculateTotalDose(radiation.records, 'last_year'),
  last_exam: radiation.records[radiation.records.length - 1]
};
```

#### Step 3: Generate Information Card

Organize information by priority:
```javascript
const emergencyCard = {
  version: "1.0",
  generated_at: new Date().toISOString(),
  basic_info: basicInfo,
  critical_allergies: criticalAllergies.sort(bySeverityDesc),
  current_medications: currentMedications,
  medical_conditions: [...medicalConditions, ...chronicConditions], // Merge acute and chronic conditions
  implants: implants,
  recent_radiation_exposure: recentRadiation,
  disclaimer: "This information card is for reference only and does not replace professional medical diagnosis",
  data_source: "my-his Personal Health Information System",
  chronic_conditions: chronicConditions // Separate field for easy access
};
```

#### Step 4: Format Output

##### JSON Format
Output structured JSON data directly.

##### Text Format
Generate a readable text card:
```
╔═══════════════════════════════════════════════════════════╗
║              EMERGENCY MEDICAL INFORMATION CARD           ║
╠═══════════════════════════════════════════════════════════╣
║ Name: Zhang San                   Age: 35                 ║
║ Blood Type: A+                    Weight: 70kg            ║
╠═══════════════════════════════════════════════════════════╣
║ 🆘 Severe Allergies                                       ║
║ ─────────────────────────────────────────────────────── ║
║ • Penicillin - Anaphylaxis (Grade 4) 🆘                  ║
║   Reaction: Difficulty breathing, laryngeal edema,        ║
║             loss of consciousness                         ║
╠═══════════════════════════════════════════════════════════╣
║ 💊 Current Medications                                    ║
║ ─────────────────────────────────────────────────────── ║
║ • Amlodipine 5mg - Once daily (Hypertension)             ║
║ • Metformin 1000mg - Twice daily (Diabetes)              ║
╠═══════════════════════════════════════════════════════════╣
║ 🏥 Chronic Diseases                                       ║
║ ─────────────────────────────────────────────────────── ║
║ • Hypertension (Diagnosed 2023-01-01, Grade 1,           ║
║   Under control)                                         ║
║   Average BP: 132/82 mmHg                                ║
║ • Type 2 Diabetes (Diagnosed 2022-05-10, HbA1c 6.8%)    ║
║   Control status: Good                                    ║
║ • COPD (Diagnosed 2020-03-15, GOLD Grade 2)              ║
║   CAT Score: 18                                          ║
╠═══════════════════════════════════════════════════════════╣
║ 🏥 Other Conditions                                       ║
║ ─────────────────────────────────────────────────────── ║
║ (Other acute or surgical diagnoses, if applicable)       ║
╠═══════════════════════════════════════════════════════════╣
║ 📿 Implants                                               ║
║ ─────────────────────────────────────────────────────── ║
║ • Cardiac pacemaker (Implanted 2022-06-10)               ║
║   Hospital: XX Hospital                                  ║
║   Note: Regular follow-up required, avoid MRI            ║
╠═══════════════════════════════════════════════════════════╣
║ 📞 Emergency Contacts                                     ║
║ ─────────────────────────────────────────────────────── ║
║ • Li Si (Spouse) - 138****1234                           ║
╠═══════════════════════════════════════════════════════════╣
║ ⚠️  Disclaimer                                           ║
║ This card is for reference only and does not replace      ║
║ professional medical diagnosis                            ║
║ Generated: 2025-12-31 12:34:56                            ║
╚═══════════════════════════════════════════════════════════╝
```

##### QR Code Format
Convert JSON data to a QR code image:
```javascript
const qrCode = generateQRCode(JSON.stringify(emergencyCard));
emergencyCard.qr_code = qrCode;
```

#### Step 5: Save Files

Save files in the user's chosen format:
```javascript
// JSON format
saveFile('emergency-card.json', JSON.stringify(emergencyCard, null, 2));

// Text format
saveFile('emergency-card.txt', generateTextCard(emergencyCard));

// QR code format
saveFile('emergency-card-qr.png', emergencyCard.qr_code);
```

#### Step 6: Output Confirmation

```
✅ Emergency Medical Information Card generated

File location: data/emergency-cards/emergency-card-2025-12-31.json
Generated at: 2025-12-31 12:34:56

Information included:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Basic information (name, age, blood type)
✓ Severe allergies (1 Grade 4 allergy)
✓ Current medications (2 drugs)
✓ Medical conditions (2 conditions)
✓ Implants (1 item)
✓ Emergency contacts (1 person)

💡 Usage recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Save JSON file to phone cloud storage
• Save QR code to phone photo album
• Print text version to carry with you
• Update information before travel

⚠️  Notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• This card is for reference only and does not replace professional medical diagnosis
• Update regularly (recommended every 3 months or when health information changes)
• If you have severe allergies, always carry an allergy emergency card
```

## Data Sources

### Primary Data Sources
- **data/profile.json**: User basic information, blood type, emergency contacts
- **data/allergies.json**: Allergy history and severity grading
- **data/medications/medications.json**: Current medication plan and dosages

### Chronic Disease Data Sources (New)
- **data/hypertension-tracker.json**: Hypertension management data (diagnosis date, classification, blood pressure control, target organ damage, cardiovascular risk)
- **data/diabetes-tracker.json**: Diabetes management data (type, HbA1c, blood glucose control, complication screening)
- **data/copd-tracker.json**: COPD management data (GOLD grading, CAT score, exacerbation history, lung function)

### Supplementary Data Sources
- **data/radiation-records.json**: Recent radiation exposure records
- **data/surgery-records/**/*.json**: Surgical implant information
- **data/discharge-summaries/**/*.json**: Medical diagnosis information

### Optional Data Sources
- **data/index.json**: Global data index

## Safety Principles

### Required Principles
- ❌ Do not add medication recommendations (only list current medications)
- ❌ Do not provide diagnostic conclusions (only list known diagnoses)
- ❌ Do not give treatment recommendations (do not substitute for a physician)
- ❌ Include a disclaimer (for reference only)

### Information Accuracy
- ✅ Only extract recorded information (do not speculate or infer)
- ✅ Label information source and update time
- ✅ Recommend regular information updates

### Privacy Protection
- ✅ Sensitive information can be optionally hidden
- ✅ Phone numbers partially masked (e.g., 138****1234)
- ✅ All data saved locally only

## Error Handling

### Missing Data
- **Allergy data missing**: Output "No allergy history recorded"
- **Medication data missing**: Output "No current medications recorded"
- **Implant data missing**: Output "No implants"

### File Read Failures
- **Cannot read profile.json**: Use default values (Name: Not set)
- **Cannot read allergies.json**: Skip allergy information
- **Continue generating other information**: Do not interrupt due to a single file failure

### QR Code Generation Failure
- Fall back to text format output
- Prompt user to manually record information

## Example Output

For complete examples, refer to [examples.md](examples.md).

## Test Data

Test data files are located at [test-data/emergency-example.json](test-data/emergency-example.json).

## Format Reference

For detailed output format descriptions, refer to [formats.md](formats.md).
