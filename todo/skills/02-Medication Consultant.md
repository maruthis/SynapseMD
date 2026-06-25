# Medication Advisor Skill Design

## Overview
**Skill Name**: `medication-advisor`
**Purpose**: Intelligent medication management, providing comprehensive safety checks, interaction detection, and adherence optimization.

## Description
Provides intelligent medication guidance including interaction checks, allergy conflict detection, dose timing optimization, adherence tracking, and safety recommendations. Use when adding new medications, checking interactions, optimizing medication schedules, or when asked "Can I take these medications together?"

## Data Integration

### Data Sources
- **Medication Records** (`data/medications/`): Current medication list and history
- **Allergy Information** (`data/allergies.json`): Allergy information for conflict checks
- **Personal Profile** (`data/profile.json`): Age, weight for dosing considerations
- **Symptom Records** (`data/symptoms/`): Track medication side effects
- **Drug Interaction Database**: Reference data for drug-drug interactions

### Related Commands
- `/medication`: Primary command for medication entry
- `/interaction`: Check specific drug interactions
- `/allergy`: Allergy information

## Core Features

### 1. Comprehensive Interaction Checks
- **Drug-Drug Interactions**: Check all current medications against newly added medication
  - 5-level severity system (A/B/C/D/X)
  - Detailed interaction descriptions
  - Management recommendations
- **Drug-Allergy Interactions**: Cross-reference with known allergies
- **Drug-Disease Interactions**: Check contraindications based on health conditions
- **Drug-Food Interactions**: Identify food interactions (e.g., grapefruit, dairy)
- **Drug-Supplement Interactions**: Check herbal and supplement interactions

### 2. Medication Safety Analysis
- **Duplicate Therapy Detection**: Identify duplicate medications or same-class drugs
- **Dose Range Checks**: Verify prescribed dose is within safe range
- **Age Appropriateness Check**: Flag medications inappropriate for age group
- **Contraindication Detection**: Check against surgery, implants, conditions
- **Side Effect Profile**: Explain common and serious side effects
- **Black Box Warnings**: Highlight FDA black box warnings

### 3. Adherence Optimization
- **Schedule Optimization**: Suggest optimal timing for medication administration
- **Reminder Strategies**: Personalized reminder recommendations
- **Pill Organization**: Suggest pill organization strategies
- **Missed Dose Guidance**: Provide missed dose instructions
- **Adherence Barriers**: Identify and address adherence challenges

### 4. Medication Education
- **Purpose Explanation**: What the medication is treating
- **How It Works**: Explain mechanism of action in simple terms
- **Expected Timeline**: When to expect effects
- **Treatment Duration**: How long to take the medication
- **Storage Instructions**: Appropriate storage conditions
- **Disposal Guidelines**: Safe disposal methods

## Output Formats

### Interaction Check Report
```
💊 Medication Interaction Check
Generated: 2025-12-31

🔍 Analyzing: Lisinopril 10mg (new medication)

✅ Drug-Drug Interactions
├─ With Metformin 500mg: Severity A - No known interaction
├─ With Aspirin 81mg: Severity B - Minor interaction
│  └─ Details: May slightly reduce ACE inhibitor effectiveness
│  └─ Action: Monitor blood pressure, no change needed
└─ With Ibuprofen as-needed: Severity D - Moderate interaction
   └─ Details: May reduce antihypertensive effect, kidney strain
   └─ Action: Limit ibuprofen use, monitor kidney function

⚠️ Drug-Allergy Check
└─ No known ACE inhibitor allergies

📊 Dose Assessment
├─ Prescribed: 10mg daily
├─ Typical range: 10-40mg daily
├─ Based on your weight (75kg): Within normal range
└─ Age appropriate: ✅

🎯 Recommendations
1. Safe to continue Lisinopril 10mg daily
2. Limit NSAID use (ibuprofen), consider acetaminophen instead
3. Monitor blood pressure weekly after starting
4. Watch for: dizziness, dry cough, kidney function changes
5. Take in the morning to reduce nighttime urination

⏰ Optimal Timing
├─ Morning (8 AM): Lisinopril, Aspirin
├─ With breakfast: Metformin
└─ As needed: Ibuprofen (use cautiously)

📅 Follow-Up
├─ Blood pressure check: 1 week after starting
├─ Lab work (kidney function): 2 weeks after starting
└─ Doctor appointment: 1 month after starting
```

### Medication Schedule Optimization
```
⏰ Optimized Medication Schedule
Generated: 2025-12-31

🌅 Morning (6:00-8:00 AM)
├─ 07:00 AM - Lisinopril 10mg
│  ├─ Take: On empty stomach, 30 minutes before breakfast
│  ├─ With: A full glass of water
│  └─ Reason: Better absorption, morning blood pressure control
└─ 07:30 AM - Aspirin 81mg
   ├─ Take: With breakfast
   └─ Reason: Reduce stomach discomfort

🍽️ Breakfast (8:00 AM)
└─ 08:00 AM - Metformin 500mg
   ├─ Take: With food to reduce GI side effects
   └─ Reason: Better tolerability

🌙 Evening
└─ No evening medications needed

📋 Adherence Tips
1. Use a pill organizer with morning/evening compartments
2. Set phone alarm for 7:00 AM daily
3. Keep a glass of water on the nightstand
4. Track adherence with a simple checklist

💊 Pill Organizer Setup
Week: Monday - Sunday
├─ Morning compartment: Lisinopril 10mg + Aspirin 81mg
├─ Breakfast compartment: Metformin 500mg
└─ As-needed compartment: Ibuprofen (use cautiously)
```

## Technical Implementation

### Interaction Database Structure
```json
{
  "drug_interactions": {
    "lisinopril": {
      "nsaids": {
        "severity": "D",
        "description": "May reduce antihypertensive effect",
        "mechanism": "Prostaglandin synthesis inhibition",
        "recommendation": "Limit NSAID use, monitor blood pressure and kidney function"
      },
      "potassium_supplements": {
        "severity": "C",
        "description": "Risk of hyperkalemia",
        "recommendation": "Monitor potassium levels"
      }
    }
  },
  "drug_allergies": {
    "ace_inhibitors": {
      "cross_reactivity": ["lisinopril", "enalapril", "benazepril"],
      "reaction_type": "Angioedema, cough, hypotension"
    }
  },
  "contraindications": {
    "lisinopril": {
      "pregnancy": "X - Absolute contraindication",
      "angioedema_history": "X - Contraindicated",
      "renal_artery_stenosis": "D - Use with caution"
    }
  }
}
```

## User Interaction Examples

### Example 1: Adding New Medication
**User**: "My doctor prescribed Lisinopril 10mg. Is it safe to take with my other medications?"
**Skill**: Runs comprehensive interaction check, provides detailed safety report

### Example 2: Interaction Check
**User**: "Can I take ibuprofen with my blood pressure medication?"
**Skill**: Checks specific interaction, provides severity and recommendations

### Example 3: Schedule Optimization
**User**: "What's the best time to take my medications?"
**Skill**: Analyzes all medications, suggests optimal timing based on pharmacokinetics

### Example 4: Side Effect Questions
**User**: "What side effects should I watch for with Lisinopril?"
**Skill**: Provides comprehensive side effect profile and when to seek help

## Safety & Ethics

### Critical Safety Rules
1. **Never provide dosage recommendations** - Only verify that prescribed dose is within standard range
2. **Never recommend starting/stopping medication** - Always defer to the prescribing physician
3. **Always recommend consulting a doctor** - Before making any changes
4. **Always include disclaimers** - This is information, not medical advice
5. **Always report Severity X interactions** - "Do not take - consult doctor immediately"

### Required Disclaimers
```
⚠️ Important Disclaimer
This information is for educational purposes only and is not medical advice.
Always consult a healthcare provider before:
- Starting a new medication
- Stopping a current medication
- Changing dose or schedule
- Ignoring interaction warnings

In case of emergency, call emergency services immediately or contact Poison Control.
```

## Testing Checklist
- [ ] Test with no interactions (no issues)
- [ ] Test Severity X interactions (should block)
- [ ] Test multiple moderate interactions
- [ ] Test allergy conflicts
- [ ] Test duplicate therapy
- [ ] Test edge cases (unknown drugs, pediatric dosing)
- [ ] Verify all safety warnings are present
- [ ] Test schedule optimization logic

## Related Skills
- `health-trend-analyzer`: Track medication effectiveness over time
- `symptom-pattern-analyzer`: Correlate medications with symptoms
- `emergency-card`: Include critical medication interactions
