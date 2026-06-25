# Emergency Medical Information Card - Usage Examples

## Example 1: Preparing an Emergency Card for Travel

### User Input
```
I'm traveling to Beijing next week and need to prepare an emergency medical information card
```

### Claude Execution
1. Read user's allergy history (found Grade 4 penicillin allergy)
2. Read current medications (aspirin, amlodipine)
3. Read implant information (cardiac pacemaker)
4. Generate JSON and text format cards with key information
5. Generate QR code for easy phone scanning

### Output Result
```json
{
  "emergency_card": {
    "version": "1.0",
    "generated_at": "2025-12-31T12:34:56Z",
    "basic_info": {
      "name": "Zhang San",
      "age": 35,
      "gender": "Male",
      "blood_type": "A+",
      "weight": "70kg",
      "emergency_contacts": [
        {
          "name": "Li Si",
          "relationship": "Spouse",
          "phone": "138****1234"
        }
      ]
    },
    "critical_allergies": [
      {
        "allergen": "Penicillin",
        "severity": "Anaphylaxis (Grade 4)",
        "reaction": "Difficulty breathing, laryngeal edema, loss of consciousness",
        "diagnosed_date": "2010-05-15"
      }
    ],
    "current_medications": [
      {
        "name": "Aspirin",
        "dosage": "100mg",
        "frequency": "Once daily",
        "instructions": "Take after breakfast",
        "purpose": "Cardiovascular prevention"
      },
      {
        "name": "Amlodipine",
        "dosage": "5mg",
        "frequency": "Twice daily",
        "instructions": "Take morning and evening",
        "purpose": "Antihypertensive therapy"
      }
    ],
    "medical_conditions": [
      {
        "condition": "Hypertension",
        "diagnosis_date": "2023-01-15",
        "status": "Under control"
      },
      {
        "condition": "Type 2 Diabetes",
        "diagnosis_date": "2022-08-20",
        "status": "Under monitoring"
      }
    ],
    "implants": [
      {
        "type": "Cardiac pacemaker",
        "implant_date": "2022-06-10",
        "hospital": "XX Hospital",
        "notes": "Regular follow-up required, avoid MRI"
      }
    ],
    "disclaimer": "This information card is for reference only and does not replace professional medical diagnosis",
    "data_source": "my-his Personal Health Information System"
  }
}
```

### Travel Recommendations
```
💡 Travel recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Save the QR code to your phone's photo album
2. Print a text version and keep it in your wallet
3. Upload the JSON file to cloud storage
4. Carry an allergy emergency card at all times
5. Inform your travel companions about your allergies

⚠️  Special notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Cardiac pacemaker: Notify airport security proactively
• Penicillin allergy: Must inform doctor at every medical visit
• Chronic disease medications: Carry sufficient supply in separate locations
```

---

## Example 2: Preparing an Emergency Card for an Elderly Person

### User Input
```
My father is 75 years old and lives alone. He needs an emergency card.
```

### Claude Execution
1. Read the father's profile (age: 75, blood type: B+)
2. Read severe allergy history (Grade 3 sulfonamide allergy)
3. Read multiple medications (5 chronic disease drugs)
4. Read medical conditions (hypertension, diabetes, coronary artery disease)
5. Generate a large-font, clear text card

### Output Result (Text Format)
```
╔═══════════════════════════════════════════════════════════╗
║                ELDERLY EMERGENCY INFORMATION CARD         ║
╠═══════════════════════════════════════════════════════════╣
║ Name: Wang Wu                     Age: 75                 ║
║ Gender: Male                      Blood Type: B+          ║
╠═══════════════════════════════════════════════════════════╣
║ 🆘 Severe Allergies (Emergency)                           ║
║ ─────────────────────────────────────────────────────── ║
║ • Sulfonamide drugs - Severe allergy (Grade 3)           ║
║   Reaction: Widespread rash, fever                       ║
╠═══════════════════════════════════════════════════════════╣
║ 💊 Current Medications (5)                               ║
║ ─────────────────────────────────────────────────────── ║
║ 1. Aspirin 100mg - Once daily                            ║
║ 2. Amlodipine 5mg - Twice daily                          ║
║ 3. Metformin 500mg - Three times daily                   ║
║ 4. Metoprolol 25mg - Twice daily                         ║
║ 5. Simvastatin 20mg - Once nightly                       ║
╠═══════════════════════════════════════════════════════════╣
║ 🏥 Medical Conditions                                     ║
║ ─────────────────────────────────────────────────────── ║
║ • Hypertension (Diagnosed 2018-03-10)                    ║
║ • Type 2 Diabetes (Diagnosed 2019-07-22)                 ║
║ • Coronary artery disease (Diagnosed 2020-11-05)         ║
╠═══════════════════════════════════════════════════════════╣
║ 📞 Emergency Contacts (2)                                 ║
║ ─────────────────────────────────────────────────────── ║
║ 1. Wang Xiaoming (Son) - 139****5678                     ║
║ 2. Mrs. Wang (Daughter-in-law) - 136****9012             ║
╠═══════════════════════════════════════════════════════════╣
║ ⚠️  Special Notes                                        ║
║ ─────────────────────────────────────────────────────── ║
║ • Elderly person living alone — contact family first     ║
║ • Severe sulfonamide allergy — absolutely prohibited     ║
║ • Cardiovascular disease history — monitor BP & HR       ║
╚═══════════════════════════════════════════════════════════╝

⚠️  In an emergency, call emergency services immediately
Generated: 2025-12-31 12:34:56
```

### Recommendations for Elderly Users
```
💡 Recommendations for elderly users:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Print the card in a larger size and post it on the refrigerator
2. Carry a small-size card at all times
3. Inform neighbors and community doctors
4. Set up quick-dial shortcuts for emergency contacts on the phone
5. Update information every quarter
```

---

## Example 3: Preparing a Medical Information Card for a Child

### User Input
```
My son is 8 years old. The school needs a medical information file.
```

### Claude Execution
1. Read child's profile (age: 8, blood type: O+)
2. Read allergy history (Grade 2 egg and milk allergy)
3. Read medication history (asthma prevention medication)
4. Read medical conditions (bronchial asthma)
5. Generate a child-specific card including parent contact information

### Output Result
```json
{
  "emergency_card": {
    "version": "1.0",
    "type": "pediatric",
    "generated_at": "2025-12-31T12:34:56Z",
    "basic_info": {
      "name": "Wang Xiaoming",
      "age": 8,
      "gender": "Male",
      "blood_type": "O+",
      "weight": "25kg",
      "school": "XX Primary School",
      "grade": "Grade 2"
    },
    "allergies": [
      {
        "allergen": "Eggs",
        "severity": "Moderate allergy (Grade 2)",
        "reaction": "Skin itching, hives",
        "diagnosed_date": "2021-03-15"
      },
      {
        "allergen": "Milk",
        "severity": "Mild allergy (Grade 1)",
        "reaction": "Mild abdominal pain",
        "diagnosed_date": "2021-06-20"
      }
    ],
    "current_medications": [
      {
        "name": "Montelukast sodium",
        "dosage": "5mg",
        "frequency": "Once nightly",
        "purpose": "Asthma prevention"
      }
    ],
    "medical_conditions": [
      {
        "condition": "Bronchial asthma",
        "diagnosis_date": "2022-09-10",
        "status": "Under control",
        "triggers": ["Pollen", "Dust mites", "Cold air"]
      }
    ],
    "emergency_contacts": [
      {
        "name": "Mr. Wang (Father)",
        "phone": "138****1234"
      },
      {
        "name": "Ms. Li (Mother)",
        "phone": "139****5678"
      },
      {
        "name": "XX Primary School Medical Room",
        "phone": "010-****1234"
      }
    ],
    "school_instructions": [
      "Avoid foods containing eggs and milk",
      "Stop immediately if breathing difficulty occurs during PE class",
      "Reduce outdoor activities during spring and autumn",
      "Keep asthma emergency medication on hand at all times"
    ],
    "disclaimer": "This information card is for reference only and does not replace professional medical diagnosis"
  }
}
```

### Recommendations for School Use
```
💡 Recommendations for school use:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Make a copy for the homeroom teacher
2. Make a copy for the school nurse
3. Inform the PE teacher of allergy conditions
4. Update emergency contacts regularly
5. Update health information every semester
```

---

## Example 4: Healthy Person with No Allergies or Medications

### User Input
```
Generate an emergency medical information card
```

### Claude Execution
1. Read user profile (age: 28, healthy)
2. No allergy history found
3. No current medications found
4. No implants found
5. Generate a concise basic information card

### Output Result
```
✅ Emergency Medical Information Card generated

File location: data/emergency-cards/emergency-card-2025-12-31.json

Information included:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Basic information (name, age, blood type)
✓ Allergy history: Not recorded
✓ Current medications: None
✓ Medical conditions: None
✓ Implants: None

💡 Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
No severe allergy history, medications, or medical conditions have been recorded.
Recommendations:
• Update health information regularly
• Record any new diagnoses promptly
• Generate a fresh card before travel
```

---

## Example 5: Multiple Severe Allergies + Polypharmacy

### User Input
```
I have multiple severe allergies and need a detailed emergency card
```

### Claude Execution
1. Read user allergy history (penicillin Grade 4, sulfonamide Grade 3, iodine contrast Grade 3)
2. Read current medications (7 drugs with interaction warnings)
3. Read medical conditions (allergic asthma, hypertension, renal insufficiency)
4. Generate a detailed medical information card

### Output Result
```
╔═══════════════════════════════════════════════════════════╗
║     SEVERE ALLERGY PATIENT - EMERGENCY MEDICAL INFO CARD  ║
╠═══════════════════════════════════════════════════════════╣
║ Name: Zhao Liu                    Age: 45                 ║
║ Blood Type: AB+                   Weight: 65kg            ║
╠═══════════════════════════════════════════════════════════╣
║ 🆘🆘🆘 SEVERE ALLERGIES (LIFE-THREATENING) 🆘🆘🆘        ║
╠═══════════════════════════════════════════════════════════╣
║ 1. Penicillin - Anaphylaxis (Grade 4) 🆘                 ║
║    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║    Reaction: Difficulty breathing, laryngeal edema,       ║
║              BP drop, loss of consciousness               ║
║    Diagnosed: 2010-05-15                                  ║
║    ⚠️  Absolutely prohibited: All penicillin-class drugs  ║
║    ⚠️  Cross-allergy: Cephalosporins require caution      ║
╠═══════════════════════════════════════════════════════════╣
║ 2. Sulfonamide drugs - Severe allergy (Grade 3) 🆘       ║
║    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║    Reaction: Widespread rash, fever, joint pain           ║
║    Diagnosed: 2012-08-20                                  ║
║    ⚠️  Absolutely prohibited: Sulfonamide antibiotics     ║
╠═══════════════════════════════════════════════════════════╣
║ 3. Iodine contrast agent - Severe allergy (Grade 3) 🆘   ║
║    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║    Reaction: Facial edema, difficulty breathing, low BP   ║
║    Diagnosed: 2018-03-10                                  ║
║    ⚠️  Absolutely prohibited: Iodine contrast agents      ║
║         (CT with contrast, angiography)                   ║
║    ⚠️  Alternative: MRI or ultrasound                     ║
╠═══════════════════════════════════════════════════════════╣
║ 💊 Current Medications (7)                               ║
╠═══════════════════════════════════════════════════════════╣
║ ⚠️  Drug Interaction Warnings                            ║
║ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║ • Aspirin + Clopidogrel                                   ║
║   Risk: Increased bleeding risk                          ║
║ • ACEI + Diuretics                                       ║
║   Risk: Renal function impact                            ║
╠═══════════════════════════════════════════════════════════╣
║ Medication List:                                          ║
║ ─────────────────────────────────────────────────────── ║
║ 1. Aspirin 100mg - Once daily                            ║
║ 2. Clopidogrel 75mg - Once daily                         ║
║ 3. Amlodipine 5mg - Twice daily                          ║
║ 4. Benazepril 10mg - Once daily                          ║
║ 5. Hydrochlorothiazide 12.5mg - Once daily               ║
║ 6. Montelukast sodium 10mg - Once nightly                ║
║ 7. Budesonide inhaler - As needed                        ║
╠═══════════════════════════════════════════════════════════╣
║ 🏥 Medical Conditions                                     ║
║ ─────────────────────────────────────────────────────── ║
║ • Allergic asthma (Diagnosed 2015-04-12)                 ║
║ • Hypertension (Diagnosed 2018-06-20)                    ║
║ • Renal insufficiency (CKD Stage 3, diagnosed 2020-11-05)║
╠═══════════════════════════════════════════════════════════╣
║ 📞 Emergency Contacts                                     ║
║ ─────────────────────────────────────────────────────── ║
║ • Spouse: Ms. Zhou - 137****2468                         ║
╠═══════════════════════════════════════════════════════════╣
║ ⚠️  Medical Visit Notes                                  ║
║ ─────────────────────────────────────────────────────── ║
║ 1. Always inform doctor of three severe allergies        ║
║ 2. Avoid iodine contrast; use MRI or ultrasound          ║
║ 3. Renal insufficiency — dosage adjustment required      ║
║ 4. Antiplatelet medication — stop before surgery         ║
║ 5. Asthma patient — avoid beta-blockers                  ║
╠═══════════════════════════════════════════════════════════╣
║ 🆘 Allergy Emergency Protocol                            ║
║ ─────────────────────────────────────────────────────── ║
║ If experiencing difficulty breathing, laryngeal edema,   ║
║ or low blood pressure:                                    ║
║ 1. Immediately stop exposure to suspected allergen       ║
║ 2. Call emergency services immediately                   ║
║ 3. Keep airway clear                                     ║
║ 4. If epinephrine auto-injector is available, use now    ║
║ 5. Await professional medical assistance                 ║
╚═══════════════════════════════════════════════════════════╝

⚠️  This patient has multiple severe allergies — exercise extreme caution with medications
Generated: 2025-12-31 12:34:56
```

### Recommendations for Patients with Severe Allergies
```
💡 Recommendations for patients with severe allergies:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Always carry an allergy emergency kit
2. Wear a medical alert bracelet
3. Set allergy warning wallpaper on your phone
4. Proactively inform the doctor of your allergy history at every visit
5. Update allergy information regularly
6. Teach family members the allergy emergency response
```

---

## Common Use Case Summary

| Scenario | Key Information | Recommended Format |
|----------|-----------------|--------------------|
| **Travel** | Allergies, medications, implants | QR code + text version |
| **Elderly living alone** | Multiple medications, emergency contacts | Large-print text version |
| **Child at school** | Allergies, parent contact info | School-specific format |
| **Severe allergies** | Allergens, cross-allergies, emergency protocol | Detailed version + emergency instructions |
| **Pre-surgery preparation** | Medications, implants, allergies | Doctor-specific format |
| **Daily carry** | Concise key information | Wallet card size |
