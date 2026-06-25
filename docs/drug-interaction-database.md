# Drug Interaction Database

## Feature Overview

The system has a built-in drug interaction detection feature that stores and manages interaction rules through the `data/interactions/interaction-db.json` database. This feature supports:

- **Drug-drug interaction detection**: Checks interactions between current medication combinations
- **Drug-disease conflict detection**: Checks whether a drug conflicts with the user's medical history
- **Drug dosage conflict detection**: Checks whether dosages are exceeded, taking age and renal function into account
- **Drug-food interaction detection**: Checks interactions between drugs and diet

## Five-Level Severity Classification

| Level | Name | Color | Definition | Recommended Action |
|-------|------|-------|------------|--------------------|
| A | Safe | 🟢 | No significant interaction | No special measures required |
| B | Use with Caution | 🟡 | Minor interaction, low risk | Monitor; no adjustment needed |
| C | Relative Contraindication | 🟠 | Clinically significant interaction | Weigh benefit vs. risk; consider alternatives |
| D | Contraindicated | 🔴 | Serious interaction; risk > benefit | Avoid co-administration; monitor if unavoidable |
| X | Absolute Contraindication | 🆘 | Life-threatening interaction | Strictly prohibited |

## Contribution Guidelines for Healthcare Professionals 🩺

We sincerely invite healthcare professionals (pharmacists, physicians, clinical pharmacologists, etc.) to help improve and maintain the drug interaction database.

### Database File Location

```
data/interactions/interaction-db.json
```

### Data Structure Description

Each interaction rule contains the following fields:

```json
{
  "id": "int_001",
  "type": "drug_drug",           // Type: drug_drug/drug_disease/drug_dosage/drug_food
  "type_name": "Drug-Drug Interaction",
  "drugs": [                      // For drug-drug interactions
    {
      "name": "Warfarin",
      "generic_name": "Warfarin",
      "category": "Anticoagulant",
      "synonyms": ["Coumadin"]
    },
    {
      "name": "Aspirin",
      "generic_name": "Aspirin",
      "category": "Antiplatelet",
      "synonyms": ["Acetylsalicylic acid"]
    }
  ],
  "severity": {
    "level": "X",                 // A/B/C/D/X
    "level_name": "Absolute Contraindication",
    "level_code": 5,              // 1-5
    "color": "🆘"
  },
  "interaction_details": {
    "mechanism": "Description of mechanism of action",
    "effect": "Interaction effect",
    "clinical_impact": "Clinical impact"
  },
  "recommendations": [
    "Recommendation 1",
    "Recommendation 2"
  ],
  "management": {
    "action": "avoid",            // avoid/monitor/adjust
    "monitoring": ["Monitoring item 1", "Monitoring item 2"]
  },
  "evidence": {
    "source": "FDA Drug Label",
    "reliability": "high",
    "references": [
      "Drug Interactions: Warfarin and Aspirin",
      "Clinical Pharmacology"
    ]
  },
  "active": true,
  "is_custom": false,             // false for preset rules, true for custom rules
  "created_at": "2025-12-31T12:34:56.789Z"
}
```

### Different Types of Interaction Rules

#### Drug-Drug Interaction (drug_drug)

```json
{
  "id": "int_001",
  "type": "drug_drug",
  "drugs": [
    {"name": "Warfarin", "generic_name": "Warfarin", "category": "Anticoagulant"},
    {"name": "Aspirin", "generic_name": "Aspirin", "category": "Antiplatelet"}
  ],
  "severity": {"level": "X", "level_name": "Absolute Contraindication", "level_code": 5},
  ...
}
```

#### Drug-Disease Interaction (drug_disease)

```json
{
  "id": "int_015",
  "type": "drug_disease",
  "drug": {
    "name": "Ibuprofen",
    "generic_name": "Ibuprofen",
    "category": "NSAID"
  },
  "disease": {
    "name": "Peptic Ulcer",
    "icd_code": "K25",
    "synonyms": ["Gastric ulcer", "Duodenal ulcer"]
  },
  "severity": {"level": "X", "level_name": "Absolute Contraindication", "level_code": 5},
  ...
}
```

#### Drug Dosage Limit (drug_dosage)

```json
{
  "id": "int_023",
  "type": "drug_dosage",
  "drug": {
    "name": "Digoxin",
    "generic_name": "Digoxin",
    "category": "Cardiac glycoside"
  },
  "dosage_limit": {
    "max_daily_dose": {"value": 0.25, "unit": "mg"},
    "warning_threshold": {"value": 0.5, "unit": "mg"},
    "age_adjustments": [
      {
        "age_group": "Elderly (>65 years)",
        "max_dose": {"value": 0.125, "unit": "mg"}
      }
    ]
  },
  ...
}
```

#### Drug-Food Interaction (drug_food)

```json
{
  "id": "int_019",
  "type": "drug_food",
  "drug": {
    "name": "Warfarin",
    "generic_name": "Warfarin",
    "category": "Anticoagulant"
  },
  "food": {
    "name": "Vitamin K-rich foods",
    "category": "Vegetables",
    "examples": ["Spinach", "Kale", "Broccoli"]
  },
  "severity": {"level": "C", "level_name": "Relative Contraindication", "level_code": 3},
  ...
}
```

### Update Guidelines

#### Adding New Interaction Rules

1. **Follow the data structure format**: Provide complete fields as shown above
2. **Ensure information sources are reliable**:
   - Prioritize drug labels (FDA, EMA, NMPA)
   - Clinical guidelines and consensus documents
   - Authoritative medical literature (Lancet, NEJM, etc.)
   - Professional drug interaction databases (Micromedex, Facts & Comparisons)
3. **Provide accurate severity classification**: Classify based on clinical evidence
4. **Give clear management recommendations**: Include monitoring parameters and management plans
5. **Update the metadata section**: Record data sources and review dates

#### Severity Classification Reference

**Class X (Absolute Contraindication)**: Life-threatening interactions; strictly prohibited
- Example: MAOIs + SSRIs (serotonin syndrome)
- Example: Nitroglycerin + Sildenafil (severe hypotension)
- Example: Terfenadine + Macrolides (fatal arrhythmia)

**Class D (Contraindicated)**: Serious interactions; risk clearly outweighs benefit
- Example: Warfarin + Aspirin (severe bleeding)
- Example: Digoxin + Potassium-wasting diuretics (digoxin toxicity)
- Example: Simvastatin + Potent CYP3A4 inhibitors (rhabdomyolysis)

**Class C (Relative Contraindication)**: Clinically significant interactions
- Example: NSAIDs + ACEI/ARB (reduced antihypertensive effect; increased risk of renal injury)
- Example: Warfarin + Vitamin K-rich foods (reduced anticoagulant effect)
- Example: Statins + Grapefruit juice (elevated plasma drug concentration)

**Class B (Use with Caution)**: Minor interactions, low risk
- Example: Certain antibiotics + Oral contraceptives (may reduce contraceptive efficacy)
- Example: H2 blockers + Antacids (may affect absorption)

**Class A (Safe)**: No significant interaction
- Example: Vitamin C + Vitamin B complex
- Example: Amlodipine + Irbesartan (antihypertensive combination)

### Quality Requirements

To ensure data quality and patient safety, please follow these guidelines when contributing:

1. **Accuracy**: Based on authoritative medical resources (FDA, EMA, NMPA drug labels, clinical guidelines)
2. **Completeness**: Provide complete mechanism, effects, and recommendations; do not omit critical information
3. **Clarity**: Use professional medical terminology; avoid vague language
4. **Traceability**: Note data sources in the `evidence` field to facilitate review and updates
5. **Practicality**: Recommendations should be specific and actionable; monitoring parameters should be clearly defined
6. **Regular updates**: Medical knowledge continues to evolve; periodic review and updates are recommended

### Version Control

When updating the database, please follow version control conventions:

1. **Update the version number**: Increment the `version` field (e.g., from 1.0.0 to 1.0.1)
2. **Update the timestamp**: Update `last_updated` to the current time
3. **Record changes**: Add a `changelog` field in the `metadata` section
4. **Update statistics**: Update the rule counts in `statistics`
5. **Keep backups**: Retain old version backups in case rollback is needed

Example update record:
```json
{
  "version": "1.1.0",
  "last_updated": "2025-01-15T10:30:00.000Z",
  "metadata": {
    "changelog": [
      {
        "version": "1.1.0",
        "date": "2025-01-15",
        "changes": "Added 5 new drug-drug interaction rules",
        "contributor": "Dr. Zhang (Pharmacist)",
        "reviewer": "Director Li (Clinical Pharmacy)"
      }
    ],
    "last_review": "2025-01-15",
    "next_review": "2025-07-15"
  }
}
```

### Data Validation

Before submitting updates, please perform the following validations:

1. **JSON format validation**: Ensure the JSON format is correct with no syntax errors
2. **Field completeness check**: Ensure all required fields are filled in
3. **Data consistency check**:
   - `severity.level` is consistent with `severity.level_code`
   - Counts in `statistics` match the actual number of rules
4. **Duplicate check**: Ensure no duplicate rules are added
5. **Logic check**: Ensure recommendations match the severity classification

### Disclaimer

The drug interaction database is for reference only and cannot replace professional medical judgment. Users of this system should:

- **Seek professional advice**: Consult a physician or pharmacist for professional guidance
- **Individualize treatment**: Adjust medication plans based on individual circumstances
- **Regular updates**: Periodically check and update the interaction database
- **Seek help promptly**: If in doubt, seek professional medical advice without delay
- **Personal responsibility**: Users are responsible for decisions made based on the database

### Contribution Process

1. **Read this document**: Understand the data structure and quality requirements
2. **Collect evidence**: Gather interaction information from authoritative sources
3. **Prepare data**: Prepare rule data according to the specified format
4. **Validate data**: Perform format and logic validation
5. **Submit updates**: Submit via one of the following methods:
   - GitHub Pull Request
   - Email submission
6. **Review process**: Reviewed by a qualified pharmacist/physician
7. **Merge update**: Merged into the main database after approval
8. **Version record**: Record the contributor in the changelog

### Contact Information

To contribute or report database issues, please contact us via:

- **GitHub Issues**: [Project repository]
- **Email**: [Project maintenance email]
- **WeChat Group**: [Healthcare professional contributor group]

Thank you for your professional contribution — making the system safer and more reliable! 💪

## Appendix: Frequently Asked Questions

### Q1: How is severity classification determined?

A: Based on a comprehensive assessment of the following factors:
- Clinical significance of the interaction
- Severity of adverse reactions
- Whether the interaction is life-threatening
- Availability of alternative options
- Risk-benefit balance

### Q2: How often is the data updated?

A: Recommended:
- Add relevant interactions within 3 months of a new drug's market approval
- Review existing rules quarterly
- Update important safety warnings within 48 hours

### Q3: How are controversial interactions handled?

A:
- Note the level of evidence (high/medium/low)
- Provide sources representing different viewpoints
- Give conservative recommendations
- Recommend consulting a specialist

### Q4: Can herbal drug interactions be added?

A: Yes, but it requires:
- High-quality clinical evidence
- Clear identification of the herbal drug's constituents
- Noting the reliability level of the evidence
- Recommending cautious use

### Q5: How are pediatric drug interactions handled?

A:
- Add age restriction fields
- Provide pediatric dose adjustment recommendations
- Indicate whether the rule applies to children
- Reference pediatric medication guidelines
