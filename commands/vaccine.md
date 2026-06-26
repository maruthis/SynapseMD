---
description: Manage vaccination records and schedules
arguments:
  - name: action
    description: "Action type: add (add vaccination plan) / record (record vaccination) / schedule (view schedule) / due (pending vaccinations) / history (vaccination history) / status (vaccination statistics) / check (pre-vaccination safety check)"
    required: true
  - name: info
    description: Vaccine information (vaccine name, dose number, date, etc., in natural language)
    required: false
  - name: date
    description: "Vaccination date or query date (format: YYYY-MM-DD, defaults to today)"
    required: false
---

# Vaccination Management

Manage vaccination records and schedules, with support for multi-dose vaccine tracking, schedule management, adverse reaction recording, and safety checks.

## Action Types

### 1. Add Vaccination Plan - `add`

Add a new vaccination plan or record a vaccine that has already been administered.

**Parameter description:**
- `info`: Vaccine information (required), described in natural language
- `date`: Vaccination date (optional), format YYYY-MM-DD, defaults to today

**Examples:**
```
/vaccine add hepatitis B vaccine 0-1-6 schedule first dose given yesterday
/vaccine add HPV vaccine first dose 2025-10-15 second dose planned 2025-12-15
/vaccine add influenza vaccine administered 2025-10-01
/vaccine add COVID-19 vaccine first dose administered today
```

**Supported description formats:**
- Vaccine name + vaccination schedule (0-1-6, 2-6, etc.)
- Administered dose information (which dose, date, site, facility)
- Planned information (planned dates for subsequent doses)
- Detailed information (manufacturer, lot number, doctor, etc.)

### 2. Record Vaccination - `record`

Record an actual vaccination.

**Parameter description:**
- `info`: Vaccination information (required), described in natural language
- `date`: Vaccination date (optional), format YYYY-MM-DD, defaults to today

**Examples:**
```
/vaccine record hepatitis B vaccine dose 2 today left upper arm
/vaccine record influenza vaccine today community health center
/vaccine record HPV dose 2 2025-12-15 right upper arm Dr. Li
```

**Supported description formats:**
- Vaccine name + dose number + date + injection site
- Vaccine name + date + facility
- Vaccine name + dose number + detailed information

### 3. View Vaccination Schedule - `schedule`

View the vaccination schedule and upcoming vaccinations.

**Examples:**
```
/vaccine schedule
/vaccine schedule 2025-12
/vaccine schedule 2026-01
```

### 4. View Pending Vaccinations - `due`

Quickly view pending and overdue vaccinations.

**Examples:**
```
/vaccine due
/vaccine due overdue
/vaccine due upcoming
```

### 5. View Vaccination History - `history`

View vaccination history records.

**Parameter description:**
- No parameter: display all history
- `date`: Month (YYYY-MM format)

**Examples:**
```
/vaccine history
/vaccine history 2025-10
/vaccine history 2025-12
```

### 6. View Vaccination Statistics - `status`

View vaccination statistics and coverage rates.

**Examples:**
```
/vaccine status
/vaccine status coverage
```

### 7. Pre-Vaccination Safety Check - `check`

Perform a comprehensive safety check before vaccination.

**Parameter description:**
- `info`: Vaccine name (required)

**Examples:**
```
/vaccine check hepatitis B vaccine
/vaccine check influenza vaccine
/vaccine check HPV vaccine
```

## Execution Steps

### Add Vaccination Plan (add)

#### 1. Parse Vaccine Information

Extract from natural language:

**Basic information:**
- **Vaccine name**: Name in any language
- **Vaccination schedule**: 0-1-6, 2-6, single dose, etc.
- **Dose information**: which dose, doses administered, total doses
- **Vaccination date**: date administered or planned date

**Detailed information (optional):**
- **Manufacturer**: vaccine producer
- **Lot number**: vaccine lot number
- **Injection site**: left upper arm, right upper arm, etc.
- **Facility**: name of medical institution
- **Administering provider**: doctor or nurse name
- **Adverse reactions**: reactions after vaccination

#### 2. Find Vaccine in Database

Match the vaccine from `data/reference/vaccine-database.json`:

**Matching rules:**
- Exact match: vaccine name is identical
- Alias match: use the aliases field
- Fuzzy match: partial name match

#### 3. Pre-Vaccination Safety Check

**Important: A comprehensive safety check must be performed before saving vaccine information.**

##### 3.1 Allergy Check

Check process:

```javascript
// Pseudocode example
function checkVaccineAllergies(vaccine) {
  const allergies = loadAllergies('data/allergies.json');
  const warnings = [];

  for (const allergy of allergies.allergies) {
    if (allergy.current_status.status !== 'active') continue;

    // Check for allergens in vaccine contraindications
    const isContraindication = vaccine.contraindications.some(c =>
      c.type === 'allergy' && c.allergen === allergy.allergen.name
    );

    if (isContraindication) {
      warnings.push({
        allergen: allergy.allergen.name,
        severity: allergy.severity.level,
        reactions: allergy.reactions,
        recommendation: getRecommendation(allergy.severity.level)
      });
    }
  }

  return warnings;
}

function getRecommendation(severityLevel) {
  const recommendations = {
    'mild': 'May vaccinate; observation required',
    'moderate': 'Vaccinate with caution; consult physician',
    'severe': 'Not recommended; consult specialist',
    'anaphylaxis': 'Absolute contraindication; do not vaccinate'
  };
  return recommendations[severityLevel];
}
```

**Warning output format:**

```
🔍 Pre-Vaccination Safety Check

Vaccine: Hepatitis B Vaccine (Recombinant)
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Allergy History Check
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Passed

Check results:
• No relevant allergy history
• Vaccine components: recombinant HBsAg, aluminum hydroxide, thimerosal
• No matching allergens

2️⃣ Age Appropriateness Check
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Passed

Current age: 35 years old
Recommended age: Any age
Assessment: Suitable for vaccination

3️⃣ Current Health Status Check
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Note

Recent symptom records:
• Fever (2025-12-28) — Recovered 3 days ago
Assessment: Recovered; vaccination is appropriate

4️⃣ Drug Interaction Check
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 1 potential interaction found

Current medications:
• Cyclosporine 100 mg twice daily (immunosuppressant)

Impact: May reduce vaccine immune response
Recommendations:
• Check antibody titer 2–3 months after vaccination
• Consider a booster dose if antibody titer is insufficient
• Consult a specialist

5️⃣ Vaccination History Check
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Vaccination records found

Hepatitis B vaccine history:
• Dose 1: 2025-11-15 ✅
• Dose 2: 2025-12-15 ✅
• Dose 3: Pending (planned 2026-05-15)

Current planned vaccination: Dose 3

6️⃣ Contraindication Check
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No contraindications

Checked items:
• Severe acute febrile illness: ❌ None
• Allergy to vaccine components: ❌ None
• Previous severe allergic reaction: ❌ None
• Pregnancy: ❌ No

━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall assessment: ✅ Vaccination is appropriate
━━━━━━━━━━━━━━━━━━━━━━━━━━

Precautions:
• Remain for observation for 30 minutes after vaccination
• Record any adverse reactions promptly
• Antibody check recommended 2 months after vaccination
• Keep injection site clean and dry

Would you like to proceed with adding the vaccination plan?
A. Proceed
B. Cancel
```

**Handling process:**
- User selects A: Proceed to add vaccination plan
- User selects B: Cancel

##### 3.2 Age Appropriateness Check

```javascript
function checkAgeAppropriateness(vaccine, birthDate) {
  const age = calculateAge(birthDate);
  const recommendation = vaccine.age_recommendations;

  if (age < recommendation.min_age) {
    return {
      appropriate: false,
      reason: `Too young; vaccination recommended after ${recommendation.min_age}`
    };
  }

  if (recommendation.max_age && age > recommendation.max_age) {
    return {
      appropriate: false,
      reason: 'Exceeds recommended maximum age'
    };
  }

  return {
    appropriate: true,
    recommended_age: recommendation.recommended_age
  };
}
```

##### 3.3 Drug Interaction Check

```javascript
function checkVaccineInteractions(vaccine) {
  const medications = loadMedications();
  const interactions = [];

  for (const vaccineInteraction of vaccine.interactions) {
    const matchingMeds = medications.filter(med =>
      med.active && med.category === vaccineInteraction.drug_category
    );

    if (matchingMeds.length > 0) {
      interactions.push({
        drugs: matchingMeds.map(m => m.name),
        interaction: vaccineInteraction
      });
    }
  }

  return interactions;
}
```

#### 4. Generate Vaccination Schedule

Generate a vaccination schedule based on vaccine type:

**Multi-dose vaccines (e.g. hepatitis B 0-1-6):**
- Create records for multiple doses
- Calculate the scheduled date for each dose
- Mark administered and pending doses

**Annual vaccines (e.g. influenza):**
- Create an annual record
- Mark the next vaccination time (one year later)

**Single-dose vaccines:**
- Create a single record
- Mark as completed or scheduled

**Schedule generation algorithm:**

```javascript
function generateVaccineSchedule(vaccine, firstDoseDate) {
  const schedule = [];

  const scheduleTypes = {
    '0-1-6': [
      { dose: 1, offset: 0, unit: 'months' },
      { dose: 2, offset: 1, unit: 'months' },
      { dose: 3, offset: 6, unit: 'months' }
    ],
    '0-2-6': [
      { dose: 1, offset: 0, unit: 'months' },
      { dose: 2, offset: 2, unit: 'months' },
      { dose: 3, offset: 6, unit: 'months' }
    ],
    '2-6': [
      { dose: 1, offset: 2, unit: 'months' },
      { dose: 2, offset: 6, unit: 'months' }
    ],
    'annual': [
      { dose: 1, offset: 1, unit: 'years' }
    ],
    'single': [
      { dose: 1, offset: 0, unit: 'days' }
    ]
  };

  const pattern = scheduleTypes[vaccine.standard_schedule];

  for (const doseInfo of pattern) {
    const scheduledDate = addOffset(firstDoseDate, doseInfo.offset, doseInfo.unit);
    const isFirstDose = doseInfo.dose === 1;

    schedule.push({
      dose_number: doseInfo.dose,
      scheduled_date: formatDate(scheduledDate),
      administered_date: isFirstDose && firstDoseDate <= new Date() ? formatDate(firstDoseDate) : null,
      status: isFirstDose && firstDoseDate <= new Date() ? 'completed' : 'scheduled'
    });
  }

  return schedule;
}
```

#### 5. Save Vaccine Information

**File path:**
`data/vaccinations.json`

**JSON data structure:**

```json
{
  "created_at": "2025-12-31T12:34:56.789Z",
  "last_updated": "2025-12-31T12:34:56.789Z",

  "vaccination_records": [
    {
      "id": "vax_20251231123456789",

      "vaccine_info": {
        "name": "Hepatitis B Vaccine",
        "type": "recombinant",
        "trade_name": "Recombinant Hepatitis B Vaccine",
        "manufacturer": "Beijing Biological Products Institute",
        "batch_number": "202512001",
        "dose_form": "injection",
        "dose_volume": {
          "value": 0.5,
          "unit": "ml"
        },
        "route": "intramuscular",
        "route_name": "Intramuscular injection"
      },

      "series_info": {
        "is_series": true,
        "series_type": "primary",
        "total_doses": 3,
        "current_dose": 2,
        "schedule_type": "0-1-6",
        "schedule_name": "0-1-6 month schedule"
      },

      "doses": [
        {
          "dose_number": 1,
          "scheduled_date": "2025-11-15",
          "administered_date": "2025-11-15",
          "administration_time": "2025-11-15T10:30:00",
          "site": "left_arm",
          "site_name": "Left upper arm, deltoid",
          "facility": "Community Health Center",
          "provider": "Dr. Wang",
          "lot_number": "202512001",
          "status": "completed"
        },
        {
          "dose_number": 2,
          "scheduled_date": "2025-12-15",
          "administered_date": "2025-12-16",
          "administration_time": "2025-12-16T09:00:00",
          "site": "right_arm",
          "site_name": "Right upper arm, deltoid",
          "facility": "Community Health Center",
          "provider": "Nurse Li",
          "lot_number": "202512045",
          "status": "completed"
        },
        {
          "dose_number": 3,
          "scheduled_date": "2026-05-15",
          "administered_date": null,
          "administration_time": null,
          "site": null,
          "site_name": null,
          "facility": null,
          "provider": null,
          "lot_number": null,
          "status": "scheduled"
        }
      ],

      "adverse_reactions": [
        {
          "dose_number": 1,
          "reactions": [
            {
              "reaction": "Injection site pain",
              "severity": "mild",
              "onset_time": "Within 6 hours of vaccination",
              "duration": "2 days",
              "treatment": "No treatment required"
            }
          ]
        }
      ],

      "safety_checks": {
        "allergy_warnings": [],
        "drug_interactions": [],
        "age_appropriate": true,
        "contraindications": []
      },

      "status": {
        "series_status": "in_progress",
        "completion_percentage": 66.7,
        "next_dose_due": "2026-05-15",
        "is_overdue": false
      },

      "metadata": {
        "created_at": "2025-11-15T10:30:00.000Z",
        "last_updated": "2025-12-16T09:00:00.000Z",
        "notes": ""
      }
    }
  ],

  "statistics": {
    "total_vaccination_records": 15,
    "total_doses_administered": 42,
    "series_completed": 8,
    "series_in_progress": 4,
    "single_doses": 3,
    "overdue_count": 1,
    "upcoming_30_days": 3,
    "adverse_reactions_count": 5,
    "severe_reactions_count": 0,
    "last_updated": "2025-12-31T12:34:56.789Z"
  }
}
```

#### 6. Output Confirmation

```
✅ Vaccination plan added

Vaccine information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Vaccine name: Hepatitis B Vaccine (Recombinant)
Vaccination schedule: 0-1-6 month schedule

Administered doses:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Dose 1: 2025-11-15 ✅ Left upper arm, deltoid
Dose 2: 2025-12-16 ✅ Right upper arm, deltoid

Pending doses:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Dose 3: 2026-05-15 (Scheduled)

Progress: 2/3 (66.7%)

💡 Notes:
• Dose 3 should be administered around 2026-05-15
• Can be given up to 2 weeks early or 1 month late
• Post-vaccination antibody testing is recommended to confirm immune response
```

### Record Vaccination (record)

#### 1. Identify Vaccination Information

Extract from natural language:
- **Vaccine name**: vaccine to be recorded
- **Dose number**: which dose
- **Vaccination date**: date administered (defaults to today)
- **Injection site**: left upper arm, right upper arm, etc.
- **Facility**: name of medical institution
- **Provider**: doctor or nurse name

#### 2. Find Vaccination Record

Find the corresponding vaccination plan record based on vaccine name and dose number.

#### 3. Update Dose Information

Update the detailed information for the corresponding dose:
- Set `administered_date`
- Record `administration_time`
- Update `site`, `facility`, `provider`
- Change `status` to "completed"

#### 4. Record Adverse Reactions

```
📋 Post-Vaccination Reaction Record

Vaccine: Hepatitis B Vaccine — Dose 2
Vaccination time: 2025-12-31 10:30

Any adverse reactions?
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. No adverse reactions
2. Injection site pain / redness / swelling
3. Fever
4. Rash / itching
5. Other reactions

Please select or describe the reaction:
```

Record adverse reaction information based on user's selection.

#### 5. Calculate Progress and Next Dose

- Update `current_dose`
- Calculate completion percentage
- Determine the scheduled date for the next dose
- Update series status

#### 6. Output Confirmation

```
✅ Vaccination record updated

Vaccine: Hepatitis B Vaccine
Dose: 2
Vaccination time: 2025-12-31 10:30
Injection site: Left upper arm, deltoid
Facility: Community Health Center

Progress: 2/3 (66.7%)
Next dose: Dose 3, planned 2026-05-15

💡 Notes:
• The next dose can be given up to 2 weeks early or 1 month late
• Aim to complete between 2026-04-15 and 2026-06-15
```

### View Vaccination Schedule (schedule)

#### 1. Load All Vaccination Records

Read all records from `data/vaccinations.json`.

#### 2. Calculate Scheduled Dates and Status

- Calculate the next scheduled dose date for each vaccine
- Determine whether any doses are overdue
- Sort by date

#### 3. Output Format

```
📅 Vaccination Schedule

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Overdue (1 item)
━━━━━━━━━━━━━━━━━━━━━━━━━━

Hepatitis B Vaccine — Dose 3
  ━━━━━━━━━━━━━━━━━━━━━━━━━━
  Scheduled date: 2025-12-20 (11 days overdue)
  Status: 🔴 Overdue

  Recommendation:
  • Get the dose as soon as possible; no need to restart the schedule
  • Contact a vaccination site to make an appointment

━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Coming up (within 30 days, 2 items)
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. HPV Vaccine — Dose 2
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Scheduled date: 2026-01-15 (15 days away)
   Injection site: Right arm recommended
   Appointment note: Book 1 week in advance

2. Influenza Vaccine (Annual booster)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Scheduled date: 2026-01-30 (30 days away)
   Note: Best administered before flu season

━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Future schedule
━━━━━━━━━━━━━━━━━━━━━━━━━━

• Hepatitis B Vaccine — Dose 3: Overdue; needs to be caught up
• HPV Vaccine — Dose 3: Planned 2026-04-15
• Tdap booster: Planned 2026-06-01
```

### View Pending Vaccinations (due)

Simplified view of pending and overdue vaccinations.

**Output format:**

```
⚠️ Vaccination Reminder

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Urgent (Overdue)
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Hepatitis B Vaccine Dose 3
   Overdue: 11 days (was due: 2025-12-20)
   💡 Get this dose as soon as possible

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Due soon (within 7 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━
None

━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Coming up (within 30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. HPV Vaccine Dose 2 — 15 days away
2. Influenza Vaccine — 30 days away

━━━━━━━━━━━━━━━━━━━━━━━━━━
Action recommendations:
• Contact a vaccination site immediately to catch up on the overdue dose
• Book an appointment for upcoming vaccines
```

### View Vaccination History (history)

#### 1. Load Vaccination Records

Read all completed vaccination records.

#### 2. Sort by Date

Sort by vaccination date, most recent first.

#### 3. Output Format

```
📋 Vaccination History

━━━━━━━━━━━━━━━━━━━━━━━━━━
December 2025 (2 records)
━━━━━━━━━━━━━━━━━━━━━━━━━━

12-31  HPV Vaccine Dose 2 ✅
       Site: Right upper arm, deltoid
       Location: Community Health Center
       Reaction: Mild injection site pain (1 day)

12-15  Hepatitis B Vaccine Dose 2 ✅
       Lot number: 202512045
       Location: Community Health Center

━━━━━━━━━━━━━━━━━━━━━━━━━━
November 2025 (1 record)
━━━━━━━━━━━━━━━━━━━━━━━━━━

11-15  Hepatitis B Vaccine Dose 1 ✅
       Lot number: 202512001
       Location: Community Health Center

━━━━━━━━━━━━━━━━━━━━━━━━━━
October 2025 (2 records)
━━━━━━━━━━━━━━━━━━━━━━━━━━

10-15  HPV Vaccine Dose 1 ✅
       Lot number: 202510012
10-01  Influenza Vaccine ✅
       Lot number: 202509088

━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 42 doses
Series completed: 8
In progress: 4
```

### View Vaccination Statistics (status)

#### 1. Calculate Statistics

- Total doses administered
- Number of series completed
- Number of series in progress
- Adverse reaction statistics
- On-time vaccination rate

#### 2. Output Format

```
📊 Vaccination Statistics

Overall:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total doses: 42
Vaccine types: 15
Series completed: 8
In progress: 4
Single-dose vaccines: 3

━━━━━━━━━━━━━━━━━━━━━━━━━━
Series Progress
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Hepatitis B Vaccine (3/3) 100%
   Completed: 2025-11-15

✅ HPV Vaccine (2/3) 66.7%
   Next: 2026-01-15

⚠️ DTaP Vaccine (1/3) 33.3%
   Status: Overdue; catch-up needed urgently

━━━━━━━━━━━━━━━━━━━━━━━━━━
Adverse Reactions
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total reactions: 5
• Mild: 5
• Moderate: 0
• Severe: 0

Common reactions:
• Injection site pain: 3 times
• Fever: 1 time
• Fatigue: 1 time

━━━━━━━━━━━━━━━━━━━━━━━━━━
Vaccination Timeliness
━━━━━━━━━━━━━━━━━━━━━━━━━━
On time: 38 doses (90.5%)
Delayed: 4 doses (9.5%)
Missed / overdue: 1 dose

━━━━━━━━━━━━━━━━━━━━━━━━━━
Immunization Coverage Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Childhood routine immunizations: Completed
✅ Adult routine immunizations: Good
⚠️ Recommended vaccines: Some missing
  • Shingles vaccine: Not administered (recommended for age 50+)
  • Pneumococcal vaccine: Not administered (recommended for age 65+)

💡 Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Prioritize catching up on the overdue DTaP vaccine
• Consider the shingles vaccine (if age-eligible)
• Get the influenza vaccine every autumn
```

### Pre-Vaccination Safety Check (check)

#### 1. Load Vaccine Information

Retrieve detailed vaccine information from the database.

#### 2. Perform Safety Check

- Allergy check
- Age appropriateness check
- Current health status check
- Drug interaction check
- Vaccination history check
- Contraindication check

#### 3. Output Format

(See the "Pre-Vaccination Safety Check" example output above)

## Vaccine Database

### Data Structure

**File path:** `data/reference/vaccine-database.json`

```json
{
  "version": "1.0.0",
  "created_at": "2025-12-31T12:34:56.789Z",
  "last_updated": "2025-12-31T12:34:56.789Z",

  "vaccines": [
    {
      "id": "hepb",
      "name": "Hepatitis B Vaccine",
      "english_name": "Hepatitis B Vaccine",
      "aliases": ["Hep B vaccine", "HepB", "Recombinant Hepatitis B Vaccine"],
      "type": "recombinant",
      "manufacturers": ["Beijing Biological Products Institute", "Kangtai Biological Products", "GlaxoSmithKline"],

      "schedule": {
        "is_series": true,
        "series_type": "primary",
        "standard_schedule": "0-1-6",
        "doses": [
          {
            "dose_number": 1,
            "timing": "birth",
            "timing_description": "Within 24 hours of birth",
            "recommended_age": "Birth",
            "min_age": "0 months",
            "max_age": null
          },
          {
            "dose_number": 2,
            "timing": "1_month_after_dose1",
            "timing_description": "1 month after dose 1",
            "interval_after_previous_dose": {
              "value": 1,
              "unit": "months"
            },
            "recommended_age": "1 month",
            "min_interval": "4 weeks"
          },
          {
            "dose_number": 3,
            "timing": "6_months_after_dose1",
            "timing_description": "6 months after dose 1",
            "interval_after_previous_dose": {
              "value": 5,
              "unit": "months"
            },
            "recommended_age": "6 months",
            "min_interval": "16 weeks",
            "grace_period": "4 weeks"
          }
        ],
        "booster": {
          "required": false,
          "indications": ["High-risk groups", "Immunocompromised"],
          "interval": "5 years"
        }
      },

      "contraindications": [
        {
          "type": "allergy",
          "allergen": "Yeast",
          "severity": "severe",
          "description": "Persons with severe allergy to any vaccine component (including yeast)"
        },
        {
          "type": "disease",
          "condition": "Severe acute febrile illness",
          "severity": "temporary",
          "description": "Defer vaccination during fever"
        }
      ],

      "age_recommendations": {
        "recommended_age": "At birth",
        "min_age": "0 months",
        "max_age": null,
        "catch_up_schedule": "Can begin vaccination at any age"
      },

      "interactions": [
        {
          "drug_category": "Immunosuppressants",
          "interaction_type": "reduced_efficacy",
          "severity": "moderate",
          "description": "Immunosuppressants may reduce vaccine immune response"
        }
      ],

      "common_adverse_reactions": [
        {
          "reaction": "Injection site pain",
          "frequency": "common",
          "severity": "mild",
          "onset": "Within 24 hours of vaccination",
          "duration": "1–3 days"
        },
        {
          "reaction": "Fever",
          "frequency": "occasional",
          "severity": "mild_to_moderate",
          "onset": "6–24 hours after vaccination",
          "duration": "1–2 days"
        }
      ],

      "special_populations": {
        "pregnancy": {
          "recommendation": "safe",
          "notes": "Safe to administer during pregnancy"
        },
        "lactation": {
          "recommendation": "safe",
          "notes": "Safe to administer while breastfeeding"
        },
        "immunocompromised": {
          "recommendation": "recommended",
          "notes": "More important for immunocompromised individuals"
        }
      }
    }
  ],

  "categories": {
    "routine_childhood": ["hepb", "bcg", "polio", "dpt", "mmr", "varicella"],
    "routine_adult": ["influenza", "tdap", "pneumococcal", "shingles", "covid"],
    "travel": ["hepa", "typhoid", "yellow_fever", "japanese_encephalitis"],
    "high_risk": ["pneumococcal", "meningococcal", "hib"]
  }
}
```

## Intelligent Recognition Rules

### Vaccine Name Recognition

**Common vaccines:**
- Hepatitis B vaccine, HepB, Hep B
- Influenza vaccine, Flu vaccine, Flu shot
- HPV vaccine, cervical cancer vaccine, human papillomavirus vaccine
- COVID-19 vaccine, coronavirus vaccine
- DTaP vaccine, DPT
- MMR vaccine (measles, mumps, rubella)
- Polio vaccine, IPV
- BCG vaccine (tuberculosis)
- Pneumococcal vaccine
- Shingles vaccine, zoster vaccine

### Dose Number Recognition

| User input | Standardized |
|-----------|-------------|
| Dose 1, first dose, 1st dose | dose_number: 1 |
| Dose 2, second dose, 2nd dose | dose_number: 2 |
| Dose 3, third dose, 3rd dose | dose_number: 3 |

### Vaccination Schedule Recognition

| User input | Standardized | Total doses |
|-----------|-------------|-------------|
| 0-1-6, 016 schedule | 0-1-6 | 3 doses |
| 0-2-6, 026 schedule | 0-2-6 | 3 doses |
| 2 doses, 2-dose | 2-dose | 2 doses |
| 3 doses, 3-dose | 3-dose | 3 doses |
| single dose, once | single | 1 dose |

### Injection Site Recognition

| User input | Standardized |
|-----------|-------------|
| Left upper arm, left arm | left_arm |
| Right upper arm, right arm | right_arm |
| Left thigh | left_thigh |
| Right thigh | right_thigh |
| Buttock, gluteal injection | buttock |

### Date Recognition

| User input | Standardized |
|-----------|-------------|
| Today, this day | Current date |
| Yesterday | Current date − 1 day |
| Tomorrow | Current date + 1 day |
| YYYY-MM-DD | Standard date format |
| Month D | That date in the current year |
| In X weeks / X months | Calculated date |

## Data Structure Update

Add to the global index `data/index.json`:

```json
{
  "vaccination_records": "data/vaccinations.json",
  "vaccine_database": "data/reference/vaccine-database.json",
  "statistics": {
    "vaccination_count": 0
  }
}
```

## Integration with Other Systems

### Integration with Allergy System

Automatically check `data/allergies.json` before vaccination:

1. Read active allergy records
2. Check for allergens in vaccine contraindications
3. Display warnings by severity
4. Provide vaccination recommendations

### Integration with Profile System

Retrieve date of birth from `data/profile.json` for:
- Age appropriateness checks
- Age-related vaccine recommendations
- Vaccination schedule determination

### Interaction with Medication System

Check current medications for interactions with vaccines:
- Immunosuppressants: may reduce vaccine response
- Anticoagulants: injection site care recommendations
- Other interactions

## Statistical Calculations

### Completion Rate Calculation

```javascript
completion_percentage = (current_dose / total_doses) * 100
```

### Overdue Determination

```javascript
is_overdue = (scheduled_date < today) && (status === 'scheduled')
```

### On-Time Vaccination Rate

```javascript
timeliness_rate = (on_time_doses / total_doses) * 100
```

### Adverse Reaction Rate

```javascript
reaction_rate = (doses_with_reactions / total_doses) * 100
```

## Notes

- This system is for personal vaccination record-keeping only and cannot replace professional medical advice
- Consult a physician or vaccination site staff before vaccination
- Always inform the vaccinator if you have a serious allergy history
- Remain for observation for 30 minutes after vaccination
- All data is stored locally only
- Important vaccination records should be shared with your doctor

## Example Usage

```bash
# Add hepatitis B vaccination plan
/vaccine add hepatitis B vaccine 0-1-6 schedule first dose given yesterday

# Add HPV vaccination plan
/vaccine add HPV vaccine first dose 2025-10-15 second dose planned 2025-12-15

# Record actual vaccination
/vaccine record hepatitis B vaccine dose 2 today left upper arm
/vaccine record influenza vaccine today community health center

# View vaccination schedule
/vaccine schedule

# View pending vaccinations
/vaccine due

# View vaccination history
/vaccine history
/vaccine history 2025-10

# View vaccination statistics
/vaccine status

# Pre-vaccination safety check
/vaccine check hepatitis B vaccine
```

## Error Handling

- **Vaccine information empty**: "Please provide vaccine information, e.g.: /vaccine add hepatitis B vaccine dose 1"
- **Vaccine not recognized**: "Vaccine not recognized. Please provide the full vaccine name."
- **Vaccination plan already exists**: "A vaccination plan for this vaccine already exists. Use /vaccine record to log a dose."
- **No vaccination records**: "No vaccination records found"
- **Vaccine database not found**: "Vaccine database not found. Please create it first."
- **Storage failure**: "Failed to save record. Please check storage space."
