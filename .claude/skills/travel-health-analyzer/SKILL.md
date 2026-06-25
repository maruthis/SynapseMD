---
name: travel-health-analyzer
description: Analyze travel health data, assess destination health risks, provide vaccination recommendations, and generate multilingual emergency medical information cards. Supports professional-grade travel health risk assessment with WHO/CDC data integration.
allowed-tools: Read, Write, Grep, Glob
---

# Travel Health Analyzer Skill

## 🚨 Important Medical Disclaimer

**All health advice and information provided by this skill is for reference only and cannot replace professional medical advice.**

- ⚠️ **All recommendations must be reviewed by a qualified physician**
- ⚠️ **Vaccination and medication plans must be formulated by a doctor**
- ⚠️ **Does not provide specific medical prescriptions or diagnoses**
- ⚠️ **Health risk data sourced from WHO/CDC may have latency**
- ⚠️ **In emergencies, seek immediate medical attention**

---

## Skill Features

### 1. Travel Health Planning Analysis

Analyzes the user's travel plans and provides comprehensive health preparation recommendations.

**Input**: Travel destination, dates, travel purpose
**Output**:
- Destination health risk assessment
- Mandatory and recommended vaccination list
- Travel medical kit recommendations
- Preventive measure suggestions
- Pre-travel preparation timeline

**Key analysis points**:
- Identify infectious disease risks at the destination
- Assess food and water safety
- Confirm environmental risks (high temperatures, high altitude, etc.)
- Check current outbreak information
- Provide WHO/CDC reference links

---

### 2. Destination Health Risk Assessment

Provides professional-grade health risk assessments for travel destinations based on WHO/CDC data.

**Data sources**:
- World Health Organization (WHO) International Travel Health
- U.S. Centers for Disease Control and Prevention (CDC) Travelers' Health
- Official data from local health authorities

**Assessment dimensions**:
- Infectious disease risks (dengue fever, malaria, cholera, hepatitis A, etc.)
- Food and water safety
- Environmental risks (high temperatures, high altitude, air pollution)
- Seasonal risks
- Current outbreak alerts

**Risk levels**:
- 🟢 **Low risk** - Standard preventive measures
- 🟡 **Moderate risk** - Requires special attention
- 🔴 **High risk** - Strict preventive measures needed
- ⚫ **Very high risk** - Recommend postponing travel or taking special precautions

**Output format**:
```markdown
## Destination Health Risk Assessment: Thailand

### Infectious Disease Risks
#### 🔴 Dengue Fever - High Risk
- **Transmission**: Mosquito bites
- **Seasonal**: Year-round
- **Symptoms**: High fever, headache, muscle and joint pain, rash
- **Prevention**: Use mosquito repellent, wear long-sleeved clothing, choose air-conditioned accommodation
- **Data sources**: [WHO](https://www.who.int/ith) | [CDC](https://www.cdc.gov/dengue)

### Food and Water Safety
#### 🟡 Moderate Risk
- Drink bottled water or boiled water
- Avoid ice
- Avoid raw food
- Peel fruit yourself

### Current Outbreak Alerts
No major outbreak alerts at this time
```

---

### 3. Vaccination Needs Analysis

Analyzes vaccination requirements based on destination and travel plans.

**Analysis content**:
- Required vaccinations (e.g., yellow fever)
- Recommended vaccinations (e.g., hepatitis A, typhoid)
- Vaccination timing planning
- Vaccine interaction checks
- Contraindication assessment

**Vaccine list template**:
```json
{
  "vaccine": "Hepatitis A vaccine",
  "status": "completed|planned|not_required|contraindicated",
  "date": "2025-06-15",
  "booster_required": false,
  "notes": "Vaccination completed, provides long-term protection"
}
```

**Timing principles**:
- 4-6 weeks before departure: Complete required vaccinations
- 2-4 weeks before departure: Complete recommended vaccinations
- Some vaccines require multiple doses, plan ahead

---

### 4. Smart Travel Medical Kit Recommendations

Generates a personalized travel medical kit list based on destination health risks and personal health status.

**Kit categories**:

#### Prescription medications
- Personal chronic disease medications (sufficient quantity + extra)
- Malaria prevention medications (if needed)
- Other travel medications prescribed by a doctor

#### Over-the-counter medications
- Anti-diarrheal (loperamide)
- Oral rehydration salts
- Fever/pain reducer (acetaminophen/ibuprofen)
- Antihistamine (loratadine)
- Motion sickness medication
- Antacid

#### Protective items
- Insect repellent (DEET 20-30%)
- Sunscreen (SPF 50+)
- Face masks (N95)

#### First aid supplies
- Bandages
- Antiseptic
- Gauze and bandages
- Thermometer
- Small scissors and tweezers

**Personalized recommendations**:
- Adjust medications based on personal medical history
- Add or remove items based on destination risks
- Consider trip duration and activity type

---

### 5. Drug Interaction Check

Checks for potential interactions between travel medications and personal chronic disease medications.

**Check content**:
- Malaria prevention medications vs. chronic disease medications
- Temporary travel medications vs. regular medications
- Vaccine vs. medication interactions
- Food vs. medication interactions

**Common interactions**:
- Doxycycline vs. antacids, calcium/iron supplements
- Mefloquine vs. certain heart medications
- Certain antibiotics vs. oral contraceptives

**Output**:
```markdown
## Drug Interaction Check Results

### ⚠️ Potential Interactions Found

**Doxycycline ↔ Antacids**
- **Effect**: Antacids reduce doxycycline absorption
- **Recommendation**: Take 2 hours apart
- **Severity**: Moderate

### ✅ No Interactions
- Amlodipine vs. travel medications: No known interactions
```

---

### 6. Multilingual Emergency Information Card Generation

Generates multilingual emergency cards with key medical information.

**Supported languages**:
- English (en)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- French (fr)
- Spanish (es)
- Thai (th)
- Vietnamese (vi)

**Card content** (bilingual example — Chinese/English):
```markdown
---
EMERGENCY MEDICAL INFORMATION
---

Name: Zhang San | DOB: 1990-01-01
Blood Type: A+

⚠️ ALLERGIES
- Penicillin (Severe: Rash, Difficulty breathing)

CURRENT MEDICATIONS
- Amlodipine 5mg Once daily (Blood pressure)

MEDICAL CONDITIONS
- Hypertension (Controlled)

EMERGENCY CONTACT
- Spouse: Li Si +86-138-1234-5678
- Doctor: Dr. Wang +86-10-8765-4321

---
[QR Code: Scan for complete medical records]
---
```

**QR code features**:
- Encodes key medical information summary
- Cloud access link (simulated)
- Supports offline access
- Can be shared with medical personnel

---

### 7. Pre/Post-Trip Health Check

#### Pre-Trip Health Check

**Check content**:
- Personal health status assessment
- Chronic disease condition confirmation
- Medication sufficiency check
- Vaccination confirmation
- Health recommendations

**Output**:
```markdown
## Pre-Trip Health Check Report

### Overall Assessment: ✅ Suitable for Travel

### Health Status
- Blood pressure: Well controlled
- Chronic diseases: Stable
- Medication: Sufficient

### Preparation Completeness
- ✅ Vaccinations: Completed
- ✅ Travel medical kit: Prepared
- ✅ Insurance: Purchased
- ⚠️ Emergency card: Pending generation

### Recommendations
1. Generate multilingual emergency card
2. Bring sufficient chronic disease medication
3. Monitor blood pressure during travel
```

#### Post-Trip Health Monitoring

**Monitoring content**:
- Fever monitoring (continuing 2-4 weeks)
- Gastrointestinal symptoms
- Skin abnormalities
- Other discomfort symptoms

**Incubation period disease reminders**:
- Malaria: May develop months after return
- Dengue fever: Usually 3-14 days
- Typhoid: 1-3 weeks
- Hepatitis A: 2-6 weeks

---

## Data File Operations

### Reading Data
```bash
# Read travel health data
Read: data/travel-health-tracker.json

# Read example data
Read: data-example/travel-health-tracker.json
```

### Writing Data
```bash
# Update travel plans
Write: data/travel-health-tracker.json

# Save health check logs
Write: data/travel-health-logs/pre-trip-assessment-YYYY-MM-DD.json
```

### Data Structure Validation
- Validate required fields exist
- Validate date format is correct
- Validate enum values are valid
- Validate data integrity

---

## WHO/CDC Data Integration

### Static Database (Current Implementation)

Built-in health risk data for common travel destinations:
- Southeast Asia: Dengue fever, hepatitis A, typhoid, malaria
- Africa: Malaria, yellow fever, cholera, meningitis
- South America: Dengue fever, yellow fever, Zika virus
- Middle East: Middle East Respiratory Syndrome (MERS)

**Data updates**: Manual updates, recommended quarterly

### Dynamic Query (Future Expansion)

Planned integrations:
- WHO Outbreak News RSS feed
- CDC Travel Health API
- Local health authority outbreak notifications

---

## Output Format

### Report format
- Markdown format for easy reading
- Structured for programmatic processing
- Includes data source citations
- Includes timestamps

### Log format
```json
{
  "log_id": "log_20250728_pretrip",
  "log_type": "pre_trip_assessment",
  "trip_id": "trip_20250801_seasia",
  "generated_at": "2025-07-28T10:00:00.000Z",
  "assessment_results": {
    "health_status": "suitable_for_travel",
    "vaccination_status": "completed",
    "risk_assessment": {...},
    "recommendations": [...]
  }
}
```

---

## Security and Privacy

### Data Protection
- Passport numbers stored with encryption
- QR codes do not contain complete sensitive information
- Supports data export and deletion

### Medical Safety
- All recommendations include disclaimers
- Emphasizes the necessity of physician consultation
- Does not provide specific prescriptions
- References authoritative data sources

---

## Usage Examples

### Analyze a travel plan
```
Input: "Planning to travel to Southeast Asia for 14 days in August 2025"

Output:
1. Destination health risk assessment
2. Vaccination recommendations
3. Travel medical kit list
4. Preventive measures
5. Timeline
```

### Generate emergency card
```
Input: "Generate emergency card in English, Chinese, Japanese, and Thai"

Output:
1. Multilingual card text
2. QR code (description)
3. Storage recommendations
```

### Assess health risks
```
Input: "Assess health risks in Thailand"

Output:
1. Infectious disease risk list
2. Food and water safety recommendations
3. Environmental risks
4. Current outbreak alerts
5. WHO/CDC reference links
```

---

**Version**: v1.0.0
**Last updated**: 2025-01-08
**Maintainer**: WellAlly Tech
