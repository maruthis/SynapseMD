---
description: Check and manage drug interactions
arguments:
  - name: action
    description: "Action type: check (check) / list (list rules) / add (add rule) / update (update rule) / delete (delete rule) / history (view history)"
    required: true
  - name: drugs
    description: Drug name or food name (for checking interactions of specific drugs, optional)
    required: false
---

# Drug Interaction Check

Detect and manage drug interactions, including four types: drug-drug, drug-disease, drug-dosage, and drug-food interactions, providing professional recommendations with five-level severity classification (A/B/C/D/X).

## Action Types

### 1. Check Interactions - `check`

Check for interactions in the current medication regimen.

**Parameter Description:**
- `drugs` (optional): Specify drugs to check, format: `drug1 drug2`; if not specified, checks all current medications

**Examples:**
```
/interaction check
/interaction check warfarin aspirin
/interaction check simvastatin amlodipine
```

**Check Content:**
- 🔄 Drug-drug interactions
- 🏥 Drug-disease conflicts
- 💊 Drug dosage conflicts
- 🍽️ Drug-food interactions

### 2. List Interaction Rules - `list`

View the interaction rule database.

**Parameter Description:**
- No parameters: List all rule statistics
- Level filter: `A`/`B`/`C`/`D`/`X` (list rules of a specific level)
- Drug name: List rules related to a specific drug

**Examples:**
```
/interaction list
/interaction list X
/interaction list warfarin
```

### 3. Add Interaction Rule - `add`

Add custom interaction rules.

**Parameter Description:**
- Rule information (required), format: `drug1 drug2 level(A/B/C/D/X) risk_description`

**Examples:**
```
/interaction add aspirin warfarin X significantly_increases_bleeding_risk
/interaction add metformin alcohol C increases_lactic_acidosis_risk
```

### 4. Update Interaction Rule - `update`

Update existing interaction rules.

**Parameter Description:**
- Rule information (required), format: `drug1 drug2 [field] [value]`

**Examples:**
```
/interaction update aspirin warfarin severity B
/interaction update warfarin vitamin_K recommendations keep_intake_stable
```

### 5. Delete Interaction Rule - `delete`

Delete custom interaction rules.

**Parameter Description:**
- Drug name (required), format: `drug1 drug2`

**Examples:**
```
/interaction delete aspirin warfarin
```

### 6. View Check History - `history`

View past interaction check records.

**Examples:**
```
/interaction history
/interaction history 2025-12
```

## Execution Steps

### Check Interactions (check)

#### 1. Load Current Medication List

Read all active medications (`active: true`) from `data/medications/medications.json`.

If no medication records, output prompt:
```
💡 Notice
No medication records yet, please use /medication add to add medications first
```

#### 2. Execute Four Detection Logic Types

##### 2.1 Drug-Drug Interaction Detection

**Detection Algorithm:**

```javascript
// Iterate through all drug combinations
for (let i = 0; i < medications.length; i++) {
  for (let j = i + 1; j < medications.length; j++) {
    const drug1 = medications[i];
    const drug2 = medications[j];

    // Check direct match (drug name)
    const directMatch = findInteraction(drug1.name, drug2.name);
    if (directMatch) {
      interactions.push({
        type: 'drug_drug',
        drugs: [drug1, drug2],
        rule: directMatch
      });
    }

    // Check category match
    const categoryMatch = findCategoryInteraction(drug1, drug2);
    if (categoryMatch) {
      interactions.push({
        type: 'category',
        drugs: [drug1, drug2],
        rule: categoryMatch
      });
    }
  }
}
```

**Match Rule Priority:**
1. Direct name match (drug generic name or brand name exactly the same)
2. Synonym match (considering drug aliases)
3. Category match (same class of drugs, such as multiple NSAIDs)
4. Mechanism match (drugs using the same metabolic enzyme)

##### 2.2 Drug-Disease Conflict Detection

**Data Sources:**
- `data/profile.json` - Disease history in user profile
- Diagnoses in discharge summary records
- Chronic disease information in symptom records

**Detection Logic:**
```javascript
for (const medication of medications) {
  for (const disease of userDiseases) {
    const conflict = findDrugDiseaseConflict(medication.name, disease.name);
    if (conflict) {
      conflicts.push({
        type: 'drug_disease',
        medication: medication,
        disease: disease,
        rule: conflict
      });
    }
  }
}
```

##### 2.3 Drug Dosage Conflict Detection

**Check Items:**
1. Whether daily dose exceeds maximum dose
2. Whether approaching warning threshold
3. Age-related dose adjustments (e.g., elderly may need reduced dose)
4. Renal function adjustment (e.g., dose reduction needed when creatinine clearance is low)

**Detection Logic:**
```javascript
for (const medication of medications) {
  const dosageRule = findDosageLimit(medication.name);
  if (!dosageRule) continue;

  // Calculate current daily dose
  const currentDose = calculateDailyDose(medication);

  // Check if exceeds maximum dose
  if (currentDose > dosageRule.max_daily_dose.value) {
    conflicts.push({
      type: 'exceeds_max_dose',
      medication: medication,
      current: currentDose,
      limit: dosageRule.max_daily_dose
    });
  }

  // Check age-related adjustments
  if (userAge >= 65 && dosageRule.adjustments?.elderly) {
    if (currentDose > dosageRule.adjustments.elderly.max_dose) {
      conflicts.push({
        type: 'age_specific_exceeds',
        medication: medication,
        age_group: 'Elderly (>65 years)',
        current: currentDose,
        limit: dosageRule.adjustments.elderly.max_dose
      });
    }
  }
}
```

##### 2.4 Drug-Food Interaction Detection

**Data Sources:**
- Get recent dietary records from `diet` command (last 7 days)

**Detection Logic:**
```javascript
// Get recent dietary records
const recentFoods = getRecentDietRecords(days: 7);

for (const medication of medications) {
  // Find known food interactions for this drug
  const foodInteractions = findFoodInteractions(medication.name);

  for (const interaction of foodInteractions) {
    // Check if user consumed related foods
    const consumed = checkFoodConsumption(recentFoods, interaction.food.examples);

    if (consumed && consumed.frequency >= 'moderate') {
      interactions.push({
        type: 'drug_food',
        medication: medication,
        food: interaction.food,
        consumed: consumed,
        rule: interaction
      });
    }
  }
}
```

#### 3. Aggregate and Sort Results

Sort all detected interactions by severity:
- 🆘 Class X (absolute contraindication) - Display first
- 🔴 Class D (contraindicated)
- 🟠 Class C (relative contraindication)
- 🟡 Class B (use with caution)
- 🟢 Class A (safe) - Usually not displayed

#### 4. Output Check Report

**Output Format:**

When no interactions:
```
✅ Drug Interaction Check

Check Time: December 31, 2025 12:34
━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Medications (3):
• Aspirin 100mg (once daily)
• Amlodipine 5mg (once daily)
• Metformin 500mg (three times daily)

Check Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No drug interactions detected
✅ No drug-disease conflicts detected
✅ No dosage issues detected
✅ No dietary conflicts detected

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Your medication regimen has good safety, please continue taking medications as directed
📅 Recommend performing an interaction check monthly

Check results saved
```

When serious interactions found:
```
🚨 Drug Interaction Check

Check Time: December 31, 2025 12:34
━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Medications (4):
• Warfarin 5mg (once daily)
• Aspirin 100mg (once daily)
• Amlodipine 5mg (once daily)
• Simvastatin 20mg (once nightly)

3 Interactions Detected:
━━━━━━━━━━━━━━━━━━━━━━━━━━

🆘 Absolute Contraindication (1)
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Warfarin + Aspirin
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Severity: 🆘 Absolute Contraindication (Class X)
   Risk Level: 5/5

   Issue Description:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Aspirin can enhance the anticoagulant effect of warfarin, significantly increasing bleeding risk.
   May cause serious bleeding, including intracranial hemorrhage, gastrointestinal bleeding, etc.

   Mechanism:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Aspirin inhibits platelet function, creating a synergistic effect with warfarin's anticoagulant action

   Clinical Impact:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Bleeding risk increases 3-5 times
   • Serious bleeding incidence: approximately 2-5%/year
   • Intracranial hemorrhage risk increases 50%

   Management Recommendations:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   🚫 Recommend avoiding concurrent use, unless:
      - There is a clear cardiovascular indication (e.g., atrial fibrillation + coronary artery disease)
      - Used under specialist physician supervision
      - Regular monitoring of coagulation function

   ⚠️ If concurrent use is necessary:
      • Closely monitor INR value (target value 2.0-3.0)
      • Watch for bleeding signs: bruising, gum bleeding, nosebleeds, black stools
      • Avoid injury and strenuous exercise
      • Regular blood count monitoring

   👁️ Situations requiring immediate medical attention:
      • Severe headache
      • Vomiting blood or black stools
      • Severe subcutaneous bruising
      • Blood in urine

   Data Source: FDA Drug Package Insert
   ━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Contraindicated (1)
━━━━━━━━━━━━━━━━━━━━━━━━━━

2. Simvastatin + Amlodipine
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Severity: 🔴 Contraindicated (Class D)
   Risk Level: 4/5

   Issue Description:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Amlodipine may inhibit simvastatin metabolism, increasing blood concentration,
   thereby increasing risk of muscle toxicity (myalgia, myositis, rhabdomyolysis).

   Increased Risks:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Rhabdomyolysis risk increases 2-3 times
   • Especially with high-dose simvastatin (>20mg)

   Management Recommendations:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   ⚠️ Recommend reducing simvastatin dose to below 20mg
   💪 If muscle pain or weakness occurs, seek immediate medical attention
   🩺 Regular monitoring of creatine kinase (CK) levels
   💡 Consider switching to a statin not metabolized through this pathway (e.g., rosuvastatin)

   Data Source: Clinical Pharmacology
   ━━━━━━━━━━━━━━━━━━━━━━━━━━

🟠 Relative Contraindication (1)
━━━━━━━━━━━━━━━━━━━━━━━━━━

3. Warfarin + Foods Rich in Vitamin K
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Severity: 🟠 Relative Contraindication (Class C)
   Risk Level: 3/5

   Issue Description:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Dietary records show you frequently consume spinach, broccoli, and other
   vitamin K-rich foods recently, which may reduce warfarin's anticoagulant effect.

   Dietary Analysis:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Spinach consumed in last 7 days: 3 times
   • Broccoli consumed in last 7 days: 2 times
   • Vitamin K intake: moderate to high

   Management Recommendations:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   🥗 Keep vitamin K intake stable, avoid drastic fluctuations
   🩺 If planning major dietary changes, inform your doctor
   📊 Regular INR monitoring
   💡 Consult a nutritionist for a balanced diet plan

   ━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary and Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🆘 1 absolute contraindication found, recommend consulting a doctor promptly
🔴 1 contraindication found, medication regimen adjustment needed
🟠 1 relative contraindication found, dietary management required

Action Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏥 Seek medical attention promptly: Discuss warfarin+aspirin concurrent use with prescribing doctor
💊 Medication adjustment: Consider reducing simvastatin dose or switching to another statin
🥗 Dietary management: Keep green vegetable intake stable
📅 Regular monitoring: Coagulation function, creatine kinase

━━━━━━━━━━━━━━━━━━━━━━━━━━
Check results saved, use /interaction history to view
⚠️ Important: This check is for reference only and cannot replace professional physician judgment
```

#### 5. Save Check Records

**File Path Format:**
`data/interactions/interaction-logs/YYYY-MM/YYYY-MM-DD.json`

**JSON Data Structure:**
```json
{
  "date": "2025-12-31",
  "check_time": "2025-12-31T12:34:56.789Z",
  "medications_count": 4,
  "medications": [
    {
      "id": "med_xxx",
      "name": "Warfarin",
      "dosage": "5mg",
      "frequency": "once daily"
    }
  ],
  "interactions_detected": {
    "total": 3,
    "by_severity": {
      "X": 1,
      "D": 1,
      "C": 1,
      "B": 0,
      "A": 0
    }
  },
  "interactions": [
    {
      "type": "drug_drug",
      "severity": "X",
      "drugs": ["Warfarin", "Aspirin"],
      "risk_description": "Significantly increases bleeding risk"
    }
  ],
  "recommendations": [
    "Seek medical attention promptly: Discuss warfarin+aspirin concurrent use with doctor",
    "Medication adjustment: Consider reducing simvastatin dose"
  ],
  "created_at": "2025-12-31T12:34:56.789Z"
}
```

### List Interaction Rules (list)

#### 1. Read Rule Database

Read all rules from `data/interactions/interaction-db.json`.

#### 2. Output Statistics

**Basic Output Format:**
```
📚 Drug Interaction Rule Database

Version: 1.0.0 | Last Updated: 2025-12-31
━━━━━━━━━━━━━━━━━━━━━━━━━━

Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Rules: 80
🟢 Class A (Safe): 10
🟡 Class B (Caution): 15
🟠 Class C (Relative Contraindication): 30
🔴 Class D (Contraindicated): 20
🆘 Class X (Absolute Contraindication): 5

By Type Distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Drug-drug interactions: 50
Drug-disease interactions: 15
Drug dosage conflicts: 8
Drug-food interactions: 7

🆘 Absolute Contraindication Rules (Class X):
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. MAO Inhibitors + SSRIs
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Risk: Serotonin syndrome (life-threatening)
   Mechanism: Excessive serotonin accumulation

2. Nitroglycerin + Sildenafil
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Risk: Severe hypotension
   Mechanism: Synergistic vasodilation

3. Warfarin + Aspirin
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Risk: Serious bleeding
   Mechanism: Enhanced anticoagulant effect

... (5 total)

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Use /interaction list [level] to view rules of a specific level
💡 Use /interaction list [drug name] to view rules for a specific drug
```

#### 3. Filtered Output

**Filter by Severity:**
```
/interaction list X

🆘 Absolute Contraindication Rules (Class X):
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Warfarin + Aspirin
   Risk: Serious bleeding
   Recommendation: Avoid concurrent use

2. MAO Inhibitors + SSRIs
   Risk: Serotonin syndrome
   Recommendation: Strictly prohibited

...
```

**Filter by Drug Name:**
```
/interaction list warfarin

📋 Warfarin-Related Interaction Rules
━━━━━━━━━━━━━━━━━━━━━━━━━━

🆘 Absolute Contraindication (1)
• Warfarin + Aspirin - Serious bleeding risk

🔴 Contraindicated (2)
• Warfarin + NSAIDs - Increased bleeding risk
• Warfarin + Garlic oil - May enhance anticoagulant effect

🟠 Relative Contraindication (2)
• Warfarin + Vitamin K-rich foods - Reduces anticoagulant effect
• Warfarin + St. John's Wort - Reduces anticoagulant effect

🟡 Use with Caution (1)
• Warfarin + Certain antibiotics - May enhance anticoagulant effect
```

### Add Interaction Rule (add)

#### 1. Parse Rule Information

Extract from natural language:
- Drug 1 name
- Drug 2 name
- Severity (A/B/C/D/X)
- Risk description

#### 2. Validate Input

- Check if severity level is valid
- Check if rule already exists
- Validate drug name format

#### 3. Create Rule Record

**JSON Data Structure:**
```json
{
  "id": "int_20251231123456789",
  "type": "drug_drug",
  "drugs": [
    {
      "name": "Drug 1",
      "category": "Category"
    },
    {
      "name": "Drug 2",
      "category": "Category"
    }
  ],
  "severity": {
    "level": "X",
    "level_name": "Absolute Contraindication",
    "level_code": 5,
    "color": "🆘"
  },
  "interaction_details": {
    "mechanism": "Mechanism of action",
    "effect": "Risk description",
    "clinical_impact": "Clinical impact"
  },
  "recommendations": [
    "Recommendation 1",
    "Recommendation 2"
  ],
  "active": true,
  "is_custom": true,
  "created_at": "2025-12-31T12:34:56.789Z"
}
```

#### 4. Save to Database

Add new rule to `data/interactions/interaction-db.json`

#### 5. Update Statistics

Update the `statistics` field in the database

#### 6. Output Confirmation

```
✅ Interaction Rule Added

Drug 1 + Drug 2
━━━━━━━━━━━━━━━━━━━━━━━━━━
Severity: 🆘 Absolute Contraindication (Class X)
Risk Description: Significantly increases bleeding risk

Data saved to: data/interactions/interaction-db.json
```

### Update Interaction Rule (update)

#### 1. Find Rule

Find existing rule by drug name

#### 2. Validate Rule Exists

Check if rule exists and if it is a custom rule

#### 3. Identify Update Field

Supported fields:
- `severity`: Severity level
- `recommendations`: Recommendations
- `notes`: Notes

#### 4. Update Rule Record

Update the value of the specified field

#### 5. Output Confirmation

```
✅ Interaction Rule Updated

Drug 1 + Drug 2
━━━━━━━━━━━━━━━━━━━━━━━━━━
Updated Field: severity
Original Value: Class D (Contraindicated)
New Value: Class C (Relative Contraindication)

Update Time: December 31, 2025 12:34
```

### Delete Interaction Rule (delete)

#### 1. Find Rule

Find rule by drug name

#### 2. Validate Deletability

- Preset rules (`is_custom: false`) cannot be deleted, only disabled
- Custom rules (`is_custom: true`) can be deleted

#### 3. Display Confirmation

```
⚠️ Confirm Deletion

About to delete interaction rule:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Drug 1 + Drug 2
Severity: Class X (Absolute Contraindication)

Cannot be recovered after deletion. Confirm?

A. Confirm deletion
B. Cancel
```

#### 4. Execute Deletion

Delete record after user confirmation, update statistics

#### 5. Output Confirmation

```
✅ Interaction Rule Deleted

Drug 1 + Drug 2
Deletion Time: December 31, 2025 12:34
```

### View Check History (history)

#### 1. Read Historical Records

Read historical summary from `data/interactions/interaction-history.json`

#### 2. Output History List

**Output Format:**
```
📋 Interaction Check History

━━━━━━━━━━━━━━━━━━━━━━━━━━
December 2025 (3 checks total)
━━━━━━━━━━━━━━━━━━━━━━━━━━

12-31 12:34  |  🚨 3 interactions found
           |  • 1 absolute contraindication (warfarin+aspirin)
           |  • 1 contraindication (simvastatin+amlodipine)
           |  • 1 relative contraindication (warfarin+vitamin K)

12-25 09:15  |  ✅ No interactions
           |  Medications at the time: 2

12-18 14:20  |  ⚠️ 1 interaction found
           |  • 1 relative contraindication (metformin+alcohol)

━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 3 checks | Average risk level: 🔴 High

Trend Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 Number of medications increased: 2 → 4
📊 Interaction risk: Increased
💡 Recommendation: With new medications added, recommend consulting a doctor for medication assessment

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Use /interaction check [date] to view detailed results of a specific check
```

## Five-Level Severity Classification Standard

| Level | Name | Code | Color | Definition | Management |
|------|------|------|------|------|----------|
| **A** | Safe | 1 | 🟢 | No significant interaction, can be used concurrently | No special measures needed |
| **B** | Use with Caution | 2 | 🟡 | Interaction exists but risk is low | Monitor, no adjustment needed |
| **C** | Relative Contraindication | 3 | 🟠 | Clinically significant interaction exists | Weigh benefits and risks, consider alternatives |
| **D** | Contraindicated | 4 | 🔴 | Serious interaction, risks outweigh benefits | Avoid concurrent use; requires monitoring in special cases |
| **X** | Absolute Contraindication | 5 | 🆘 | Life-threatening interaction | Strictly prohibited concurrent use |

### Determination Standards by Level

#### Class A - Safe (🟢)
- **Definition**: No significant drug interactions
- **Clinical significance**: Concurrent use will not cause adverse reactions or efficacy changes
- **Management**: No special measures required
- **Example**: Vitamin C + B-complex vitamins

#### Class B - Use with Caution (🟡)
- **Definition**: Minor interaction exists, but clinical risk is low
- **Clinical significance**: May require dose adjustment or timing arrangement, but can usually be used safely concurrently
- **Management**: Regularly monitor relevant indicators, watch for adverse reactions
- **Example**: Certain antibiotics + oral contraceptives (may reduce contraceptive efficacy)

#### Class C - Relative Contraindication (🟠)
- **Definition**: Clinically significant interaction exists
- **Clinical significance**: May cause increased adverse reactions or reduced efficacy
- **Management**: Carefully evaluate benefits and risks, consider alternative drugs
- **Example**: NSAIDs + ACEI/ARB (may reduce antihypertensive effect)

#### Class D - Contraindicated (🔴)
- **Definition**: Serious interaction, risks clearly outweigh benefits
- **Clinical significance**: May cause serious adverse reactions or treatment failure
- **Management**: Generally avoid concurrent use; if necessary, requires specialist physician approval and close monitoring
- **Example**: Aspirin + Warfarin (significantly increases bleeding risk)

#### Class X - Absolute Contraindication (🆘)
- **Definition**: Life-threatening interaction
- **Clinical significance**: Concurrent use may lead to fatal consequences
- **Management**: Strictly prohibited concurrent use
- **Example**: MAO inhibitors + SSRIs (serotonin syndrome)

## Integration with Other Commands

### Integration with medication command

**Location**: `add` action of medication.md command

**Integration Point**: After step 3 "Check drug allergies", add step 4 "Check drug interactions"

**Check Process**:
1. Read current medication list
2. Execute interaction detection
3. Sort by severity and display warnings
4. User chooses to continue adding/cancel adding

**Integration Example**:
```markdown
#### 4. Check Drug Interactions (New)

Before saving medication information, check for interactions with current medications.

**Check Steps**:

1. **Load current medications**: Read all active medications from `data/medications/medications.json`
2. **Execute interaction detection**: Call four detection logic types
3. **Aggregate results**: Generate interaction report
4. **Display warnings**: Display by severity level

**Output Format**:
```
🔍 Drug Interaction Check

2 potential interactions detected:

━━━━━━━━━━━━━━━━━━━━━━━━━━
🆘 Absolute Contraindication (Class X)
• Warfarin + Aspirin
  Risk: Significantly increases bleeding risk
  Recommendation: Avoid concurrent use, use under physician monitoring

Continue adding this medication?
A. I understand the risks, continue adding (requires physician confirmation)
B. Cancel adding, consult physician
```
```

### Integration with diet command

Retrieve data from `/diet` command dietary records for drug-food interaction detection

### Integration with profile command

Retrieve disease history, age, renal function, and other information from user profile for drug-disease conflict and dosage adjustment detection

## Data Structure Update

Add to global index `data/index.json`:

```json
{
  "interaction_db": "data/interactions/interaction-db.json",
  "interaction_logs": "data/interactions/interaction-logs",
  "statistics": {
    "last_check": null,
    "last_check_date": null,
    "total_checks": 0
  }
}
```

## Notes

1. **Medical disclaimer**: All check results are for reference only and cannot replace professional medical advice
2. **Data accuracy**: Preset database needs regular updates and maintenance
3. **User experience**: Warning information should be clear without causing excessive panic
4. **Privacy protection**: All data is stored locally only, not uploaded to the cloud
5. **Regular checks**: Recommend monthly interaction checks, especially after adding new medications

## Example Usage

```
# Check interactions for current medications
/interaction check

# Check interactions for specific drugs
/interaction check warfarin aspirin

# List all interaction rules
/interaction list

# List absolute contraindication rules
/interaction list X

# Add custom interaction rule
/interaction add aspirin warfarin X significantly_increases_bleeding_risk

# Update rule
/interaction update aspirin warfarin severity D

# Delete custom rule
/interaction delete aspirin warfarin

# View check history
/interaction history
```

## Error Handling

- **No medication records**: "No medication records yet, please use /medication add to add medications first"
- **Rule not found**: "Interaction rule not found"
- **Invalid severity level**: "Severity must be A, B, C, D, or X"
- **Cannot delete preset rule**: "Preset rules cannot be deleted, please use the update command for adjustments"
- **Database not initialized**: "Interaction database not initialized, creating..."
