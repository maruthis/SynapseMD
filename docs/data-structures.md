# Data Structure Reference

## Biochemical Examination Data Structure

```json
{
  "id": "20251231123456789",
  "type": "Biochemical Examination",
  "date": "2025-12-31",
  "hospital": "XX Hospital",
  "items": [
    {
      "name": "White Blood Cell Count",
      "value": "6.5",
      "unit": "×10^9/L",
      "min_ref": "3.5",
      "max_ref": "9.5",
      "is_abnormal": false
    }
  ]
}
```

### Field Descriptions
- `id`: Unique identifier (generated from timestamp)
- `type`: Examination type, fixed as "Biochemical Examination"
- `date`: Examination date (YYYY-MM-DD format)
- `hospital`: Name of the hospital visited
- `items`: Array of examination items
  - `name`: Name of the examination item
  - `value`: Result value
  - `unit`: Unit of measurement
  - `min_ref`: Lower bound of reference range
  - `max_ref`: Upper bound of reference range
  - `is_abnormal`: Whether the result is abnormal (boolean)

## Imaging Examination Data Structure

```json
{
  "id": "20251231123456789",
  "type": "Imaging Examination",
  "subtype": "Ultrasound",
  "date": "2025-12-31",
  "hospital": "XX Hospital",
  "body_part": "Abdomen",
  "findings": {
    "description": "Description of examination findings",
    "measurements": {
      "Size": "Specific value"
    },
    "conclusion": "Examination conclusion"
  },
  "original_image": "images/original.jpg"
}
```

### Field Descriptions
- `id`: Unique identifier (generated from timestamp)
- `type`: Examination type, fixed as "Imaging Examination"
- `subtype`: Imaging subtype (Ultrasound, CT, MRI, X-ray, etc.)
- `date`: Examination date (YYYY-MM-DD format)
- `hospital`: Name of the hospital visited
- `body_part`: Body part examined
- `findings`: Findings object
  - `description`: Text description of examination findings
  - `measurements`: Measurements data object
  - `conclusion`: Examination conclusion
- `original_image`: Path to the original image backup

## Radiation Record Data Structure

```json
{
  "id": "20251231123456789",
  "exam_type": "CT",
  "body_part": "Chest",
  "exam_date": "2025-12-31",
  "standard_dose": 7.0,
  "body_surface_area": 1.85,
  "adjustment_factor": 1.07,
  "actual_dose": 7.5,
  "dose_unit": "mSv"
}
```

### Field Descriptions
- `id`: Unique identifier (generated from timestamp)
- `exam_type`: Examination type (CT, X-ray, PET-CT, etc.)
- `body_part`: Body part examined
- `exam_date`: Examination date (YYYY-MM-DD format)
- `standard_dose`: Standard radiation dose (mSv)
- `body_surface_area`: User's body surface area (m²)
- `adjustment_factor`: Body surface area adjustment factor
- `actual_dose`: Actual radiation dose (mSv)
- `dose_unit`: Dose unit, fixed as "mSv"

## User Profile Data Structure

```json
{
  "basic_info": {
    "gender": "F",
    "height": 175,
    "height_unit": "cm",
    "weight": 70,
    "weight_unit": "kg",
    "birth_date": "1990-01-01"
  },
  "calculated": {
    "age": 35,
    "bmi": 22.9,
    "bmi_status": "Normal",
    "body_surface_area": 1.85,
    "bsa_unit": "m²"
  }
}
```

### Field Descriptions
- `basic_info`: Basic information object
  - `gender`: Gender (M = male, F = female; other values allowed)
  - `height`: Height value
  - `height_unit`: Height unit
  - `weight`: Weight value
  - `weight_unit`: Weight unit
  - `birth_date`: Date of birth (YYYY-MM-DD format)
- `calculated`: Auto-calculated information object
  - `age`: Age (in years)
  - `bmi`: BMI index
  - `bmi_status`: BMI status (Underweight / Normal / Overweight / Obese)
  - `body_surface_area`: Body surface area (calculated using the Mosteller formula)
  - `bsa_unit`: Body surface area unit

## Global Index Data Structure

```json
{
  "biochemical_exams": [
    {
      "id": "20251231123456789",
      "date": "2025-12-31",
      "type": "Biochemical Examination",
      "file_path": "data/biochemical-exams/2025-12/2025-12-31_cbc.json"
    }
  ],
  "imaging_exams": [
    {
      "id": "20251231123456789",
      "date": "2025-12-31",
      "type": "Imaging Examination",
      "subtype": "Ultrasound",
      "file_path": "data/imaging-exams/2025-12/2025-12-31_abdominal-ultrasound.json"
    }
  ],
  "last_updated": "2025-12-31T12:34:56.789Z"
}
```

### Field Descriptions
- `biochemical_exams`: Biochemical examination index array
- `imaging_exams`: Imaging examination index array
- `symptom_records`: Symptom records index array
- `last_updated`: Last updated time (ISO 8601 format)

## Symptom Record Data Structure

```json
{
  "id": "20251231123456789",
  "record_date": "2025-12-31",
  "symptom_date": "2025-12-31",
  "original_input": "User's original natural language input",

  "standardized": {
    "main_symptom": "Headache",
    "category": "Nervous System",
    "body_part": "Head",
    "severity": "Mild",
    "severity_level": 1,
    "characteristics": "Dull, pressure-like pain",
    "onset_time": "2025-12-31T10:00:00",
    "duration": "2 hours",
    "frequency": "First occurrence"
  },

  "associated_symptoms": [
    {
      "name": "Nausea",
      "present": true
    },
    {
      "name": "Vomiting",
      "present": false
    }
  ],

  "triggers": {
    "possible_causes": ["Insufficient sleep", "Mental stress"],
    "aggravating_factors": [],
    "relieving_factors": ["Slight relief after rest"]
  },

  "medical_assessment": {
    "urgency": "observation",
    "urgency_level": 1,
    "recommendation": "Home observation",
    "advice": "Get adequate rest and ensure sufficient sleep. If symptoms worsen or persist beyond 24 hours, seek medical attention.",
    "red_flags": []
  },

  "follow_up": {
    "needs_follow_up": false,
    "follow_up_date": null,
    "improvement": null
  },

  "metadata": {
    "created_at": "2025-12-31T12:34:56.789Z",
    "last_updated": "2025-12-31T12:34:56.789Z"
  }
}
```

### Field Descriptions
- `id`: Unique identifier (generated from timestamp)
- `record_date`: Record creation date (YYYY-MM-DD format)
- `symptom_date`: Date the symptom occurred (YYYY-MM-DD format)
- `original_input`: User's original natural language description
- `standardized`: Standardized medical information object
  - `main_symptom`: Standard medical term for the primary symptom
  - `category`: System classification of the symptom
  - `body_part`: Body part where the symptom occurs
  - `severity`: Severity description (Mild / Moderate / Severe / Critical)
  - `severity_level`: Severity level (1–4)
  - `characteristics`: Description of symptom characteristics
  - `onset_time`: Symptom onset time (ISO 8601 format)
  - `duration`: Duration description
  - `frequency`: Frequency description
- `associated_symptoms`: Array of associated symptoms
  - `name`: Symptom name
  - `present`: Whether this symptom is present (boolean)
- `triggers`: Triggers and relieving factors object
  - `possible_causes`: Array of possible causes
  - `aggravating_factors`: Array of aggravating factors
  - `relieving_factors`: Array of relieving factors
- `medical_assessment`: Medical assessment object
  - `urgency`: Urgency category (observation / outpatient / urgent / emergency)
  - `urgency_level`: Urgency level (1–4)
  - `recommendation`: Medical advice category
  - `advice`: Specific advice content
  - `red_flags`: Array of red flag warning signs
- `follow_up`: Follow-up information object
  - `needs_follow_up`: Whether follow-up is needed (boolean)
  - `follow_up_date`: Follow-up date (if applicable)
  - `improvement`: Improvement status (if applicable)
- `metadata`: Metadata object
  - `created_at`: Record creation time (ISO 8601 format)
  - `last_updated`: Last updated time (ISO 8601 format)

### Urgency Level Classification

- **observation (Level 1)**: Home observation
- **outpatient (Level 2)**: Outpatient visit (within 1 week)
- **urgent (Level 3)**: Seek care promptly (today or tomorrow)
- **emergency (Level 4)**: Seek immediate medical attention or call emergency services

### Symptom System Classification

- Respiratory system: Cough, expectoration, dyspnea, chest pain, etc.
- Cardiovascular system: Palpitations, chest tightness, edema, etc.
- Digestive system: Abdominal pain, nausea, vomiting, diarrhea, constipation, etc.
- Nervous system: Headache, dizziness, insomnia, seizures, etc.
- Urinary system: Frequent urination, urgency, dysuria, hematuria, etc.
- Endocrine system: Polydipsia, polyuria, weight changes, etc.
- Musculoskeletal: Joint pain, muscle pain, limited mobility, etc.
- Systemic symptoms: Fever, fatigue, weight loss, etc.

## Medication Record Data Structure

### Drug Information Data Structure

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
          "timing_label": "After breakfast",
          "dose": {
            "value": 100,
            "unit": "mg"
          }
        },
        {
          "weekday": 2,
          "time": "08:00",
          "timing_label": "After breakfast",
          "dose": {
            "value": 100,
            "unit": "mg"
          }
        }
        ... (continued through Sunday, 7 records total)
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

### Field Descriptions

- `medications`: Medications array
  - `id`: Unique identifier (prefix med_ + timestamp)
  - `name`: Drug name (generic name or brand name)
  - `generic_name`: Generic name
  - `dosage`: Dosage information object
    - `value`: Dosage value
    - `unit`: Dosage unit (mg, g, mL, IU, tablet, capsule, etc.)
  - `frequency`: Dosing frequency object
    - `type`: Frequency type (daily / weekly / every_other_day / as_needed)
    - `times_per_day`: Number of doses per day
    - `interval_days`: Dosing interval in days
  - `schedule`: Dosing schedule array (required to explicitly specify a dosing schedule for each day of the week)
    - `weekday`: Day of the week (1–7, where 1 = Monday and 7 = Sunday)
    - `time`: Dosing time (HH:mm format)
    - `timing_label`: Time label (After breakfast, Before bedtime, etc.)
    - `dose`: Dose at this time point
  - `instructions`: Dosing instructions
  - `notes`: Additional notes
  - `active`: Whether active (true = currently in use, false = discontinued)
  - `created_at`: Creation time (ISO 8601 format)
  - `last_updated`: Last updated time (ISO 8601 format)

### Schedule Array Generation Rules

**Important: The schedule must explicitly generate a dosing record for each day of the week**

#### Once-daily medications
Generate 7 records (1 per day, Monday through Sunday)
```json
"schedule": [
  {"weekday": 1, "time": "08:00", ...},
  {"weekday": 2, "time": "08:00", ...},
  {"weekday": 3, "time": "08:00", ...},
  {"weekday": 4, "time": "08:00", ...},
  {"weekday": 5, "time": "08:00", ...},
  {"weekday": 6, "time": "08:00", ...},
  {"weekday": 7, "time": "08:00", ...}
]
```

#### Twice-daily medications
Generate 14 records (2 per day × 7 days)
```json
"schedule": [
  {"weekday": 1, "time": "08:00", ...},  // Monday morning
  {"weekday": 1, "time": "20:00", ...},  // Monday evening
  {"weekday": 2, "time": "08:00", ...},  // Tuesday morning
  {"weekday": 2, "time": "20:00", ...},  // Tuesday evening
  ... (continued through Sunday)
]
```

#### Three-times-daily medications
Generate 21 records (3 per day × 7 days)
```json
"schedule": [
  {"weekday": 1, "time": "08:00", ...},  // Monday after breakfast
  {"weekday": 1, "time": "12:30", ...},  // Monday after lunch
  {"weekday": 1, "time": "18:30", ...},  // Monday after dinner
  {"weekday": 2, "time": "08:00", ...},  // Tuesday after breakfast
  ... (continued through Sunday)
]
```

#### Once-weekly medications
Generate 1 record (on the specified day of the week)
```json
"schedule": [
  {"weekday": 1, "time": "08:00", ...}  // Every Monday
]
```

#### Every-other-day medications
Generate 4 records (Mon, Wed, Fri, Sun — or Tue, Thu, Sat)
```json
"schedule": [
  {"weekday": 1, "time": "08:00", ...},
  {"weekday": 3, "time": "08:00", ...},
  {"weekday": 5, "time": "08:00", ...},
  {"weekday": 7, "time": "08:00", ...}
]
```

### Medication Log Data Structure

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

### Field Descriptions

- `date`: Medication date (YYYY-MM-DD format)
- `logs`: Medication log array
  - `id`: Record unique identifier (prefix log_ + timestamp)
  - `medication_id`: Associated medication ID
  - `medication_name`: Drug name
  - `scheduled_time`: Scheduled dosing time (HH:mm format)
  - `actual_time`: Actual dosing time (ISO 8601 format; null for missed doses)
  - `status`: Medication status (taken / missed / skipped / delayed)
  - `dose`: Actual dose taken
  - `notes`: Notes (e.g., reason for missing a dose)
  - `created_at`: Record creation time (ISO 8601 format)

### Medication Status Values

- **taken**: Taken (on time or with a delay)
- **missed**: Missed (not taken)
- **skipped**: Skipped (discontinued or temporarily suspended per physician instruction)
- **delayed**: Taken late (taken but after the scheduled time)

### Frequency Type Descriptions

- **daily**: Daily (times_per_day indicates the number of doses per day)
- **weekly**: Weekly (times_per_day indicates the number of doses per week)
- **every_other_day**: Every other day
- **as_needed**: As needed (adherence is not calculated)

### Medication Adherence Calculation

```
Adherence percentage = (Actual doses taken / Scheduled doses) × 100%

Where:
- Actual doses taken = Number of records with status "taken" or "delayed"
- Scheduled doses = Total doses that should have been taken (excluding "skipped" and "as_needed")
- Pending doses are not counted in the statistics
```

### Adherence Levels

- **Excellent**: ≥ 90%
- **Good**: 70% – 89%
- **Needs Improvement**: < 70%

## Global Index Update (Medication Records)

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

---

## Child Accident Prevention Data Structure

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male"
  },

  "safety_assessments": [
    {
      "date": "2025-01-14",
      "age": "2y5m",
      "age_months": 29,
      "area": "home",
      "area_name": "Home Safety",

      "checklist": {
        "window_protection": {
          "item": "Window protection",
          "safe": true,
          "notes": "Limiters installed"
        },
        "outlet_covers": {
          "item": "Outlet protection",
          "safe": true,
          "notes": "All outlets have protective covers"
        },
        "chemical_storage": {
          "item": "Chemical storage",
          "safe": false,
          "notes": "Medications stored at low level; need to move to a locked high location"
        }
      },

      "score": {
        "total_items": 5,
        "safe_items": 4,
        "percentage": 80,
        "level": "good"
      },

      "risks_identified": [
        {
          "item": "chemical_storage",
          "risk_level": "high",
          "description": "Medications not stored safely"
        }
      ]
    }
  ],

  "emergency_contacts": [
    { "name": "Dad", "phone": "138****1234", "relationship": "father" },
    { "name": "Mom", "phone": "139****5678", "relationship": "mother" }
  ]
}
```

### Field Descriptions
- `child_profile`: Child's basic information
- `safety_assessments`: Safety assessment records array
- `area`: Assessment area (home / car / water / food / outdoor)
- `checklist`: Safety checklist items
- `score`: Safety score
- `risks_identified`: Array of identified risks
- `emergency_contacts`: Emergency contacts

---

## Child Developmental Milestones Data Structure

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male",
    "premature": false
  },

  "developmental_tracking": {
    "assessments": [
      {
        "date": "2025-01-14",
        "age_months": 6,

        "gross_motor": {
          "items": [
            {
              "milestone": "Sitting independently",
              "age_expected": 6,
              "achieved": true,
              "age_achieved": 5,
              "date_achieved": "2020-06-01"
            }
          ],
          "status": "normal"
        },

        "fine_motor": {
          "items": [
            {
              "milestone": "Pincer grasp",
              "age_expected": 9,
              "achieved": false
            }
          ],
          "status": "normal"
        }
      }
    ]
  }
}
```

### Field Descriptions
- `gross_motor`: Gross motor development
- `fine_motor`: Fine motor development
- `language`: Language development
- `social`: Social development
- `cognitive`: Cognitive development
- `milestone`: Milestone name
- `age_expected`: Expected age of achievement (in months)
- `achieved`: Whether achieved
- `age_achieved`: Actual age of achievement (in months)

---

## Child Illness Management Data Structure

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male"
  },

  "illness_records": [
    {
      "id": "illness_20250112",
      "date": "2025-01-12",
      "onset_date": "2025-01-12",
      "days_illness": 3,

      "condition": {
        "name": "Acute upper respiratory tract infection",
        "category": "respiratory",
        "severity": "mild"
      },

      "symptoms": [
        {
          "name": "Fever",
          "severity": "moderate",
          "status": "improving"
        }
      ],

      "fever_tracking": [
        {
          "date": "2025-01-12T18:00:00",
          "temperature": 38.2,
          "medication": null
        }
      ],

      "medications": [
        {
          "name": "Ibuprofen Suspension",
          "dosage": "5ml",
          "frequency": "As needed"
        }
      ]
    }
  ]
}
```

### Field Descriptions
- `condition`: Illness information
- `category`: Illness category (respiratory / digestive, etc.)
- `severity`: Severity level (mild / moderate / severe)
- `fever_tracking`: Temperature tracking records
- `medications`: Medication records

---

## Child Sleep Management Data Structure

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male"
  },

  "sleep_records": [
    {
      "date": "2025-01-13",
      "age_months": 29,

      "night_sleep": {
        "bedtime": "21:00",
        "fall_asleep_time": "21:30",
        "wake_time": "07:00",
        "total_sleep_hours": 9.5,
        "sleep_quality": "good"
      },

      "night_wakeups": {
        "count": 1,
        "durations_minutes": [10],
        "reasons": ["Thirsty"]
      },

      "day_sleep": {
        "naps": 1,
        "total_nap_sleep": 2
      },

      "total_sleep": {
        "hours": 11.5,
        "within_recommended": true
      }
    }
  ],

  "sleep_problems": {
    "night_terrors": false,
    "bedwetting": false,
    "sleep_walking": false
  }
}
```

### Field Descriptions
- `night_sleep`: Nighttime sleep
- `night_wakeups`: Nighttime wake-up records
- `day_sleep`: Daytime naps
- `total_sleep`: Total sleep duration
- `sleep_problems`: Sleep problem flags

---

## Child Nutrition and Diet Data Structure

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male"
  },

  "dietary_records": [
    {
      "date": "2025-01-14",
      "age_months": 29,

      "meals": {
        "breakfast": {
          "time": "08:00",
          "foods": [
            {
              "name": "Milk",
              "amount": "200ml",
              "category": "dairy"
            }
          ]
        },
        "lunch": {
          "time": "12:00",
          "foods": [
            {
              "name": "Rice",
              "amount": "1 small bowl",
              "category": "grain"
            }
          ]
        }
      },

      "water_intake": {
        "amount_ml": 800,
        "recommended_min": 1000,
        "adequate": false
      },

      "nutrition_assessment": {
        "protein": "adequate",
        "calcium": "adequate",
        "iron": "adequate",
        "vitamin_d": "supplement_recommended"
      }
    }
  ],

  "picky_eating": {
    "level": "mild",
    "refused_foods": ["Carrots", "Green peppers"],
    "preferred_foods": ["Chicken", "Fruit"]
  }
}
```

### Field Descriptions
- `meals`: Meal records
- `category`: Food category (grain / protein / vegetable / fruit / dairy)
- `water_intake`: Water intake
- `nutrition_assessment`: Nutrition assessment
- `picky_eating`: Picky eating assessment

---

## Child Mental Health Data Structure

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male"
  },

  "assessments": [
    {
      "date": "2025-01-14",
      "age_months": 60,

      "mood_assessment": {
        "overall_mood": "stable",
        "mood_rating": 7,
        "emotional_regulation": "good"
      },

      "behavior_assessment": {
        "overall_behavior": "normal",
        "activity_level": "appropriate",
        "attention_span": "age_appropriate",
        "aggression": "none"
      },

      "anxiety_screening": {
        "overall_anxiety": "low_risk"
      },

      "attention_screening": {
        "inattention_score": 8,
        "hyperactivity_score": 5,
        "total_score": 13
      },

      "overall_assessment": "normal"
    }
  ],

  "mood_tracking": [
    {
      "date": "2025-01-14",
      "mood": "happy",
      "mood_rating": 7,
      "context": "playing"
    }
  ],

  "behavior_tracking": {
    "tantrums": {
      "frequency": "rare",
      "triggers": ["hungry", "tired"]
    },
    "sleep_issues": false,
    "aggression": false
  }
}
```

### Field Descriptions
- `mood_assessment`: Mood assessment
- `behavior_assessment`: Behavior assessment
- `anxiety_screening`: Anxiety screening
- `attention_screening`: Attention screening (ADHD-related)
- `mood_tracking`: Mood tracking records
- `behavior_tracking`: Behavior problem tracking

---
