---
description: Manage COPD lung function monitoring, symptom assessment, and acute exacerbation records
arguments:
  - name: action
    description: Action type：fev1(lung function)/cat(CAT score)/mmrc(mMRC score)/symptom(symptom record)/exacerbation(acute exacerbation)/medication(medication management)/vaccine(vaccination)/status(control status)/assessment(GOLD grouping)
    required: true
  - name: info
    description: Detailed information (FEV1 value, CAT score, symptom description, etc., natural language description)
    required: false
---

# COPD (Chronic Obstructive Pulmonary Disease) Management

Long-term management of Chronic Obstructive Pulmonary Disease (COPD), including lung function monitoring, symptom assessment, and acute exacerbation prevention.

## ⚠️ Medical Safety Statement

**Important: This system is for health monitoring records only and cannot replace professional medical diagnosis and treatment.**

- ❌ Does not provide specific medication dosage adjustment recommendations
- ❌ Does not directly prescribe or recommend specific medications
- ❌ Does not replace physician diagnosis and treatment decisions
- ❌ Does not make prognosis judgments or predict lung function decline rates
- ✅ Provides lung function monitoring records and trend analysis (for reference only)
- ✅ Provides symptom scoring and assessment (CAT, mMRC)
- ✅ Provides acute exacerbation records and trigger tracking
- ✅ Provides medication reminders and vaccination reminders
- ✅ Provides lifestyle advice and medical consultation reminders

All medication regimens and treatment decisions should follow physician guidance.

## Operation Types

### 1. Record Lung Function - `fev1`

Record pulmonary function test results.

**Parameter Description:**
- `info`: Lung function information (required), described in natural language

**Examples:**
```
/copd fev1 1.8 65%
/copd lung-function fvc 3.2 ratio 0.56
/copd fev1 2.1 70% fvc 3.5 ratio 0.60
/copd lung-function 2025-06-15 fev1 1.8 predicted 65%
```

**Supported indicators:**
- **fev1**: Forced expiratory volume in one second (L)
- **predicted**: FEV1 as a percentage of predicted value (%)
- **fvc**: Forced vital capacity (L)
- **ratio**: FEV1/FVC ratio

**COPD diagnostic criteria:**
- FEV1/FVC < 0.70 (post-bronchodilator)
- Indicates the presence of airflow limitation

**GOLD classification (based on FEV1 % predicted):**
| Grade | FEV1 % Predicted | Severity |
|------|-------------|---------|
| Grade 1 | ≥80% | Mild |
| Grade 2 | 50-79% | Moderate |
| Grade 3 | 30-49% | Severe |
| Grade 4 | <30% | Very severe |

### 2. CAT Score - `cat`

Conduct the COPD Assessment Test (CAT).

**Examples:**
```
/copd cat
/copd cat score 18
/copd cat 2025-06-20 cough 2 sputum 2 chest_tightness 2 breathlessness 3 activity 2 confidence 2 sleep 3 energy 2
```

**CAT scoring items (0-5 points each):**
1. **cough**: Cough
2. **sputum**: Phlegm (sputum)
3. **chest_tightness**: Chest tightness
4. **breathlessness_climbing**: Breathlessness climbing a hill or stairs
5. **activity_limitation**: Limitation doing activities at home
6. **confidence_outdoors**: Confidence leaving home outdoors
7. **sleep**: Sleep quality
8. **energy**: Energy level

**CAT score interpretation:**
| Total Score | Impact | Level |
|------|------|------|
| 0-10 | Mild impact | Low |
| 11-20 | Moderate impact | Medium |
| 21-30 | Severe impact | High |
| 31-40 | Very severe impact | Very high |

### 3. mMRC Score - `mmrc`

Conduct the Modified Medical Research Council (mMRC) Dyspnea Scale assessment.

**Examples:**
```
/copd mmrc 0
/copd mmrc 2
/copd mmrc 2025-06-20 grade 2
```

**mMRC grades (0-4):**
| Grade | Description |
|------|------|
| Grade 0 | Breathless only with strenuous exercise |
| Grade 1 | Breathless when hurrying or walking up a slight hill |
| Grade 2 | Walks slower than people of the same age or stops to catch breath when walking at own pace |
| Grade 3 | Stops to catch breath after walking 100 meters or after a few minutes on level ground |
| Grade 4 | Too breathless to leave the house or breathless when dressing |

**mMRC severity:**
- Grades 0-1: Mild breathlessness
- Grade 2: Moderate breathlessness
- Grades 3-4: Severe breathlessness

### 4. Record Symptoms - `symptom`

Record COPD-related symptoms.

**Examples:**
```
/copd symptom dyspnea moderate
/copd symptom sputum white moderate
/copd symptom wheeze exertion
/copd symptom cough daily productive
/copd symptom dyspnea severe mrc 3
```

**Supported symptom records:**

#### Breathlessness - `dyspnea`
```
/copd symptom dyspnea mild
/copd symptom dyspnea moderate
/copd symptom dyspnea severe
/copd symptom dyspnea mrc 2
```

#### Cough - `cough`
```
/copd symptom cough daily
/copd symptom cough weekly productive
/copd symptom cough dry
```

#### Sputum - `sputum`
```
/copd symptom sputum white moderate
/copd symptom sputum yellow scanty
/copd symptom sputum purulent abundant
```

**Sputum color classification:**
- white: White
- clear: Clear/transparent
- yellow: Yellow
- green: Green
- purulent: Purulent

**Sputum quantity:**
- scanty: Small amount
- moderate: Moderate amount
- abundant: Large amount

#### Wheezing - `wheeze`
```
/copd symptom wheeze exertion
/copd symptom wheeze constant
/copd symptom wheeze none
```

### 5. Record Acute Exacerbation - `exacerbation`

Record COPD acute exacerbation events.

**Examples:**
```
/copd exacerbation moderate
/copd exacerbation severe hospitalized
/copd exacerbation trigger infection recovery 10 days
/copd exacerbation 2025-02-15 moderate viral_infection
/copd exacerbation history
```

**Acute exacerbation severity:**
- **mild**: Managed at home, increased use of short-acting bronchodilators
- **moderate**: Requires oral corticosteroids and/or antibiotics
- **severe**: Requires hospitalization or emergency care

**Common triggers:**
- viral_infection: Viral infection
- bacterial_infection: Bacterial infection
- air_pollution: Air pollution
- weather_change: Temperature changes
- non_adherence: Poor medication adherence

**Acute exacerbation symptoms:**
- increased_dyspnea: Worsening breathlessness
- increased_sputum: Increased sputum
- purulent_sputum: Purulent sputum
- wheezing: Worsening wheezing

**Recovery status:**
```
/copd exacerbation recovery 10 days
/copd exacerbation resolved
/copd exacerbation ongoing 5 days
```

### 6. Medication Management - `medication`

Manage COPD-related medications (integrated with the medication management system).

**Examples:**
```
/copd medication add tiotropium 18μg once-daily handihaler
/copd medication add salbutamol 100μg as-needed
/copd medication list
/copd medication adherence
```

**Common COPD medication types:**
- **LAMA**: Long-acting muscarinic antagonists (e.g., tiotropium)
- **LABA**: Long-acting beta2-agonists (e.g., salmeterol)
- **ICS**: Inhaled corticosteroids (e.g., budesonide)
- **SABA**: Short-acting beta2-agonists (e.g., salbutamol)
- **SAMA**: Short-acting muscarinic antagonists (e.g., ipratropium)

**Execution process:**
1. Parse medication information and device type
2. Call the `/medication add` command to add the medication
3. Add reference record in copd-tracker.json
4. Output confirmation and medication guidance

### 7. Vaccination Record - `vaccine`

Record influenza and pneumococcal vaccine administration.

**Examples:**
```
/copd vaccine flu 2025-10-15
/copd vaccine pneumococcal ppsv23 2024-05-10
/copd vaccine pneumococcal pcv13 2023-03-20
/copd vaccine status
```

**Vaccination recommendations:**

#### Influenza vaccine
- **Annual vaccination**: Before flu season (September-November)
- **Dose**: Standard dose or high dose (≥65 years old)
- **Next vaccination**: Once a year

#### Pneumococcal vaccines
- **PCV13** (13-valent conjugate vaccine): Recommended for all COPD patients
- **PPSV23** (23-valent polysaccharide vaccine): Recommended for all COPD patients
- **Vaccination sequence**: PCV13 first, followed by PPSV23 8 weeks later
- **Re-vaccination**: PPSV23 may be repeated after 5 years (under 65 or high-risk individuals)

### 8. View Control Status - `status`

View the COPD comprehensive control status.

**Examples:**
```
/copd status
```

**Output content:**
- GOLD classification
- Symptom scores (CAT, mMRC)
- Lung function status
- Acute exacerbation frequency
- Medication status
- Vaccination status
- Control assessment

### 9. GOLD Grouping Assessment - `assessment`

Conduct GOLD comprehensive assessment grouping (ABCD grouping).

**Examples:**
```
/copd assessment
```

**GOLD grouping criteria:**

| Group | CAT Score | mMRC Score | Annual Acute Exacerbations |
|------|---------|----------|---------------|
| Group A | <10 | 0-1 | 0-1 |
| Group B | ≥10 | ≥2 | 0-1 |
| Group C | <10 | 0-1 | ≥2 |
| Group D | ≥10 | ≥2 | ≥2 |

**Group treatment recommendations:**
- **Group A**: Use short-acting bronchodilators as needed
- **Group B**: Long-acting bronchodilator (LAMA or LABA)
- **Group C**: Long-acting bronchodilator (LAMA or LABA+LAMA)
- **Group D**: LAMA+LABA±ICS (based on eosinophil level)

## Data Structure

### Lung function structure
```json
{
  "date": "2025-06-10",
  "post_bronchodilator": {
    "fev1": 1.8,
    "fev1_percent_predicted": 65,
    "fvc": 3.2,
    "fev1_fvc_ratio": 0.56
  },
  "interpretation": "Moderate airflow limitation"
}
```

### CAT score structure
```json
{
  "date": "2025-06-20",
  "total_score": 18,
  "max_score": 40,
  "interpretation": "Moderate symptom impact",
  "items": {
    "cough": 2,
    "sputum": 2,
    "chest_tightness": 2,
    "breathlessness_climbing": 3,
    "activity_limitation": 2,
    "confidence_outdoors": 2,
    "sleep": 3,
    "energy": 2
  }
}
```

### Acute exacerbation structure
```json
{
  "id": "exace_20250215000000001",
  "date": "2025-02-15",
  "severity": "moderate",
  "triggers": ["viral_infection"],
  "symptoms": ["increased_dyspnea", "purulent_sputum"],
  "treatment": ["antibiotics", "prednisone"],
  "hospitalized": false,
  "recovery_days": 10,
  "created_at": "2025-02-15T00:00:00.000Z"
}
```

## GOLD Comprehensive Assessment Tool

### Step 1: Lung function assessment (GOLD grades 1-4)
Determine airflow limitation severity based on FEV1 % predicted.

### Step 2: Symptom assessment
- **CAT score**: ≥10 indicates more symptoms
- **mMRC score**: ≥2 indicates more symptoms

### Step 3: Risk assessment
- **Low risk**: 0-1 acute exacerbation/year (not hospitalized)
- **High risk**: ≥2 acute exacerbations/year or ≥1 hospitalization

### Step 4: ABCD grouping
Determine grouping based on symptom assessment and risk assessment.

## Pulmonary Rehabilitation

### Breathing exercises
- **Pursed-lip breathing**: Close mouth, inhale through nose, exhale slowly through pursed lips as if whistling
- **Diaphragmatic breathing**: Abdomen rises when inhaling, abdomen contracts when exhaling
- **Frequency**: 2-3 times per day, 10-15 minutes each time

### Exercise training
- **Aerobic exercise**: Walking, cycling, swimming (3-5 times per week, 30 minutes each)
- **Strength training**: Upper and lower limb strength training (2-3 times per week)
- **Intensity**: Moderate intensity (able to talk but not sing)

### Daily activities
- Energy conservation techniques
- Energy management strategies
- Assistive device use

## Lifestyle Recommendations

### Quit smoking (most important)
- **Stop smoking immediately**: This is the most effective intervention to slow lung function decline
- **Quit smoking support**: Counseling, nicotine replacement therapy, medication
- **Avoid secondhand smoke**: Stay away from smoking environments

### Nutritional support
- **Maintain healthy weight**: BMI 21-25 kg/m²
- **Malnutrition**: Increase calorie and protein intake
- **Obesity**: Lose 5-10% of body weight

### Exercise
- **Regular exercise**: 3-5 times per week, 30 minutes each
- **Types**: Walking, cycling, swimming
- **Pulmonary rehabilitation**: Participate in a pulmonary rehabilitation program

### Environmental control
- **Avoid air pollution**: Reduce outdoor activities on smoggy days
- **Avoid irritating gases**: Smoke, dust, chemical fumes
- **Indoor air**: Maintain ventilation, use air purifiers

### Infection prevention
- **Wash hands frequently**: Wash with soap and water for 20 seconds
- **Wear a mask**: Wear a mask in crowded places
- **Avoid contact**: Stay away from people with colds and flu
- **Vaccinations**: Annual flu vaccine + pneumococcal vaccine

## Medication Guidance

### Inhaler technique

#### Metered-dose inhaler (MDI)
1. Remove cap and shake the inhaler
2. Breathe out to residual volume (not into the inhaler)
3. Place the mouthpiece in your mouth, seal your lips around it
4. Begin to inhale slowly and deeply while pressing the inhaler at the same time
5. Continue inhaling deeply to full lung capacity
6. Hold breath for 10 seconds
7. Exhale slowly
8. If a second puff is needed, wait 1 minute and repeat

#### Dry powder inhaler (DPI)
1. Open the inhaler and load the medication
2. Breathe out to residual volume (not into the inhaler)
3. Place the mouthpiece in your mouth, seal your lips around it
4. Inhale forcefully and quickly
5. Hold breath for 10 seconds
6. Exhale slowly
7. Rinse mouth with water (if the medication contains corticosteroids)

### Nebulizer use
1. Prepare the medication per physician's prescription
2. Pour the medication into the nebulizer cup
3. Connect the nebulizer and power source
4. Use a face mask or mouthpiece
5. Turn on power and inhale the nebulized medication (10-15 minutes)
6. After nebulization, clean the face mask and nebulizer cup

## Medical Consultation Advice

### Emergency care (call 911 immediately)
- Breathing difficulty markedly worsening, not relieved by rest
- Blue lips or fingernails (cyanosis)
- Confusion, drowsiness, or unconsciousness
- Chest pain, suspected myocardial infarction or pneumothorax
- Signs of respiratory failure (PaO2 <60 mmHg or PaCO2 >50 mmHg)

### Seek care soon (within 48 hours)
- Acute exacerbation with progressively worsening symptoms
- Sputum becoming purulent or significantly increased quantity
- Fever (temperature >38.5°C)
- No improvement in symptoms after medication
- New severe symptoms

### Regular follow-up
- **Stable COPD**: Once every 3-6 months
- **Frequent acute exacerbations**: Once every 1-3 months
- **Severe COPD**: Once every 1-2 months
- **Follow-up items**: Lung function, blood gas analysis, chest X-ray

## Acute Exacerbation Recognition

**Definition:**
- Worsening breathlessness
- Increased sputum
- Purulent sputum

**At least 2 of the above symptoms lasting >3 days**

**Home identification methods:**
- **PEF monitoring**: PEF decline >20% suggests acute exacerbation
- **Blood oxygen saturation**: SpO2 <90% suggests hypoxia
- **Symptom diary**: Record daily symptoms to help identify abnormalities

## Acute Exacerbation Home Management

### Mild acute exacerbation
1. **Increase bronchodilators**: Increase frequency of short-acting bronchodilator use
2. **Use a spacer**: Improve medication inhalation efficiency
3. **Rest**: Reduce physical activity
4. **Drink plenty of fluids**: 2-3L of water per day to thin sputum
5. **Monitor**: Closely observe symptom changes

### Moderate acute exacerbation
1. **Above measures**
2. **Oral corticosteroids**: Prednisone 40mg/day × 5 days (as directed by physician)
3. **Antibiotics**: If bacterial infection is suspected (as directed by physician)
4. **Monitor oxygen levels**: SpO2 should be >90%

### Severe acute exacerbation
**Seek medical attention immediately or call 911**

## Error Handling

- **Invalid FEV1 value**: "FEV1 value should be within the normal range (0.5-8.0 L)"
- **Score out of range**: "CAT score should be between 0-40; mMRC score should be between grades 0-4"
- **Incomplete information**: "Please provide complete information, e.g.: /copd fev1 1.8 65%"
- **No data**: "No COPD records yet; please record lung function or symptoms first"
- **File read failure**: "Unable to read COPD data; please check the data file"

## Example Usage

```
# Lung function record
/copd fev1 1.8 65%
/copd lung-function fvc 3.2 ratio 0.56

# Symptom assessment
/copd cat
/copd mmrc 2

# Symptom record
/copd symptom dyspnea moderate
/copd symptom sputum white moderate
/copd symptom wheeze exertion

# Acute exacerbation record
/copd exacerbation moderate
/copd exacerbation trigger infection
/copd exacerbation recovery 10 days
/copd exacerbation history

# Medication management
/copd medication add tiotropium 18μg once-daily
/copd medication list

# Vaccination
/copd vaccine flu 2025-10-15
/copd vaccine pneumococcal ppsv23 2024-05-10

# View status
/copd status
/copd assessment
```

## Notes

- **Quitting smoking is the most important intervention**: Slows lung function decline
- **Use maintenance medications regularly**: Continue even when symptom-free
- **Use inhalers correctly**: Regularly check inhaler technique
- **Regular lung function monitoring**: At least once a year
- **Vaccinations**: Prevent infections and acute exacerbations
- **Develop an action plan**: Define the steps to take during an acute exacerbation
- **Keep a symptom diary**: Helps identify early signs of acute exacerbation

---

**Disclaimer: This system is for health monitoring records only and does not replace professional medical diagnosis and treatment.**
