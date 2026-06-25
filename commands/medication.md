---
description: Manage medication plans and record medication intake
arguments:
  - name: action
    description: "Action type: add (add medication) / log (record medication intake) / history (medication history) / status (medication statistics) / list (medication list)"
    required: true
  - name: info
    description: Medication information (drug name, dosage, usage, etc., in natural language)
    required: false
---

# Medication Record Management

Manage medications and medication schedules, record daily medication intake, and track medication adherence.

## Action Types

### 1. Add Medication - `add`

Add a new medication and its medication schedule.

**Parameter description:**
- `info`: Medication information (required), described in natural language

**Examples:**
```
/medication add aspirin 100mg once daily after breakfast
/medication add amlodipine 5mg once each morning and evening
/medication add metformin 500mg three times daily after meals
/medication add vitamin D 1000IU once weekly
```

**Supported description formats:**
- Drug name + dosage + frequency + timing
- Frequency keywords: daily, every day, weekly, every other day, as needed
- Timing keywords: before breakfast, after breakfast, before lunch, after lunch, before dinner, after dinner, at bedtime, once each morning and evening, etc.

### 2. Record Medication Intake - `log`

Record actual medication intake.

**Parameter description:**
- `info`: Medication log (required), described in natural language

**Examples:**
```
/medication log took aspirin
/medication log aspirin taken
/medication log forgot amlodipine
/medication log amlodipine missed
/medication log aspirin taken at 8am
```

**Automatic recognition:**
- ✅ Took, taken, had, used — normal medication intake
- ❌ Forgot, missed, not taken — missed dose record
- ⏰ Planned — scheduled reminder

### 3. View Medication List - `list`

View all added medications and medication schedules.

**Examples:**
```
/medication list
```

### 4. View Medication History - `history`

View medication record history.

**Examples:**
```
/medication history
/medication history today
/medication history 2025-12-31
/medication history week
```

### 5. View Medication Statistics - `status`

View medication adherence statistics.

**Examples:**
```
/medication status
/medication status today
/medication status week
/medication status month
```

## Execution Steps

### Add Medication (add)

#### 1. Parse Medication Information

Extract from natural language:
- **Drug name**: generic name or brand name
- **Dosage**: value + unit (mg, g, ml, IU, tablet, capsule, etc.)
- **Frequency**: number of times per day, per week, etc.
- **Timing**: specific time points for taking the medication
- **Special instructions**: before meals, after meals, at bedtime, etc.

#### 2. Generate Medication Schedule

**Core rule: The schedule array must explicitly generate medication schedule records for every day of the week (1–7)**

**Frequency mapping rules:**

| User input | Frequency type | Schedule records | Generation rule |
|-----------|---------------|-----------------|-----------------|
| Once daily, 1 time per day | daily | 7 entries | 1 per day, Monday to Sunday |
| Twice daily, 2 times per day, once each morning and evening | daily | 14 entries | 2 per day, Monday to Sunday |
| Three times daily, 3 times per day | daily | 21 entries | 3 per day, Monday to Sunday |
| Once weekly | weekly | 1 entry | Only the specified weekday |
| Every other day | every_other_day | 4 entries | Mon, Wed, Fri, Sun or Tue, Thu, Sat |
| As needed | as_needed | 0 entries | No fixed schedule |

**Schedule generation algorithm:**

```javascript
// Pseudocode example
function generateSchedule(frequency, times, timeSlots) {
  const schedule = [];

  if (frequency === 'daily') {
    // N times per day: generate N records for each of the 7 days of the week
    for (let weekday = 1; weekday <= 7; weekday++) {
      for (const timeSlot of timeSlots) {
        schedule.push({
          weekday: weekday,
          time: timeSlot.time,
          timing_label: timeSlot.label,
          dose: {
            value: timeSlot.dose.value,
            unit: timeSlot.dose.unit
          }
        });
      }
    }
  } else if (frequency === 'weekly') {
    // Once weekly: generate only 1 record (default Monday, or user-specified day)
    schedule.push({
      weekday: 1,  // or user-specified weekday
      time: timeSlots[0].time,
      timing_label: timeSlots[0].label,
      dose: {
        value: timeSlots[0].dose.value,
        unit: timeSlots[0].dose.unit
      }
    });
  } else if (frequency === 'every_other_day') {
    // Every other day: generate 4 records (1, 3, 5, 7 or 2, 4, 6)
    const days = [1, 3, 5, 7];  // or [2, 4, 6]
    for (const weekday of days) {
      schedule.push({
        weekday: weekday,
        time: timeSlots[0].time,
        timing_label: timeSlots[0].label,
        dose: {
          value: timeSlots[0].dose.value,
          unit: timeSlots[0].dose.unit
        }
      });
    }
  }

  return schedule;
}
```

**Generation examples:**

**Once daily:**
```
Input: once daily after breakfast
Generated: 7 records
- Monday 08:00 after breakfast
- Tuesday 08:00 after breakfast
- Wednesday 08:00 after breakfast
- Thursday 08:00 after breakfast
- Friday 08:00 after breakfast
- Saturday 08:00 after breakfast
- Sunday 08:00 after breakfast
```

**Twice daily:**
```
Input: twice daily, once each morning and evening
Generated: 14 records
- Monday 08:00 morning
- Monday 20:00 evening
- Tuesday 08:00 morning
- Tuesday 20:00 evening
- ... (continuing to Sunday)
```

**Three times daily:**
```
Input: three times daily after meals
Generated: 21 records
- Monday 08:00 after breakfast
- Monday 12:30 after lunch
- Monday 18:30 after dinner
- Tuesday 08:00 after breakfast
- ... (continuing to Sunday)
```

**Time mapping rules:**

| User input | Standard time | Note |
|-----------|--------------|-------|
| Before breakfast, before meals (morning) | 07:00 | Adjustable in personal settings |
| After breakfast, after meals (morning) | 08:00 | Adjustable in personal settings |
| Before lunch | 11:30 | Adjustable in personal settings |
| After lunch | 12:30 | Adjustable in personal settings |
| Before dinner | 17:30 | Adjustable in personal settings |
| After dinner | 18:30 | Adjustable in personal settings |
| At bedtime | 21:00 | Adjustable in personal settings |
| Morning and evening | 08:00, 20:00 | Two doses |

#### 3. Check Drug Allergies

**Important: Before saving medication information, check whether the user has relevant allergies.**

**Check process:**

1. **Parse drug class**: Identify the drug family from the drug name
2. **Read allergy records**: Check allergy records in `data/allergies.json`
3. **Match allergens**: Check whether the drug or its class is on the allergy list
4. **Display warnings**: If a potential allergy is found, display a warning and request confirmation

**Common drug family mappings:**

| Drug class | Included drugs |
|-----------|---------------|
| Penicillins | Penicillin, Amoxicillin, Ampicillin, Mezlocillin, Piperacillin, etc. |
| Cephalosporins | Cefazolin, Cefixime, Ceftriaxone, Cefuroxime, Ceftazidime, etc. |
| Sulfonamides | Sulfamethoxazole, Sulfadiazine, Sulfadimidine, etc. |
| Tetracyclines | Tetracycline, Doxycycline, Minocycline, etc. |
| Aminoglycosides | Gentamicin, Amikacin, Streptomycin, etc. |
| Macrolides | Erythromycin, Azithromycin, Clarithromycin, etc. |
| Iodinated contrast agents | Iohexol, Iopamidol, Ioversol, etc. |
| NSAIDs | Aspirin, Ibuprofen, Diclofenac sodium, Celecoxib, etc. |

**Allergy check logic:**

```javascript
// Pseudocode example
function checkDrugAllergy(drugName) {
  // 1. Read allergy records
  const allergies = loadAllergies('data/allergies.json');

  // 2. Filter active drug allergies
  const drugAllergies = allergies.allergies.filter(a =>
    a.allergen.type === 'drug' &&
    a.current_status.status === 'active'
  );

  // 3. Check direct match (exact drug name match)
  const directMatch = drugAllergies.find(a =>
    a.allergen.name === drugName ||
    a.allergen.synonyms.includes(drugName)
  );

  if (directMatch) {
    return {
      hasAllergy: true,
      allergy: directMatch,
      matchType: 'direct'
    };
  }

  // 4. Check drug family match
  const drugFamily = getDrugFamily(drugName);
  if (drugFamily) {
    const familyMatch = drugAllergies.find(a =>
      drugFamily.allergens.includes(a.allergen.name)
    );

    if (familyMatch) {
      return {
        hasAllergy: true,
        allergy: familyMatch,
        matchType: 'family',
        familyName: drugFamily.name
      };
    }
  }

  return { hasAllergy: false };
}
```

**Warning output format:**

```
⚠️ Allergy Warning

A potential drug allergy has been detected:

• Penicillin — Severe allergy (Grade 3)
  Drug being added: Amoxicillin (belongs to the penicillin class)
  Allergic reactions: rash, difficulty breathing

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. If confirmed not allergic, you may proceed to add
2. If unsure, consult a doctor or pharmacist
3. Carefully check the drug's ingredients
4. Consider allergy testing for confirmation

Would you like to continue adding this medication?
A. Continue adding (I confirm I am not allergic)
B. Cancel adding
```

**Special warning (anaphylactic shock):**

If an anaphylactic shock-level allergy is detected, use a stronger warning:

```
🚨 Severe Allergy Warning

A history of anaphylactic shock to this medication has been detected!

• Penicillin — Anaphylactic shock (Grade 4) 🆘
  Drug being added: Amoxicillin (belongs to the penicillin class)
  Allergic reactions: difficulty breathing, laryngeal edema, loss of consciousness

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Warning: Anaphylactic shock can be life-threatening!

Strongly recommended:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Stop adding this medication immediately
2. Consult a doctor or pharmacist
3. Under no circumstances take this risk

Would you like to continue?
A. Force continue (not recommended)
B. Cancel adding (recommended)
```

**Handling process:**

- User selects A: Continue adding the medication, save medication information
- User selects B: Cancel adding, do not save medication information

#### 4. Check Pregnancy Drug Safety

**Important: Before saving medication information, check whether the user is pregnant and the drug's safety during pregnancy.**

**Check process:**

1. **Check pregnancy status**: Read `data/pregnancy-tracker.json` to check for an active pregnancy
2. **Query drug pregnancy category**: Query the drug's pregnancy category (A/B/C/D/X) from the drug database
3. **Display warnings**: If the drug is Category D/X or has pregnancy contraindications, display a warning

**Drug categories during pregnancy (FDA):**

| Category | Description | Risk | Definition |
|---------|-------------|------|------------|
| A | Safe | Lowest | Controlled studies show no risk |
| B | Relatively safe | Low | Animal studies show no risk; no controlled human studies |
| C | Use with caution | Moderate | Animal studies show risk; human studies lacking |
| D | Contraindicated (benefit > risk) | High | Evidence of risk, but may be used in certain situations |
| X | Absolutely contraindicated | Highest | Contraindicated during pregnancy or in women who may become pregnant |

**Common drug pregnancy categories:**

| Drug class | Drug example | Category | Use during pregnancy |
|-----------|-------------|----------|---------------------|
| **Analgesics/Antipyretics** |
| Acetaminophen | Tylenol | B | ✅ Safe (preferred) |
| Aspirin | Aspirin | C/D | ⚠️ Use with caution (low dose may be used) |
| Ibuprofen | Ibuprofen | B/D | ⚠️ Contraindicated in third trimester |
| Diclofenac | Diclofenac | B/D | ⚠️ Contraindicated in third trimester |
| **Antibiotics** |
| Penicillins | Amoxicillin | B | ✅ Relatively safe |
| Cephalosporins | Cefixime | B | ✅ Relatively safe |
| Erythromycin | Erythromycin | B | ✅ Relatively safe |
| Clindamycin | Clindamycin | B | ✅ Relatively safe |
| Tetracyclines | Doxycycline | D | ❌ Contraindicated (affects fetal bones/teeth) |
| Fluoroquinolones | Levofloxacin | C | ⚠️ Avoid use |
| **Cardiovascular drugs** |
| Antihypertensive | Labetalol | C | ✅ Can be used (commonly used in pregnancy) |
| Antihypertensive | Methyldopa | B | ✅ Can be used |
| Antihypertensive | ACE inhibitors/ARBs | C/D | ❌ Contraindicated (teratogenic) |
| **Anticoagulants** |
| Warfarin | Warfarin | D/X | ❌ Contraindicated (teratogenic) |
| Heparin | Heparin | B | ✅ Can be used |
| **Antidepressants** |
| SSRIs | Sertraline | C | ⚠️ Weigh risks and benefits |
| SSRIs | Paroxetine | D | ⚠️ Avoid in third trimester |
| **Antihistamines** |
| Loratadine | Claritin | B | ✅ Relatively safe |
| Cetirizine | Zyrtec | B | ✅ Relatively safe |
| **Vitamins / Supplements** |
| Folic acid | Folic Acid | A | ✅ Recommended |
| Vitamin D | Vitamin D | A/B | ✅ Safe (in appropriate amounts) |
| Vitamin A | Vitamin A | A/X | ⚠️ Category X in high doses |
| Iron | Iron | C/B | ✅ Recommended in second and third trimesters |

**Pregnancy safety check logic:**

```javascript
// Pseudocode example
function checkPregnancySafety(drugName) {
  // 1. Check if pregnant
  const pregnancy = loadPregnancy('data/pregnancy-tracker.json');

  if (!pregnancy.current_pregnancy) {
    return { is_pregnant: false };
  }

  const gestationalWeek = pregnancy.current_pregnancy.current_week;
  const trimester = pregnancy.current_pregnancy.current_trimester;

  // 2. Query drug pregnancy category
  const pregnancyCategory = getDrugPregnancyCategory(drugName);

  // 3. Assess risk based on category and gestational week
  if (pregnancyCategory === 'X') {
    return {
      is_pregnant: true,
      pregnancyCategory: 'X',
      risk: 'contraindicated',
      recommendation: 'do_not_use',
      message: 'This drug is contraindicated during pregnancy'
    };
  }

  if (pregnancyCategory === 'D') {
    return {
      is_pregnant: true,
      pregnancyCategory: 'D',
      risk: 'high',
      recommendation: 'consult_doctor',
      message: 'This drug carries high risk during pregnancy and must be used under physician guidance'
    };
  }

  if (pregnancyCategory === 'C') {
    return {
      is_pregnant: true,
      pregnancyCategory: 'C',
      risk: 'moderate',
      recommendation: 'use_with_caution',
      message: 'This drug should be used with caution during pregnancy; weigh risks and benefits'
    };
  }

  // Category A or B
  return {
    is_pregnant: true,
    pregnancyCategory: pregnancyCategory,
    risk: 'low',
    recommendation: 'generally_safe',
    message: 'This drug is relatively safe during pregnancy'
  };
}
```

**Warning output format (Category X — absolutely contraindicated):**

```
🚨 Pregnancy Drug Safety Warning

Pregnancy has been detected!
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current gestational week: 12 weeks (first trimester)

Drug being added: Isotretinoin
Pregnancy category: X (absolutely contraindicated)

Risk information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Category X drugs have been proven teratogenic to the fetus,
and are contraindicated during pregnancy or in women who may become pregnant.

Isotretinoin risks:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Severe birth defects (craniofacial, cardiac, thymic)
• Central nervous system abnormalities
• Increased risk of miscarriage

⚠️ Prohibited!
━━━━━━━━━━━━━━━━━━━━━━━━━━
Isotretinoin and similar drugs must not be used during pregnancy.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Stop adding this drug immediately
❌ If already taking it, stop immediately and seek medical attention
❌ Consult a dermatologist to find an alternative

❌ If already taken, consult your prenatal physician immediately
   and undergo necessary prenatal diagnostics

Would you like to continue?
━━━━━━━━━━━━━━━━━━━━━━━━━━
A. Cancel adding (strongly recommended)
B. I have consulted a doctor and still want to add (not recommended)

⚠️ Important note:
This system's recommendation is based on medical guidelines. For final medication decisions,
always follow the professional advice of your prenatal physician!
```

**Warning output format (Category D — high risk):**

```
⚠️ Pregnancy Drug Safety Warning

Pregnancy has been detected!
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current gestational week: 28 weeks (third trimester)

Drug being added: ACE inhibitor (e.g., Enalapril)
Pregnancy category: D

Risk information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Category D drugs have evidence of fetal harm,
but in certain situations (e.g., benefit to the mother),
they may be used cautiously after physician evaluation.

ACE inhibitor risks:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Fetal renal impairment
• Oligohydramnios
• Fetal growth restriction
• Neonatal renal abnormalities

⚠️ Physician evaluation required!
━━━━━━━━━━━━━━━━━━━━━━━━━━
ACE inhibitors are generally contraindicated during pregnancy,
unless a physician determines that maternal benefit outweighs the risk.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🏥 Consult your prenatal physician immediately
❌ Do not use without physician approval
❌ Your doctor may suggest switching to a safer
   antihypertensive (e.g., labetalol) for pregnancy

Would you like to continue?
━━━━━━━━━━━━━━━━━━━━━━━━━━
A. Cancel adding (recommended)
B. Physician has evaluated; continue use

⚠️ Important note:
Please use this type of medication only under the guidance of your prenatal physician!
```

**Warning output format (Category C — moderate risk):**

```
⚠️ Pregnancy Drug Safety Notice

Pregnancy has been detected!
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current gestational week: 20 weeks (second trimester)

Drug being added: Fluconazole
Pregnancy category: C

Risk information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Category C drugs: Animal studies show risk,
but controlled human studies are lacking.
Maternal benefit must be weighed against potential risk.

Fluconazole risks:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Animal studies show risk at high doses
• Limited human data
• Single low-dose risk may be lower
• Higher risk with prolonged or high-dose use

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Use under physician guidance
✅ Weigh treatment need against potential risk
✅ Use the lowest effective dose
✅ Minimize duration of use

Would you like to continue?
━━━━━━━━━━━━━━━━━━━━━━━━━━
A. Physician has evaluated; continue use
B. Cancel adding; consult physician
C. View more information

⚠️ Note:
If unsure, please consult a doctor or pharmacist first.
```

**Safe output format (Category A/B — relatively safe):**

```
✅ Pregnancy Drug Safety Check

Pregnancy has been detected!
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current gestational week: 16 weeks (second trimester)

Drug being added: Penicillin V potassium
Pregnancy category: B

Safety assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This drug is relatively safe during pregnancy ✅

Penicillin-class antibiotics:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Category B drug: no risk in animal studies
• Long history of human use; good safety profile
• One of the preferred drugs for treating infections during pregnancy

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Use as directed by your physician
✅ Follow the prescribed dosage strictly
✅ Complete the full course
✅ Seek medical attention promptly if adverse reactions occur

💡 Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Even though this is a relatively safe drug,
it should still be used under physician guidance.
```

**Special notice (first / third trimester):**

```
📅 Special Pregnancy Notice

Current gestational week: 12 weeks (first trimester)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Organ development period — the most sensitive stage

⚠️ First trimester special note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
The first trimester (weeks 1–13) is the critical period
for fetal organ development and is most sensitive to external factors.

✅ Relatively safe recommended drugs:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Fever / Pain: Acetaminophen (Category B)
• Antibiotics: Penicillins, Cephalosporins (Category B)
• Allergies: Loratadine, Cetirizine (Category B)

❌ Drugs to avoid:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Tetracyclines (affect bones / teeth)
• Fluoroquinolones (affect cartilage)
• ACE inhibitors / ARBs (teratogenic)
• Warfarin (teratogenic)
• Isotretinoin (severely teratogenic)

💡 Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Medication use in the first trimester requires extra caution.
Please consult your prenatal physician before taking any medication!
```

**Handling process:**

- Category X/D drugs: Cancel adding by default; user must confirm "physician has evaluated"
- Category C drugs: Display risk information; user chooses
- Category A/B drugs: Indicate relatively safe, but physician guidance still required

#### 5. Check Drug Interactions

**Important: Before saving medication information, check interactions with current medications.**

**Check process:**

1. **Load current medications**: Read all active medications (`active: true`) from `data/medications/medications.json`
2. **Perform interaction detection**:
   - Drug–drug interaction detection
   - Drug–disease conflict detection
   - Drug dosage conflict detection
   - Drug–food interaction detection
3. **Summarize results**: Generate interaction report
4. **Display warnings**: Show by severity level

**Detection logic:**

**4.1 Drug–Drug Interactions**

```javascript
// Pseudocode example
function checkDrugDrugInteractions(newDrug, currentMedications) {
  const interactions = [];

  // Iterate through all current medications
  for (const medication of currentMedications) {
    // Find interaction rules in the database
    const rule = findInteractionInDB(newDrug.name, medication.name);

    if (rule) {
      interactions.push({
        type: 'drug_drug',
        drug1: newDrug.name,
        drug2: medication.name,
        rule: rule
      });
    }
  }

  // Sort by severity (X > D > C > B > A)
  return interactions.sort((a, b) => b.rule.severity.level_code - a.rule.severity.level_code);
}
```

**4.2 Drug–Disease Conflicts**

Read the user's disease history from `data/profile.json` and check whether the drug has disease contraindications.

**4.3 Drug Dosage Conflicts**

Check whether the dosage exceeds the maximum daily dose, taking into account age and renal function adjustments.

**4.4 Drug–Food Interactions**

Read recent dietary records from the `diet` command and check drug–food interactions.

**Warning output format:**

```
🔍 Drug Interaction Check

2 potential interactions detected:

━━━━━━━━━━━━━━━━━━━━━━━━━━
🆘 Absolute Contraindication (Category X)

• Warfarin + Aspirin
  Current medication: Warfarin 5 mg
  Drug being added: Aspirin 100 mg

  Risk: Significantly increased bleeding risk
  Mechanism: Aspirin can enhance warfarin's anticoagulant effect

  Recommendations:
  ━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚫 Avoid co-administration unless there is a clear indication and physician monitoring
  ⚠️ If co-administration is necessary, monitor coagulation function closely
  👁️ Patient should watch for signs of bleeding (bruising, gum bleeding, black stools, etc.)

━━━━━━━━━━━━━━━━━━━━━━━━━━
🟠 Relative Contraindication (Category C)

• Warfarin + Vitamin K-rich foods
  Current medication: Warfarin 5 mg
  Dietary records: Recently consuming spinach and broccoli frequently

  Risk: Reduced anticoagulant effect of warfarin
  Mechanism: Vitamin K is a cofactor required for coagulation factor synthesis

  Recommendations:
  ━━━━━━━━━━━━━━━━━━━━━━━━━━
  🥗 Maintain stable vitamin K intake
  📊 Avoid drastic fluctuations in dietary vitamin K content
  🩺 Inform your doctor if you increase green vegetable intake

━━━━━━━━━━━━━━━━━━━━━━━━━━
Would you like to continue adding this medication?

A. I understand the risks; continue adding (physician confirmation required)
B. Cancel adding; consult physician
C. View more detailed information
```

**Handling process:**

- User selects A: Continue adding the medication, save medication information
- User selects B: Cancel adding, do not save medication information
- User selects C: Display complete interaction details

**When no interactions are found:**

```
✅ Drug Interaction Check

━━━━━━━━━━━━━━━━━━━━━━━━━━
No interactions with current medications detected

Check results:
• ✅ No drug–drug interactions
• ✅ No drug–disease conflicts
• ✅ No dosage issues
• ✅ No dietary conflicts

This medication can be safely added
```

**Saving warning tags:**

If the user chooses to continue adding despite serious interactions (Category D or X), add a warning tag in the medication record:

```json
{
  "id": "med_20251231123456789",
  "name": "Aspirin",
  "warnings": [
    {
      "type": "drug_interaction",
      "severity": "X",
      "description": "Absolute contraindication with Warfarin",
      "date_identified": "2025-12-31T12:34:56.789Z"
    }
  ],
  "active": true,
  ...
}
```

#### 5. Save Medication Information

**File path format:**
`data/medications/medications.json`

**JSON data structure:**
```json
{
  "medications": [
    {
      "id": "med_20251231123456789",
      "name": "Aspirin",
      "generic_name": "Aspirin",
      "dosage": {
        "value": 100,
        "unit": "mg"
      },
      "frequency": {
        "type": "daily",
        "times_per_day": 1,
        "interval_days": 1
      },
      "schedule": [
        {
          "weekday": 1,
          "time": "08:00",
          "timing_label": "after breakfast",
          "dose": {
            "value": 100,
            "unit": "mg"
          }
        },
        {
          "weekday": 2,
          "time": "08:00",
          "timing_label": "after breakfast",
          "dose": {
            "value": 100,
            "unit": "mg"
          }
        },
        {
          "weekday": 3,
          "time": "08:00",
          "timing_label": "after breakfast",
          "dose": {
            "value": 100,
            "unit": "mg"
          }
        },
        {
          "weekday": 4,
          "time": "08:00",
          "timing_label": "after breakfast",
          "dose": {
            "value": 100,
            "unit": "mg"
          }
        },
        {
          "weekday": 5,
          "time": "08:00",
          "timing_label": "after breakfast",
          "dose": {
            "value": 100,
            "unit": "mg"
          }
        },
        {
          "weekday": 6,
          "time": "08:00",
          "timing_label": "after breakfast",
          "dose": {
            "value": 100,
            "unit": "mg"
          }
        },
        {
          "weekday": 7,
          "time": "08:00",
          "timing_label": "after breakfast",
          "dose": {
            "value": 100,
            "unit": "mg"
          }
        }
      ],
      "instructions": "Take after breakfast",
      "notes": "",
      "active": true,
      "created_at": "2025-12-31T12:34:56.789Z",
      "last_updated": "2025-12-31T12:34:56.789Z"
    }
  ]
}
```

**Multiple-dose example (twice daily):**
```json
{
  "id": "med_20251231123456790",
  "name": "Amlodipine",
  "dosage": {
    "value": 5,
    "unit": "mg"
  },
  "frequency": {
    "type": "daily",
    "times_per_day": 2,
    "interval_days": 1
  },
  "schedule": [
    {
      "weekday": 1,
      "time": "08:00",
      "timing_label": "morning",
      "dose": {
        "value": 5,
        "unit": "mg"
      }
    },
    {
      "weekday": 1,
      "time": "20:00",
      "timing_label": "evening",
      "dose": {
        "value": 5,
        "unit": "mg"
      }
    },
    {
      "weekday": 2,
      "time": "08:00",
      "timing_label": "morning",
      "dose": {
        "value": 5,
        "unit": "mg"
      }
    },
    {
      "weekday": 2,
      "time": "20:00",
      "timing_label": "evening",
      "dose": {
        "value": 5,
        "unit": "mg"
      }
    },
    {
      "weekday": 3,
      "time": "08:00",
      "timing_label": "morning",
      "dose": {
        "value": 5,
        "unit": "mg"
      }
    },
    {
      "weekday": 3,
      "time": "20:00",
      "timing_label": "evening",
      "dose": {
        "value": 5,
        "unit": "mg"
      }
    }
    ... (continuing to Sunday, 14 records total)
  ],
  "instructions": "Take once each morning and evening",
  "active": true,
  "created_at": "2025-12-31T12:34:56.789Z",
  "last_updated": "2025-12-31T12:34:56.789Z"
}
```

**Once weekly example:**
```json
{
  "id": "med_20251231123456791",
  "name": "Vitamin D",
  "dosage": {
    "value": 1000,
    "unit": "IU"
  },
  "frequency": {
    "type": "weekly",
    "times_per_day": 1,
    "interval_days": 7
  },
  "schedule": [
    {
      "weekday": 1,
      "time": "08:00",
      "timing_label": "Monday morning",
      "dose": {
        "value": 1000,
        "unit": "IU"
      }
    }
  ],
  "instructions": "Take every Monday morning",
  "active": true,
  "created_at": "2025-12-31T12:34:56.789Z",
  "last_updated": "2025-12-31T12:34:56.789Z"
}
```

**Every other day example:**
```json
{
  "id": "med_20251231123456792",
  "name": "Some medication",
  "dosage": {
    "value": 50,
    "unit": "mg"
  },
  "frequency": {
    "type": "every_other_day",
    "times_per_day": 1,
    "interval_days": 2
  },
  "schedule": [
    {
      "weekday": 1,
      "time": "08:00",
      "timing_label": "morning",
      "dose": {
        "value": 50,
        "unit": "mg"
      }
    },
    {
      "weekday": 3,
      "time": "08:00",
      "timing_label": "morning",
      "dose": {
        "value": 50,
        "unit": "mg"
      }
    },
    {
      "weekday": 5,
      "time": "08:00",
      "timing_label": "morning",
      "dose": {
        "value": 50,
        "unit": "mg"
      }
    },
    {
      "weekday": 7,
      "time": "08:00",
      "timing_label": "morning",
      "dose": {
        "value": 50,
        "unit": "mg"
      }
    }
  ],
  "instructions": "Take every other day (Mon, Wed, Fri, Sun)",
  "active": true,
  "created_at": "2025-12-31T12:34:56.789Z",
  "last_updated": "2025-12-31T12:34:56.789Z"
}
```

#### 5. Output Confirmation

```
✅ Medication Added

Medication information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Drug name: Aspirin
Single dose: 100 mg
Frequency: 1 time daily

Medication schedule:
━━━━━━━━━━━━━━━━━━━━━━━━━━
☀️ After breakfast (08:00) — 100 mg

Instructions: Take after breakfast
━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Tip: Use /medication log took aspirin to record medication intake
```

### Record Medication Intake (log)

#### 1. Identify Medication Status

Recognize from natural language:
- **Taken normally**: took, taken, had, used, administered
- **Missed**: forgot, missed, did not take, skipped
- **Time information**: today, yesterday, specific time (8am, 2pm, etc.)

#### 2. Save Medication Log

**File path format:**
`data/medication-logs/YYYY-MM/YYYY-MM-DD.json`

**JSON data structure:**
```json
{
  "date": "2025-12-31",
  "logs": [
    {
      "id": "log_20251231080000001",
      "medication_id": "med_20251231123456789",
      "medication_name": "Aspirin",
      "scheduled_time": "08:00",
      "actual_time": "2025-12-31T08:15:00",
      "status": "taken",
      "dose": {
        "value": 100,
        "unit": "mg"
      },
      "notes": "",
      "created_at": "2025-12-31T08:15:00.000Z"
    }
  ]
}
```

**Missed dose record example:**
```json
{
  "id": "log_20251231200000002",
  "medication_id": "med_20251231123456790",
  "medication_name": "Amlodipine",
  "scheduled_time": "20:00",
  "actual_time": null,
  "status": "missed",
  "dose": {
    "value": 5,
    "unit": "mg"
  },
  "notes": "Forgot to take",
  "created_at": "2025-12-31T22:00:00.000Z"
}
```

**Status values:**
- `taken`: Taken
- `missed`: Missed dose
- `skipped`: Skipped (physician order to stop)
- `delayed`: Taken late

#### 3. Output Confirmation

**Normal medication intake:**
```
✅ Medication log added

Drug: Aspirin 100 mg
Scheduled time: 08:00 (after breakfast)
Actual time: today 08:15
Status: ✅ Taken
```

**Missed dose record:**
```
⚠️ Missed dose recorded

Drug: Amlodipine 5 mg
Scheduled time: 20:00 (evening)
Status: ❌ Missed

💡 Recommendation: If less than 2 hours have passed since the scheduled time, you may take it now. If more than 2 hours have passed, skip this dose and continue with the original schedule.
```

### View Medication List (list)

**Output format:**
```
💊 My Medication List

Current medications (3):
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Aspirin — 100 mg
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Once daily, after breakfast
   Medication schedule (7 times per week):
   Monday 08:00 (after breakfast) — 100 mg
   Tuesday 08:00 (after breakfast) — 100 mg
   Wednesday 08:00 (after breakfast) — 100 mg
   Thursday 08:00 (after breakfast) — 100 mg
   Friday 08:00 (after breakfast) — 100 mg
   Saturday 08:00 (after breakfast) — 100 mg
   Sunday 08:00 (after breakfast) — 100 mg

2. Amlodipine — 5 mg
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Twice daily, morning and evening
   Medication schedule (14 times per week):
   Monday 08:00 (morning) — 5 mg
   Monday 20:00 (evening) — 5 mg
   Tuesday 08:00 (morning) — 5 mg
   Tuesday 20:00 (evening) — 5 mg
   ... (same for Wednesday to Sunday)

3. Metformin — 500 mg
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Three times daily, after meals
   Medication schedule (21 times per week):
   Monday 08:00 (after breakfast) — 500 mg
   Monday 12:30 (after lunch) — 500 mg
   Monday 18:30 (after dinner) — 500 mg
   Tuesday 08:00 (after breakfast) — 500 mg
   Tuesday 12:30 (after lunch) — 500 mg
   Tuesday 18:30 (after dinner) — 500 mg
   ... (same for Wednesday to Sunday)

Discontinued (1):
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Vitamin C (discontinued 2025-12-15)
```

### View Medication History (history)

**Today's history output format:**
```
📋 Today's Medication Log

December 31, 2025
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Aspirin 100 mg
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Scheduled: 08:00 (after breakfast)
   Actual: 08:15 ✅

✅ Amlodipine 5 mg
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Scheduled: 08:00 (morning)
   Actual: 08:10 ✅

⏰ Metformin 500 mg
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Scheduled: 12:30 (after lunch)
   Status: Pending

✅ Amlodipine 5 mg
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Scheduled: 20:00 (evening)
   Actual: 20:05 ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━
Today's plan: 4 doses
Taken: 3 doses
Pending: 1 dose
Missed: 0 doses
```

**Weekly history output format:**
```
📋 This Week's Medication Log

2025-12-25 to 2025-12-31
━━━━━━━━━━━━━━━━━━━━━━━━━━

Aspirin 100 mg (once daily)
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ✅ ✅ ✅ ✅ ✅ ⏰
Adherence: 85.7% (6/7)

Amlodipine 5 mg (twice daily)
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅✅ ✅✅ ❌⏰ ✅✅ ✅✅ ✅✅ ✅⏰
Adherence: 78.6% (11/14)

Legend: ✅ Taken  ❌ Missed  ⏰ Pending
```

### View Medication Statistics (status)

**Output format:**
```
📊 Medication Adherence Statistics

Period: This week (2025-12-25 to 2025-12-31)
━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Planned doses: 28
Actual doses taken: 24
Missed doses: 3
Pending: 1

Adherence: 85.7% ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━

By medication:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Aspirin 100 mg
  ━━━━━━━━━━━━━━━━━━━━━━━━━━
  Planned: 7  |  Taken: 6  |  Missed: 0
  Adherence: 100% ✅
  This week's performance: Excellent

Amlodipine 5 mg
  ━━━━━━━━━━━━━━━━━━━━━━━━━━
  Planned: 14  |  Taken: 11  |  Missed: 2
  Adherence: 78.6% ⚠️
  This week's performance: Good, needs improvement

Metformin 500 mg
  ━━━━━━━━━━━━━━━━━━━━━━━━━━
  Planned: 7  |  Taken: 7  |  Missed: 0
  Adherence: 100% ✅
  This week's performance: Excellent

Adherence evaluation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Excellent: ≥ 90% (2 medications)
⚠️ Good: 70–89% (1 medication)
❌ Needs improvement: < 70% (0 medications)

💡 Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Amlodipine missed 2 doses; consider setting a medication reminder
• Morning medication adherence is good
• Evening medications occasionally missed; consider preparing them before bedtime

Monthly trend:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 1: 82.1%
Week 2: 87.5%
Week 3: 89.3%
This week: 85.7%
Trend: 📈 Steady improvement
```

## Intelligent Recognition Rules

### Drug Name Recognition

**Common drug class examples:**
- Antihypertensives: Amlodipine, Nifedipine, Irbesartan, etc.
- Antidiabetics: Metformin, Glimepiride, Insulin, etc.
- Cardiovascular drugs: Aspirin, Clopidogrel, Statins, etc.
- Vitamins: Vitamin D, B vitamins, Vitamin C, etc.
- Supplements: Calcium, Fish oil, Probiotics, etc.

### Dosage Recognition

**Supported units:**
- Weight units: mg, g, μg (micrograms)
- Volume units: ml, L
- International units: IU
- Count units: tablet, capsule, sachet, bag, vial, bottle, drop

**Extraction rules:**
- Number + unit: 100mg, 5ml, 2 tablets, 1 capsule
- Written numbers: one tablet, two capsules, three sachets

### Frequency Recognition

| User input | Standardized | Times/day |
|-----------|-------------|-----------|
| Once daily, 1 time per day | daily | 1 |
| Twice daily, 2 times per day, once each morning and evening | daily | 2 |
| Three times daily, 3 times per day, after meals (three times) | daily | 3 |
| Four times daily, 4 times per day | daily | 4 |
| Once weekly | weekly | 0.14 |
| Twice weekly | weekly | 0.29 |
| Every other day | every_other_day | 0.5 |
| As needed, when necessary | as_needed | 0 |

### Timing Recognition

| User input | Standard time | Period |
|-----------|--------------|--------|
| Before breakfast, before meals (morning), upon waking | 07:00 | Morning |
| After breakfast, after meals (morning) | 08:00 | Morning |
| Before lunch | 11:30 | Noon |
| After lunch | 12:30 | Noon |
| Before dinner | 17:30 | Evening |
| After dinner | 18:30 | Evening |
| At bedtime | 21:00 | Night |
| Upon waking, in the morning | 07:00 | Morning |
| Morning | 08:00 | Morning |
| Noon, afternoon | 12:00 | Noon |
| Evening, nighttime | 20:00 | Evening |

### Medication Status Recognition

**Taken keywords:**
- took, taken, had, used, administered
- done, completed, on time

**Missed keywords:**
- forgot, missed, did not take, skipped, didn't take
- missed dose, not on time

## Data Structure Update

Add to the global index `data/index.json`:

```json
{
  "medications": [
    {
      "id": "med_20251231123456789",
      "name": "Aspirin",
      "dosage_value": 100,
      "dosage_unit": "mg",
      "frequency_type": "daily",
      "file_path": "data/medications/medications.json",
      "active": true,
      "created_at": "2025-12-31T12:34:56.789Z"
    }
  ],
  "medication_logs": [
    {
      "id": "log_20251231080000001",
      "date": "2025-12-31",
      "medication_id": "med_20251231123456789",
      "medication_name": "Aspirin",
      "status": "taken",
      "file_path": "data/medication-logs/2025-12/2025-12-31.json"
    }
  ]
}
```

## Medication Adherence Calculation

**Adherence percentage = (actual doses taken / planned doses) × 100%**

**Adherence levels:**
- ✅ **Excellent**: ≥ 90%
- ⚠️ **Good**: 70% – 89%
- ❌ **Needs improvement**: < 70%

**Notes:**
- Pending doses are not included in statistics
- Physician-ordered discontinuations are not counted as missed doses
- As-needed medications are not included in adherence calculations

## Missed Dose Handling Recommendations

**Missed dose handling rules:**

1. **Discovered promptly (< 2 hours after scheduled time)**
   - Recommend taking immediately
   - Record as "taken late" status

2. **Discovered late (≥ 2 hours after scheduled time)**
   - Generally recommend skipping this dose
   - Continue with the original schedule for the next dose
   - Record as "missed" status

3. **Special medications require physician guidance**
   - Some medications (e.g., oral contraceptives) have special missed-dose rules
   - Consult a doctor or pharmacist

## Notes

- This system is for personal medication record-keeping only and cannot replace professional medical advice
- Verify drug name and dosage are accurate before adding
- If in doubt, consult a doctor or pharmacist
- Regularly update the medication list; deactivate discontinued medications
- All data is stored locally only
- Share important medication records with your doctor

## Example Usage

```
# Add a once-daily medication
/medication add aspirin 100mg once daily after breakfast

# Add a twice-daily medication
/medication add amlodipine 5mg once each morning and evening

# Add a three-times-daily medication
/medication add metformin 500mg three times daily after meals

# Add a once-weekly medication
/medication add vitamin D 1000IU once weekly

# Record medication taken
/medication log took aspirin
/medication log aspirin taken

# Record missed dose
/medication log forgot amlodipine
/medication log amlodipine missed

# View medication list
/medication list

# View today's medication history
/medication history today

# View this week's statistics
/medication status week
```

## Error Handling

- **Medication information empty**: "Please provide medication information, e.g.: /medication add aspirin 100mg once daily"
- **Medication already exists**: "This medication already exists. Please remove the existing entry before making changes."
- **Cannot recognize dosage**: "Unable to recognize dosage information. Please ensure dosage and unit are included (e.g.: 100mg)"
- **Cannot recognize frequency**: "Unable to recognize medication frequency. Please specify how many times per day or per week"
- **No records**: "No medication records found"
- **Medication not found**: "Medication not found. Please add the medication first."
- **Storage failure**: "Failed to save record. Please check storage space."
