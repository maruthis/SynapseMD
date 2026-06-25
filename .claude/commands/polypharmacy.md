---
description: Polypharmacy management command - manage medication lists, Beers Criteria screening, drug interaction checks
arguments:
  - name: action
    description: Action type (add, list, beers, inappropriate, interaction, anticholinergic, acb-score, deprescribe, status, recommendations)
    required: true
  - name: info
    description: Specific information (medication info, interactions, deprescribing plan, etc.)
    required: false
---

# Polypharmacy Management Command

## Feature Overview

Used to manage polypharmacy in the elderly, including medication list management, Beers Criteria screening, drug interaction checks, and deprescribing plans.

---

## ⚠️ Safety Red Lines

1. **Do not adjust medication doses or discontinue medications**
   - Do not recommend specific medication dose adjustments
   - Do not recommend self-discontinuation of medications
   - Adjustments require physician evaluation

2. **Do not replace professional assessment by physicians/pharmacists**
   - System only provides screening and recommendations
   - Medication adjustments require healthcare professionals

3. **Do not recommend specific medication regimens**
   - Do not recommend specific medication brands
   - Do not write prescriptions
   - Medication regimens require physician decisions

---

## ✅ What the system can do

- Medication list management
- Inappropriate medication screening (Beers Criteria)
- Drug-drug interaction checks
- Drug-disease interaction checks
- Anticholinergic drug burden assessment
- Deprescribing plan recommendations
- Medication adherence assessment

---

## Available Operations

### 1. Add Medication - `add`

Add new medication information.

**Parameter description:**
- `info`: Medication information (required)
  - Medication name
  - Dose (e.g., 100mg, 5mg)
  - Administration frequency (qd/bid/tid/qid/prn, etc.)
  - Indication (optional)
- `date`: Start date (optional, default today)

**Execution steps:**
#### 1. Parameter identification
- Extract medication name, dose, and administration from info
- Format: `(\w+)[\s]+([\d.]+mg)[\s]+(\w+)`
- Example: "aspirin 100mg qd"

#### 2. Record update
- Update `data/polypharmacy-management.json`
- Add to `medication_list` array
- Update medication count

#### 3. Automatic screening
- Automatically perform Beers Criteria screening
- Automatically check drug interactions
- Update anticholinergic burden

#### 4. Output confirmation
- Display newly added medication information
- Display Beers Criteria screening results
- Display drug interactions (if any)
- Display current total medication count

**Examples:**
```
/polypharmacy add aspirin 100mg qd cardiovascular protection
/polypharmacy add amlodipine 5mg qd hypertension
```

---

### 2. View Medication List - `list`

View all current medications.

**Execution steps:**
#### 1. Read data
- Read `data/polypharmacy-management.json`
- Extract `medication_list` array

#### 2. Display medication list
- Medication name
- Dose and administration
- Indication
- Start date
- Whether appropriate (based on Beers Criteria)

#### 3. Statistics
- Total number of medications
- Prescription medications
- Over-the-counter medications
- Inappropriate medications

**Example:**
```
/polypharmacy list
```

---

### 3. Beers Criteria Screening - `beers`

Screen for inappropriate medications based on Beers Criteria.

**Execution steps:**
#### 1. Read medication list
- Read `data/polypharmacy-management.json`

#### 2. Beers Criteria screening
- Check against Beers Criteria (2019 edition) one by one
- Identify potentially inappropriate medications in the elderly
- Identify medications to use with caution in the elderly
- Identify drug-disease interactions

#### 3. Update records
- Update `beers_criteria_violations` array
- Flag inappropriate medications

#### 4. Display screening results
- List of inappropriate medications
- Issues with each medication
- Severity level
- Alternative recommendations

**Common Beers Criteria inappropriate medications:**
- Benzodiazepines (falls, excessive sedation)
- Anticholinergic drugs (cognitive impairment, constipation)
- First-generation antihistamines (sedation, anticholinergic)
- NSAIDs (gastrointestinal bleeding, renal impairment)
- Corticosteroids (long-term use)
- Warfarin (bleeding risk, use with caution)

**Example:**
```
/polypharmacy beers
```

---

### 4. View Inappropriate Medications - `inappropriate`

View inappropriate medications identified by Beers Criteria screening.

**Execution steps:**
#### 1. Read screening results
- Read `beers_criteria_violations` array

#### 2. Display inappropriate medication report
- Medication name
- Beers Criteria violated
- Severity (high/moderate/low)
- Recommended actions
- Alternative medications

**Example:**
```
/polypharmacy inappropriate
```

---

### 5. Drug Interaction Check - `interaction`

Check drug-drug and drug-disease interactions.

**Sub-operations:**
- `check` - Check interactions for all medications
- `add` - Add known interactions

**Parameter description (check):**
No parameters needed, checks interactions for all medications

**Parameter description (add):**
- `info`: Interaction information
  - Two medication names
  - Severity (major/moderate/minor)
  - Interaction description

**Execution steps:**
#### 1. Parameter identification (add)
- Extract two medication names and severity from info
- Format: `interaction[:\s]+add[:\s]+(\w+)[\s]+(\w+)[\s]+(\w+)`

#### 2. Interaction check
- Check drug-drug interactions
- Check drug-disease interactions
- Reference standard interaction databases

#### 3. Update records
- Update `drug_interactions` array
- Update `disease_drug_interactions` array

#### 4. Display interaction report
- Interaction list
- Severity level
- Clinical significance
- Management recommendations

**Common important interactions:**
- Warfarin + Aspirin → Increased bleeding risk
- ACE inhibitor + Potassium-sparing diuretics → Hyperkalemia
- Beta-blockers + Digoxin → Bradycardia
- NSAIDs + ACE inhibitor/ARB → Renal function deterioration
- Antidepressants + MAOIs → Serotonin syndrome

**Examples:**
```
/polypharmacy interaction check
/polypharmacy interaction add warfarin aspirin moderate
```

---

### 6. Anticholinergic Burden Assessment - `anticholinergic`

Calculate anticholinergic drug burden score.

**Sub-operations:**
- No parameters - Calculate anticholinergic burden for current medications
- `acb-score` - Directly record ACB score

**Anticholinergic burden scoring standard (ACB scale):**
- Each medication scored 0-3 points
- Cumulative total score
- Result interpretation:
  - 0-1: Acceptable
  - 2-3: Avoid if possible
  - ≥4: Significant risk

**Common anticholinergic medications:**
- Benzodiazepines (1 point)
- First-generation antihistamines (2-3 points)
- Tricyclic antidepressants (3 points)
- Antipsychotics (2-3 points)
- Anti-Parkinson medications (1-2 points)
- Bladder anticholinergic medications (1-2 points)

**Execution steps:**
#### 1. Identify anticholinergic medications
- Identify from medication list
- Reference ACB scale scoring

#### 2. Calculate total score
- Sum all medication scores

#### 3. Assess risk
- Assess risk level based on total score
- List associated risks (cognitive impairment, falls, dry mouth, constipation, etc.)

#### 4. Update records
- Update `anticholinergic_burden` section

#### 5. Display assessment report
- Total anticholinergic burden score
- Contributing medications list
- Risk level
- Associated risks
- Reduction recommendations

**Examples:**
```
/polypharmacy anticholinergic
/polypharmacy acb-score 4
```

---

### 7. Deprescribing Plan - `deprescribe`

Develop a medication deprescribing plan.

**Parameter description:**
- `info`: Deprescribing medication information (optional)
  - Medication name
  - Action (taper/switch/discontinue)
  - Timeline
  - Alternative medication

**Deprescribing principles:**
- Discontinue medications without clear indications
- Discontinue medications with poor efficacy
- Discontinue preventive medications (unclear benefit)
- Reduce number of medications
- Simplify administration regimen

**Deprescribing steps:**
- Assess the indication for each medication
- Assess medication benefits and risks
- Identify medications that can be discontinued
- Develop a dose reduction plan
- Monitor dose reduction response

**Execution steps:**
#### 1. Parameter identification
- Extract medication name and action from info
- Format: `deprescribe[:\s]+(\w+)[\s]+(\w+)`

#### 2. Identify candidate medications
- Beers Criteria inappropriate medications
- High anticholinergic burden medications
- Medications without clear indications
- Medications that can be safely discontinued

#### 3. Develop deprescribing plan
- Determine action (taper/switch/discontinue)
- Determine timeline
- Determine alternative options (if applicable)
- Determine monitoring indicators

#### 4. Update records
- Update `deprescribing_plan` array

#### 5. Display deprescribing plan
- Candidate medication list
- Deprescribing recommendations
- Dose reduction schedule
- Monitoring indicators
- Precautions

**Examples:**
```
/polypharmacy deprescribe
/polypharmacy deprescribe diazepam taper
/polypharmacy deprescribe chlorpheniramine switch loratadine
```

---

### 8. View Polypharmacy Status - `status`

View current polypharmacy management status.

**Execution steps:**
#### 1. Read data
- Read `data/polypharmacy-management.json`

#### 2. Display status report
- Medication list summary
- Beers Criteria screening results
- Drug interaction summary
- Anticholinergic burden
- Deprescribing plan
- Statistical data

**Example:**
```
/polypharmacy status
```

---

### 9. View Recommendations - `recommendations`

View polypharmacy management recommendations.

**Execution steps:**
#### 1. Comprehensive assessment
- Based on Beers Criteria screening results
- Based on drug interactions
- Based on anticholinergic burden
- Based on medication adherence

#### 2. Generate recommendations
- Medication deprescribing recommendations
- Alternative medication recommendations
- Medication adherence improvement recommendations
- Regular review recommendations

#### 3. Display recommendation report
- Priority ranking
- Specific recommendation content
- Implementation timeline
- Monitoring indicators

**Example:**
```
/polypharmacy recommendations
```

---

## Notes

### Medication Review
- Regular medication review (every 6 months)
- Assess the indication for each medication
- Assess medication benefits and risks
- Identify duplicate medications

### Deprescribing
- Gradually reduce medications to avoid withdrawal reactions
- Prioritize deprescribing of Beers Criteria inappropriate medications
- Prioritize deprescribing of high anticholinergic burden medications
- Monitor dose reduction response

### Interaction Management
- Focus on serious interactions
- Consider drug-disease interactions
- Regular review of liver and kidney function

### Adherence Improvement
- Simplify administration regimen
- Reduce number of medications
- Use pill organizers
- Set reminders

---

## Reference Resources

- Beers Criteria (AGS 2019 edition)
- Anticholinergic Cognitive Burden (ACB) Scale
- START/STOP Criteria
- Chinese Potentially Inappropriate Medication List for the Elderly
