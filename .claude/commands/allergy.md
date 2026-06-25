---
description: Manage allergy history records
arguments:
  - name: action
    description: "Action type: add/list/update/delete"
    required: true
  - name: info
    description: Allergy information (allergen, severity, reaction symptoms, etc., natural language description)
    required: false
---

# Allergy History Management

Record and manage allergy history, including drug allergies, food allergies, environmental allergies, etc., with support for quick search and updates.

## Action Types

### 1. Add Allergy Record - `add`

Add a new allergy record.

**Parameter Description:**
- `info`: Allergy information (required), described in natural language

**Examples:**
```
/allergy add penicillin severe allergy as a child had breathing difficulty after injection
/allergy add peanut moderate allergy lips swell after eating
/allergy add pollen mild sneezing runny nose
/allergy add iodine contrast agent severe shock during CT scan
/allergy add bee sting anaphylactic shock whole body rash throat swelling
```

**Supported Description Formats:**
- Allergen name + severity + reaction symptoms + discovery circumstances
- Allergen name can be: drug name, food name, environmental factor, etc.
- Severity keywords: mild, slight, moderate, severe, shock, anaphylactic shock
- Reaction symptoms: rash, difficulty breathing, throat swelling, nausea, vomiting, etc.

### 2. View Allergy Records - `list`

View all allergy records with filter support.

**Parameter Description:**
- No parameters: show all allergies
- `active`: show active allergies only
- `drug`: show drug allergies only
- `food`: show food allergies only
- `severe`: show allergies with severity of severe and above only

**Examples:**
```
/allergy list
/allergy list active
/allergy list drug
/allergy list severe
```

### 3. Update Allergy Record - `update`

Update an existing allergy record.

**Parameter Description:**
- `info`: Update information (required), format: allergen name + fields and values to update

**Examples:**
```
/allergy update penicillin severity moderate
/allergy update peanut status resolved
/allergy update penicillin notes still need to avoid
/allergy update peanut
```

**Supported Fields:**
- `severity`: Severity level (mild/moderate/severe/anaphylaxis)
- `status`: Current status (active/resolved)
- `notes`: Notes

### 4. Delete Allergy Record - `delete`

Delete an allergy record.

**Parameter Description:**
- `info`: Allergen name (required)

**Examples:**
```
/allergy delete penicillin
/allergy delete peanut
```

## Execution Steps

### Add Allergy Record (add)

#### 1. Parse Allergy Information

Extract from natural language:

**Basic Information (auto-extracted):**
- **Allergen Name**: The specific substance causing the allergy
- **Allergy Type**: Drug, food, environmental, other
- **Severity**: Mild, moderate, severe, anaphylactic shock
- **Reaction Symptoms**: Specific allergic reaction manifestations

**Detailed Information (extracted or asked):**
- **Discovery Time**: When the allergy was first discovered
- **Discovery Circumstances**: The situation and background at the time
- **Confirmation Method**: Doctor diagnosis, self-observation, test confirmation
- **Current Status**: Still allergic or resolved

#### 2. Medical Standardization Conversion

Convert colloquial descriptions to standard medical terminology:

| Colloquial Description | Medical Term | Type |
|---------|---------|------|
| Penicillin, Pen G | Penicillin | Drug Allergy |
| Peanut, nuts | Peanut | Food Allergy |
| Pollen, catkins | Pollen | Environmental Allergy |
| Iodine contrast agent, CT contrast | Iodine contrast agent | Drug Allergy |
| Bee sting, wasp sting | Hymenoptera venom | Other Allergy |

#### 3. Allergy Type Classification

Classified by category:

- **Drug Allergies**: Antibiotics (penicillin, cephalosporin, etc.), pain medications (aspirin, etc.), contrast agents, vaccines, herbal medicine, etc.
- **Food Allergies**: Seafood (shrimp, crab, shellfish), nuts (peanut, walnut), eggs, dairy products, gluten, fruits, etc.
- **Environmental Allergies**: Pollen, dust mites, animal hair, mold, latex, etc.
- **Other Allergies**: Insect stings, chemicals, metals, etc.

#### 4. Severity Assessment

**Mild (Level 1):**
- Localized skin reactions (mild rash, itching)
- Does not affect general condition
- No emergency treatment needed

**Moderate (Level 2):**
- Significant discomfort (obvious rash, nausea, mild breathing difficulty)
- Needs treatment but no life-threatening risk
- Recommended to see a doctor

**Severe (Level 3):**
- Severe reactions (serious breathing difficulty, generalized urticaria, blood pressure drop)
- Requires medical intervention
- Must see a doctor

**Anaphylactic Shock (Level 4):**
- Life-threatening systemic allergic reaction
- Shock, throat swelling, loss of consciousness
- Requires emergency treatment

#### 5. Automatic Severity Assessment

**Keyword Mapping:**
- "shock", "anaphylactic shock", "loss of consciousness", "coma" → Level 4 (anaphylactic shock)
- "severe", "systemic", "unbearable", "blood pressure drop" → Level 3 (severe)
- "obvious", "moderate", "needs treatment", "swelling" → Level 2 (moderate)
- "mild", "slight", "occasional", "localized" → Level 1 (mild)

#### 6. Reaction Symptom Identification

**Skin Symptoms:**
- Rash, urticaria, itching, redness and swelling, erythema

**Respiratory Symptoms:**
- Difficulty breathing, wheezing, throat swelling, chest tightness

**Digestive Symptoms:**
- Nausea, vomiting, diarrhea, abdominal pain

**Systemic Symptoms:**
- Shock, blood pressure drop, fainting, loss of consciousness, generalized urticaria

#### 7. Save Allergy Record

**File Path Format:**
`data/allergies.json`

**JSON Data Structure:**
```json
{
  "allergies": [
    {
      "id": "allergy_20251231123456789",
      "allergen": {
        "name": "Penicillin",
        "type": "drug",
        "type_category": "Drug Allergy",
        "synonyms": ["Penicillin", "Pen G"]
      },
      "severity": {
        "level": "severe",
        "level_code": 3,
        "description": "Severe allergic reaction"
      },
      "reactions": [
        {
          "reaction": "Rash",
          "onset_time": "Within 30 minutes of exposure",
          "severity": "Moderate"
        },
        {
          "reaction": "Difficulty breathing",
          "onset_time": "15 minutes after exposure",
          "severity": "Severe"
        }
      ],
      "discovery": {
        "date": "2010-05-15",
        "age_at_discovery": "8 years old",
        "circumstances": "Occurred after penicillin injection during pneumonia treatment"
      },
      "confirmation": {
        "method": "doctor_confirmed",
        "method_name": "Doctor diagnosis",
        "confirmed_by": "XX Hospital Pediatrics",
        "test_results": null
      },
      "current_status": {
        "status": "active",
        "status_name": "Active",
        "last_occurrence": "2020-03-10",
        "resolved_date": null
      },
      "management": {
        "avoidance_strategy": "Strictly avoid using penicillin-class drugs",
        "emergency_plan": "If accidentally used, seek medical attention immediately, carry allergy information",
        "carries_epipen": false,
        "medical_alert": true
      },
      "notes": "Must proactively inform medical staff at every medical visit",
      "metadata": {
        "created_at": "2025-12-31T12:34:56.789Z",
        "last_updated": "2025-12-31T12:34:56.789Z"
      }
    }
  ],
  "statistics": {
    "total_allergies": 5,
    "active_allergies": 4,
    "drug_allergies": 2,
    "food_allergies": 1,
    "environmental_allergies": 1,
    "other_allergies": 1,
    "severe_count": 2,
    "anaphylaxis_count": 1,
    "last_updated": "2025-12-31T12:34:56.789Z"
  }
}
```

#### 8. Output Confirmation

```
✅ Allergy record added

Allergen Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Allergen: Penicillin
Type: Drug Allergy
Severity: 🔴 Severe (Level 3)

Allergic Reactions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Rash - Moderate, within 30 minutes of exposure
• Difficulty breathing - Severe, 15 minutes after exposure

Discovery Circumstances:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Discovery Date: 2010-05-15 (age 8)
Confirmation Method: Doctor diagnosis
Circumstances: Occurred after injection during pneumonia treatment

Management Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Must inform medical staff at every visit
🚫 Strictly avoid using penicillin-class drugs
🆔 Recommend wearing a medical alert identification

Data saved to: data/allergies.json
```

### View Allergy Records (list)

**Output Format:**
```
📋 Allergy History List

━━━━━━━━━━━━━━━━━━━━━━━━━━
5 allergy records total (4 active)

Drug Allergies (2):
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Penicillin 🔴 Severe
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Reactions: Rash, difficulty breathing
   Discovered: 2010-05-15 (Doctor diagnosis)
   Status: Active ⚠️

2. Iodine Contrast Agent 🟠 Severe
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Reactions: Generalized urticaria, blood pressure drop
   Discovered: 2018-03-20 (Doctor diagnosis)
   Status: Active ⚠️

Food Allergies (1):
━━━━━━━━━━━━━━━━━━━━━━━━━━

3. Peanut 🟡 Moderate
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Reactions: Lip swelling, nausea
   Discovered: 2015-08-10 (Self-observation)
   Status: Active ⚠️

Environmental Allergies (1):
━━━━━━━━━━━━━━━━━━━━━━━━━━

4. Pollen 🟢 Mild
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Reactions: Sneezing, runny nose, itchy eyes
   Discovered: 2019-03-01 (Test confirmed)
   Status: Active

Other Allergies (1):
━━━━━━━━━━━━━━━━━━━━━━━━━━

5. Bee Sting 🔴 Anaphylactic Shock
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Reactions: Generalized urticaria, throat swelling, loss of consciousness
   Discovered: 2012-07-22 (Doctor diagnosis)
   Status: Active 🆘 Carrying epinephrine pen

━━━━━━━━━━━━━━━━━━━━━━━━━━
Legend: 🟢 Mild 🟡 Moderate 🟠 Severe 🔴 Critical 🆘 Shock

Important Reminder:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• 2 severe allergy records, must proactively inform medical staff during visits
• 1 anaphylactic shock record, need to carry emergency medications
```

**Filtered Output Example:**

Drug allergies only:
```
📋 Drug Allergy List

━━━━━━━━━━━━━━━━━━━━━━━━━━
2 drug allergy records total

1. Penicillin 🔴 Severe
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Reactions: Rash, difficulty breathing
   Discovered: 2010-05-15

2. Iodine Contrast Agent 🟠 Severe
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Reactions: Generalized urticaria, blood pressure drop
   Discovered: 2018-03-20
```

Severe allergies only:
```
📋 Severe Allergy List

━━━━━━━━━━━━━━━━━━━━━━━━━━
3 severe allergy records total

⚠️ The following allergies may be life-threatening, must proactively inform medical staff:

1. Penicillin 🔴 Severe
2. Iodine Contrast Agent 🟠 Severe
3. Bee Sting 🆘 Anaphylactic Shock
```

### Update Allergy Record (update)

#### 1. Find Allergy Record

Find existing record by allergen name.

#### 2. Identify Update Fields

**Supported Fields:**
- `severity`: Severity level (mild/moderate/severe/anaphylaxis)
- `status`: Current status (active/resolved)
- `notes`: Notes

#### 3. Interactive Update

If only the allergen name is provided, enter interactive update mode:
```
📝 Update Allergy Record: Penicillin

Current Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Severity: Severe (Level 3)
Status: Active

Select field to update:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Severity
2. Current Status
3. Reaction Symptoms
4. Management Strategy
5. Notes

Enter option number (1-5):
```

#### 4. Output Confirmation

```
✅ Allergy record updated

Allergen: Penicillin
Updated Field: Severity
Previous Value: Severe (Level 3)
New Value: Moderate (Level 2)

Update Time: 2025-12-31 12:34
```

### Delete Allergy Record (delete)

#### 1. Find Allergy Record

Find the record to delete by allergen name.

#### 2. Display Confirmation

```
⚠️ Confirm Deletion

About to delete allergy record:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Allergen: Penicillin
Severity: Severe (Level 3)
Discovery Date: 2010-05-15

This cannot be undone. Confirm?

A. Confirm Delete
B. Cancel
```

#### 3. Execute Deletion

Delete record after user confirmation, update statistics.

#### 4. Output Confirmation

```
✅ Allergy record deleted

Allergen: Penicillin
Deletion Time: 2025-12-31 12:34
```

## Intelligent Recognition Rules

### Allergen Name Recognition

**Common Drug Allergens:**
- Antibiotics: Penicillin, cephalosporin, erythromycin, amoxicillin, ampicillin, etc.
- Pain medications: Aspirin, ibuprofen, diclofenac sodium, etc.
- Contrast agents: Iodine contrast agent, gadolinium contrast agent, etc.
- Vaccines: Influenza vaccine, hepatitis B vaccine, etc.

**Common Food Allergens:**
- Seafood: Shrimp, crab, shellfish, abalone, etc.
- Nuts: Peanut, walnut, almond, cashew, etc.
- Other: Eggs, milk, sesame, mango, pineapple, etc.

**Common Environmental Allergens:**
- Pollen: Pollen, catkins, plane tree fluff, etc.
- Animals: Cat hair, dog hair, feathers, etc.
- Other: Dust mites, mold, latex, etc.

### Severity Recognition

| Keywords | Severity | Level |
|--------|---------|------|
| Shock, anaphylactic shock, loss of consciousness, coma | Anaphylactic Shock | 4 |
| Severe, systemic, blood pressure drop, unbearable | Severe | 3 |
| Obvious, moderate, swelling, needs treatment | Moderate | 2 |
| Mild, slight, localized, occasional | Mild | 1 |

### Reaction Symptom Recognition

**Skin Symptoms:**
Rash, urticaria, itching, redness and swelling, erythema, swelling

**Respiratory Symptoms:**
Difficulty breathing, wheezing, throat swelling, chest tightness, shortness of breath

**Digestive Symptoms:**
Nausea, vomiting, diarrhea, abdominal pain, bloating

**Systemic Symptoms:**
Shock, blood pressure drop, fainting, loss of consciousness, systemic reactions

### Confirmation Method Recognition

**Doctor Diagnosis:**
Doctor diagnosis, hospital diagnosis, doctor confirmation

**Self-Observation:**
Self-discovered, self-observation, experienced it

**Test Confirmed:**
Skin test, blood test, allergen test, test confirmed

## Data Structure Update

Add to global index `data/index.json`:

```json
{
  "allergy_records": "data/allergies.json",
  "statistics": {
    "allergy_count": 5
  }
}
```

## Integration with Medication Command

When using `/medication add` to add a medication, the system automatically checks allergy records:

**Check Logic:**
1. Parse drug name, extract generic name and drug class
2. Check if related allergies exist in `data/allergies.json`
3. For drug allergies, check drug family relationships:
   - Penicillin class: penicillin, amoxicillin, ampicillin, mezlocillin, etc.
   - Cephalosporin class: cefazolin, cefixime, ceftriaxone, etc.
   - Sulfonamide class: sulfamethoxazole, sulfadiazine, etc.
4. If potential allergy is found, display warning

**Warning Output:**
```
⚠️ Allergy Warning

Detected that you may be allergic to the following drug:

• Penicillin - Severe allergy
  Drug being added: Amoxicillin (belongs to penicillin class)

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. If confirmed not allergic, can continue adding
2. If uncertain, recommend consulting a doctor or pharmacist
3. Please carefully check drug ingredients

Continue adding?
A. Continue Adding
B. Cancel
```

## Integration with Visit Preparation Command

When using the `/prepare` command, allergy information is automatically displayed:

**Output Example:**
```
Your Health Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Allergy History Key Reminders (3 records):
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Penicillin - Severe allergy (must inform)
🔴 Iodine contrast agent - Severe allergy (remind before examination)
🆘 Bee sting - Anaphylactic shock (carry emergency medication)

Visit Preparation Checklist:
━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ ID/Health insurance card (required)
☐ Allergy history list (required) ⭐
☐ Medication list or currently taking medications
☐ Allergy emergency medications (if carrying) ⭐
☐ Previous examination reports
```

## Notes

- This system is for allergy record purposes only and cannot replace professional medical diagnosis
- Patients with severe allergies and anaphylactic shock should carry emergency medications and medical alert identification at all times
- Must proactively inform medical staff of allergy history at every medical visit
- Regularly update allergy records to document new allergies or resolved allergies
- All data is stored locally only

## Example Usage

```
# Add severe drug allergy
/allergy add penicillin severe allergy as a child had breathing difficulty after injection

# Add anaphylactic shock
/allergy add bee sting anaphylactic shock whole body rash throat swelling loss of consciousness

# Add food allergy
/allergy add peanut moderate allergy lips swell nausea after eating

# Add environmental allergy
/allergy add pollen mild sneezing runny nose itchy eyes

# List all allergies
/allergy list

# List drug allergies only
/allergy list drug

# List severe allergies only
/allergy list severe

# Update severity
/allergy update penicillin severity moderate

# Mark as resolved
/allergy update peanut status resolved

# Delete allergy record
/allergy delete peanut
```

## Error Handling

- **Empty allergy information**: "Please provide allergy information, e.g.: /allergy add penicillin severe allergy"
- **Allergen already exists**: "This allergen already exists, please use /allergy update to update the record"
- **Allergen not found**: "No record found for this allergen"
- **Cannot identify severity**: "Cannot identify severity, please specify clearly (mild/moderate/severe/anaphylactic shock)"
- **Cannot identify allergy type**: "Cannot identify allergy type, please provide more detailed information"
- **No allergy records**: "No allergy records yet"
- **Deletion cancelled**: "Deletion cancelled"
- **Storage failure**: "Failed to save record, please check storage space"
