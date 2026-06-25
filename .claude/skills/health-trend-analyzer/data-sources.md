# Health Trend Analyzer - Detailed Data Source Reference

This document provides detailed descriptions of all data sources used by the Health Trend Analyzer, including data structures, reading methods, availability checks, and missing data handling.

## Data Source Overview

| Data Source | File Path | Update Frequency | Data Type | Required |
|-------------|-----------|-----------------|-----------|----------|
| Personal profile | `data/profile.json` | Low | Basic info | Optional |
| Symptom records | `data/symptoms/**/*.json` | High | Time series | Recommended |
| Mood records | `data/mood/**/*.json` | High | Time series | Recommended |
| Diet records | `data/diet/**/*.json` | High | Time series | Optional |
| Medication logs | `data/medication-logs/**/*.json` | High | Time series | Recommended |
| Female cycle | `data/cycle-tracker.json` | Medium | Time series | Conditional |
| Pregnancy tracking | `data/pregnancy-tracker.json` | Medium | Time series | Conditional |
| Menopause | `data/menopause-tracker.json` | Medium | Time series | Conditional |
| Allergy history | `data/allergies.json` | Low | Static data | Optional |
| Radiation records | `data/radiation-records.json` | Low | Time series | Optional |
| Lab results | `data/medical_records/**/*.json` | Low | Time series | Recommended |

---

## 1. Personal Profile (profile.json)

### File Path
`data/profile.json`

### Data Structure
```json
{
  "created_at": "2025-01-01T00:00:00.000Z",
  "last_updated": "2025-12-31T12:34:56.789Z",
  "basic_info": {
    "name": "Zhang San",
    "gender": "male",
    "birth_date": "1990-01-01",
    "blood_type": "A+",
    "height": 175,
    "height_unit": "cm",
    "weight": 70.5,
    "weight_unit": "kg",
    "emergency_contacts": [
      {
        "name": "Li Si",
        "relationship": "spouse",
        "phone": "138****1234"
      }
    ]
  },
  "calculated": {
    "age": 35,
    "age_years": 35,
    "bmi": 23.0,
    "bmi_status": "normal",
    "body_surface_area": 1.85,
    "bsa_unit": "m²"
  },
  "history": [
    {
      "date": "2025-10-01",
      "weight": 70.8,
      "bmi": 23.1
    },
    {
      "date": "2025-11-01",
      "weight": 69.5,
      "bmi": 22.7
    },
    {
      "date": "2025-12-01",
      "weight": 68.5,
      "bmi": 22.4
    }
  ]
}
```

### Field Descriptions

**basic_info**: Basic information
- `name`: Name
- `gender`: Gender ("male" or "female")
- `birth_date`: Date of birth (YYYY-MM-DD format)
- `blood_type`: Blood type (A+, B+, AB+, O+, A-, B-, AB-, O-)
- `height`: Height
- `height_unit`: Height unit (cm)
- `weight`: Current weight
- `weight_unit`: Weight unit (kg)
- `emergency_contacts`: Emergency contact list

**calculated**: Calculated fields
- `age`: Age (years)
- `bmi`: BMI index
- `bmi_status`: BMI status ("underweight", "normal", "overweight", "obese")
- `body_surface_area`: Body surface area (m²)

**history**: Historical records (for tracking weight changes)
- `date`: Record date
- `weight`: Weight at that time
- `bmi`: BMI at that time

### Reading Method
```javascript
const profile = JSON.parse(readFile('data/profile.json'));

// Get current BMI
const currentBMI = profile.calculated.bmi;

// Get weight history (for trend analysis)
const weightHistory = profile.history.map(h => ({
  date: h.date,
  weight: h.weight,
  bmi: h.bmi
}));
```

### Availability Check
```javascript
function checkProfileAvailable() {
  try {
    const profile = JSON.parse(readFile('data/profile.json'));
    return {
      available: true,
      hasHistory: profile.history && profile.history.length > 0,
      historyLength: profile.history ? profile.history.length : 0
    };
  } catch (error) {
    return { available: false, error: error.message };
  }
}
```

### Missing Data Handling
- If file does not exist: Skip weight/BMI analysis, prompt "No personal profile recorded"
- If no history data: Use current weight and bmi as single data point, cannot analyze trends

---

## 2. Symptom Records (symptoms/)

### File Path
`data/symptoms/YYYY-MM/YYYY-MM-DD.json`

### Data Structure
```json
{
  "date": "2025-12-31",
  "logs": [
    {
      "id": "symptom_20251231083000001",
      "name": "headache",
      "severity": "moderate",
      "severity_level": 2,
      "onset_time": "08:30",
      "duration": 4,
      "duration_unit": "hours",
      "description": "Persistent dull pain, bilateral temporal area",
      "triggers": ["lack of sleep", "stress"],
      "location": "head",
      "associated_symptoms": ["nausea", "photophobia"],
      "relief_factors": "relieved after rest",
      "created_at": "2025-12-31T08:30:00.000Z"
    },
    {
      "id": "symptom_20251231140000002",
      "name": "fatigue",
      "severity": "mild",
      "severity_level": 1,
      "onset_time": "14:00",
      "duration": 3,
      "duration_unit": "hours",
      "description": "Feeling tired, difficulty concentrating",
      "triggers": ["after lunch", "heavy workload"],
      "location": "whole body",
      "associated_symptoms": [],
      "relief_factors": "short nap",
      "created_at": "2025-12-31T14:00:00.000Z"
    }
  ],
  "summary": {
    "total_symptoms": 2,
    "most_severe": "headache",
    "overall_discomfort": "moderate"
  }
}
```

### Field Descriptions

**Symptom record fields**:
- `id`: Unique identifier
- `name`: Symptom name (e.g., headache, fatigue, insomnia)
- `severity`: Severity level ("mild", "moderate", "severe")
- `severity_level`: Severity level number (1=mild, 2=moderate, 3=severe)
- `onset_time`: Onset time (HH:mm format)
- `duration`: Duration
- `duration_unit`: Duration unit (hours, days)
- `description`: Symptom description
- `triggers`: List of trigger factors
- `location`: Symptom location
- `associated_symptoms`: Associated symptoms
- `relief_factors`: Relief factors
- `created_at`: Record timestamp

**summary**: Daily summary
- `total_symptoms`: Total symptoms for the day
- `most_severe`: Most severe symptom
- `overall_discomfort`: Overall discomfort level

### Reading Method
```javascript
// Get all symptom files
const symptomFiles = glob('data/symptoms/**/*.json');

// Read all symptom data
const allSymptoms = symptomFiles.map(file => {
  const data = JSON.parse(readFile(file));
  return data.logs;
}).flat();

// Filter by time range
function filterSymptomsByDate(symptoms, startDate, endDate) {
  return symptoms.filter(symptom => {
    const symptomDate = new Date(symptom.created_at);
    return symptomDate >= startDate && symptomDate <= endDate;
  });
}

// Count symptom frequency
function getSymptomFrequency(symptoms) {
  const frequency = {};
  symptoms.forEach(symptom => {
    const name = symptom.name;
    frequency[name] = (frequency[name] || 0) + 1;
  });
  return frequency;
}
```

### Availability Check
```javascript
function checkSymptomsAvailable(startDate, endDate) {
  const symptomFiles = glob('data/symptoms/**/*.json');

  if (symptomFiles.length === 0) {
    return { available: false, message: "No symptom records available" };
  }

  // Check if there is data in the time range
  const allSymptoms = readAllSymptoms(symptomFiles);
  const filtered = filterSymptomsByDate(allSymptoms, startDate, endDate);

  return {
    available: true,
    totalFiles: symptomFiles.length,
    totalRecords: allSymptoms.length,
    recordsInRange: filtered.length,
    dataDensity: filtered.length / getDaysBetween(startDate, endDate) // Average records per day
  };
}
```

### Data Quality Assessment
- **Excellent**: Data density ≥ 0.5 (at least 1 record every 2 days on average)
- **Good**: Data density ≥ 0.3 (at least 1 record every 3 days on average)
- **Fair**: Data density ≥ 0.1 (at least 1 record every 10 days on average)
- **Insufficient**: Data density < 0.1 (insufficient data, trend analysis reliability is low)

### Missing Data Handling
- If directory does not exist: Skip symptom analysis, prompt "No symptom records available, recommend using /symptom command to record"
- If insufficient data (< 1 month): Prompt "Symptom records less than 1 month, recommend extending recording time"
- If data quality is poor: Note in report "Data quality: Fair, trend analysis for reference only"

---

## 3. Mood Records (mood/)

### File Path
`data/mood/YYYY-MM/YYYY-MM-DD.json`

### Data Structure
```json
{
  "date": "2025-12-31",
  "logs": [
    {
      "id": "mood_20251231080000001",
      "timestamp": "2025-12-31T08:00:00.000Z",
      "mood_score": 7,
      "mood_description": "good",
      "energy_level": "moderate",
      "energy_score": 6,
      "sleep_quality": "fair",
      "sleep_hours": 6.5,
      "stress_level": "low",
      "stress_score": 3,
      "notes": "Slept okay last night, feeling good today"
    }
  ],
  "summary": {
    "average_mood": 7.0,
    "average_sleep": 6.5,
    "average_stress": 3.0,
    "day_mood": "stable"
  }
}
```

### Field Descriptions

**Mood record fields**:
- `id`: Unique identifier
- `timestamp`: Record timestamp
- `mood_score`: Mood score (1-10, 10 = best)
- `mood_description`: Mood description (e.g., "excellent", "good", "fair", "poor", "bad")
- `energy_level`: Energy level ("high", "moderate", "low")
- `energy_score`: Energy score (1-10)
- `sleep_quality`: Sleep quality ("excellent", "good", "fair", "poor")
- `sleep_hours`: Sleep duration (hours)
- `stress_level`: Stress level ("low", "moderate", "high")
- `stress_score`: Stress score (1-10, 10 = most stressed)
- `notes`: Notes

**summary**: Daily summary
- `average_mood`: Average mood (average of multiple records in the day)
- `average_sleep`: Average sleep duration
- `average_stress`: Average stress score
- `day_mood`: Overall daily mood trend ("improving", "declining", "stable")

### Reading Method
```javascript
// Read all mood data
const moodFiles = glob('data/mood/**/*.json');
const allMoods = moodFiles.map(file => {
  const data = JSON.parse(readFile(file));
  return data.logs;
}).flat();

// Extract time series data
function getMoodTimeSeries(moods) {
  return moods.map(mood => ({
    date: mood.timestamp.split('T')[0],
    time: mood.timestamp.split('T')[1].substring(0, 5),
    moodScore: mood.mood_score,
    sleepHours: mood.sleep_hours,
    stressScore: mood.stress_score
  }));
}

// Calculate averages
function getMoodStats(moods) {
  const avgMood = moods.reduce((sum, m) => sum + m.mood_score, 0) / moods.length;
  const avgSleep = moods.reduce((sum, m) => sum + m.sleep_hours, 0) / moods.length;
  const avgStress = moods.reduce((sum, m) => sum + m.stress_score, 0) / moods.length;

  return { avgMood, avgSleep, avgStress };
}
```

### Availability Check
```javascript
function checkMoodAvailable(startDate, endDate) {
  const moodFiles = glob('data/mood/**/*.json');

  if (moodFiles.length === 0) {
    return { available: false, message: "No mood records available" };
  }

  const allMoods = readAllMoods(moodFiles);
  const filtered = filterByDate(allMoods, startDate, endDate);

  return {
    available: true,
    totalRecords: filtered.length,
    recordRate: filtered.length / getDaysBetween(startDate, endDate), // Record rate
    hasSleepData: filtered.every(m => m.sleep_hours > 0),
    hasStressData: filtered.every(m => m.stress_score > 0)
  };
}
```

### Missing Data Handling
- If no sleep data (sleep_hours = 0): Skip sleep-mood correlation analysis
- If no stress data (stress_score = 0): Skip stress-mood correlation analysis
- If record rate < 30%: Prompt "Few mood records, recommend recording daily"

---

## 4. Diet Records (diet/)

### File Path
`data/diet/YYYY-MM/YYYY-MM-DD.json`

### Data Structure
```json
{
  "date": "2025-12-31",
  "meals": [
    {
      "id": "diet_20251231080000001",
      "meal_type": "breakfast",
      "meal_time": "08:00",
      "foods": [
        {
          "name": "Milk oatmeal porridge",
          "amount": 1,
          "unit": "bowl",
          "calories": 250,
          "protein": 8,
          "carbs": 40,
          "fat": 5
        },
        {
          "name": "Boiled egg",
          "amount": 1,
          "unit": "piece",
          "calories": 70,
          "protein": 6,
          "carbs": 1,
          "fat": 5
        }
      ],
      "total_calories": 320,
      "notes": "Well-balanced nutrition"
    },
    {
      "id": "diet_20251231120000002",
      "meal_type": "lunch",
      "meal_time": "12:00",
      "foods": [
        {
          "name": "Rice",
          "amount": 150,
          "unit": "g",
          "calories": 180,
          "protein": 4,
          "carbs": 40,
          "fat": 0
        }
      ],
      "total_calories": 650,
      "notes": ""
    },
    {
      "id": "diet_20251231180000003",
      "meal_type": "dinner",
      "meal_time": "18:30",
      "foods": [
        {
          "name": "Chicken breast salad",
          "amount": 1,
          "unit": "serving",
          "calories": 350,
          "protein": 30,
          "carbs": 15,
          "fat": 20
        }
      ],
      "total_calories": 450,
      "notes": "Low fat, high protein"
    }
  ],
  "summary": {
    "total_calories": 1420,
    "total_protein": 48,
    "total_carbs": 96,
    "total_fat": 30,
    "meals_count": 3
  }
}
```

### Field Descriptions

**Meal record fields**:
- `id`: Unique identifier
- `meal_type`: Meal type ("breakfast", "lunch", "dinner", "snack")
- `meal_time`: Meal time (HH:mm format)
- `foods`: Food list

**Food fields**:
- `name`: Food name
- `amount`: Quantity
- `unit`: Unit (g, ml, piece, bowl, serving, etc.)
- `calories`: Calories
- `protein`: Protein (g)
- `carbs`: Carbohydrates (g)
- `fat`: Fat (g)

**summary**: Daily summary
- `total_calories`: Total calories
- `total_protein`: Total protein
- `total_carbs`: Total carbohydrates
- `total_fat`: Total fat
- `meals_count`: Number of meals

### Reading Method
```javascript
// Read all diet data
const dietFiles = glob('data/diet/**/*.json');
const allDiets = dietFiles.map(file => {
  const data = JSON.parse(readFile(file));
  return data.meals;
}).flat();

// Calculate daily nutritional intake
function getDailyNutrition(diets) {
  const daily = {};

  diets.forEach(meal => {
    const date = meal.meal_time.split('T')[0];
    if (!daily[date]) {
      daily[date] = { calories: 0, protein: 0, carbs: 0, fat: 0 };
    }

    meal.foods.forEach(food => {
      daily[date].calories += food.calories;
      daily[date].protein += food.protein;
      daily[date].carbs += food.carbs;
      daily[date].fat += food.fat;
    });
  });

  return daily;
}
```

### Availability Check
```javascript
function checkDietAvailable(startDate, endDate) {
  const dietFiles = glob('data/diet/**/*.json');

  if (dietFiles.length === 0) {
    return { available: false, message: "No diet records available" };
  }

  const allDiets = readAllDiets(dietFiles);
  const filtered = filterByDate(allDiets, startDate, endDate);

  return {
    available: true,
    totalRecords: filtered.length,
    hasCalorieData: filtered.every(d => d.total_calories > 0),
    hasMacroData: filtered.every(d => d.total_protein > 0)
  };
}
```

### Missing Data Handling
- Diet data is optional; missing data does not affect other dimension analysis
- If no calorie data (calories = 0): Skip diet-weight correlation analysis
- If record rate < 20%: Prompt "Few diet records, recommend recording every meal"

---

## 5. Medication Logs (medication-logs/)

### File Path
`data/medication-logs/YYYY-MM/YYYY-MM-DD.json`

### Data Structure
```json
{
  "date": "2025-12-31",
  "logs": [
    {
      "id": "log_20251231080000001",
      "medication_id": "med_20250915123456789",
      "medication_name": "Amlodipine",
      "scheduled_time": "08:00",
      "scheduled_dose": {
        "value": 5,
        "unit": "mg"
      },
      "actual_time": "2025-12-31T08:05:00",
      "status": "taken",
      "actual_dose": {
        "value": 5,
        "unit": "mg"
      },
      "notes": "",
      "created_at": "2025-12-31T08:05:00.000Z"
    },
    {
      "id": "log_20251231200000002",
      "medication_id": "med_20250915123456789",
      "medication_name": "Amlodipine",
      "scheduled_time": "20:00",
      "scheduled_dose": {
        "value": 5,
        "unit": "mg"
      },
      "actual_time": null,
      "status": "missed",
      "actual_dose": null,
      "notes": "Forgot to take",
      "created_at": "2025-12-31T22:00:00.000Z"
    }
  ],
  "summary": {
    "total_planned": 2,
    "total_taken": 1,
    "total_missed": 1,
    "adherence_rate": 50
  }
}
```

### Field Descriptions

**Medication log fields**:
- `id`: Unique identifier
- `medication_id`: Medication ID (linked to medications.json)
- `medication_name`: Medication name
- `scheduled_time`: Scheduled dose time (HH:mm)
- `scheduled_dose`: Scheduled dose
- `actual_time`: Actual dose time (ISO 8601 format)
- `status`: Dose status ("taken", "missed", "skipped", "delayed")
- `actual_dose`: Actual dose
- `notes`: Notes

**summary**: Daily summary
- `total_planned`: Number of planned doses
- `total_taken`: Number of doses actually taken
- `total_missed`: Number of missed doses
- `adherence_rate`: Daily adherence rate (%)

### Reading Method
```javascript
// Read all medication logs
const logFiles = glob('data/medication-logs/**/*.json');
const allLogs = logFiles.map(file => {
  const data = JSON.parse(readFile(file));
  return data.logs;
}).flat();

// Calculate adherence
function calculateAdherence(logs, medicationName) {
  const medLogs = logs.filter(log => log.medication_name === medicationName);
  const taken = medLogs.filter(log => log.status === 'taken').length;
  const total = medLogs.length;

  return {
    medication: medicationName,
    adherence: total > 0 ? Math.round((taken / total) * 100) : 0,
    taken: taken,
    total: total,
    missed: total - taken
  };
}

// Statistics by date
function getDailyAdherence(logs) {
  const daily = {};

  logs.forEach(log => {
    const date = log.actual_time ? log.actual_time.split('T')[0] : log.created_at.split('T')[0];
    if (!daily[date]) {
      daily[date] = { planned: 0, taken: 0, missed: 0 };
    }

    daily[date].planned++;
    if (log.status === 'taken') {
      daily[date].taken++;
    } else if (log.status === 'missed') {
      daily[date].missed++;
    }
  });

  // Calculate daily adherence rate
  Object.keys(daily).forEach(date => {
    const d = daily[date];
    d.adherence = Math.round((d.taken / d.planned) * 100);
  });

  return daily;
}
```

### Availability Check
```javascript
function checkMedicationLogsAvailable(startDate, endDate) {
  const logFiles = glob('data/medication-logs/**/*.json');

  if (logFiles.length === 0) {
    return { available: false, message: "No medication logs available" };
  }

  const allLogs = readAllLogs(logFiles);
  const filtered = filterByDate(allLogs, startDate, endDate);

  return {
    available: true,
    totalRecords: filtered.length,
    medications: [...new Set(filtered.map(log => log.medication_name))], // Unique medication list
    dateRange: getDateRange(filtered)
  };
}
```

### Missing Data Handling
- If no medication logs: Skip medication adherence analysis
- If logs are incomplete (< 1 month): Prompt "Few medication logs, recommend extending recording time"

---

## 6. Lab Results (medical_records/)

### File Path
`data/medical_records/biochemical_tests/YYYY-MM-DD.json` or
`data/medical_records/imaging_tests/YYYY-MM-DD.json`

### Data Structure (Biochemical Tests)
```json
{
  "report_id": "lab_20251231001",
  "report_type": "biochemical",
  "test_date": "2025-12-31",
  "hospital": "XX Hospital Laboratory",
  "indicators": [
    {
      "name": "Total Cholesterol",
      "name_en": "Total Cholesterol",
      "value": 210,
      "unit": "mg/dL",
      "reference_range": "200-240",
      "reference_min": 200,
      "reference_max": 240,
      "status": "normal",
      "trend": "decreased" // Relative to last test
    },
    {
      "name": "Fasting Glucose",
      "name_en": "Fasting Glucose",
      "value": 5.4,
      "unit": "mmol/L",
      "reference_range": "3.9-6.1",
      "reference_min": 3.9,
      "reference_max": 6.1,
      "status": "normal",
      "trend": "stable"
    },
    {
      "name": "Systolic BP",
      "name_en": "Systolic BP",
      "value": 132,
      "unit": "mmHg",
      "reference_range": "90-140",
      "reference_min": 90,
      "reference_max": 140,
      "status": "normal",
      "trend": "decreased"
    },
    {
      "name": "Diastolic BP",
      "name_en": "Diastolic BP",
      "value": 82,
      "unit": "mmHg",
      "reference_range": "60-90",
      "reference_min": 60,
      "reference_max": 90,
      "status": "normal",
      "trend": "decreased"
    }
  ],
  "summary": {
    "total_indicators": 4,
    "abnormal_count": 0,
    "improved_count": 2,
    "worsened_count": 0
  },
  "created_at": "2025-12-31T10:00:00.000Z"
}
```

### Field Descriptions

**Lab report fields**:
- `report_id`: Report ID
- `report_type`: Report type ("biochemical", "imaging")
- `test_date`: Test date
- `hospital`: Hospital name
- `indicators`: List of indicators

**Indicator fields**:
- `name`: Indicator name
- `name_en`: Indicator name (English)
- `value`: Test value
- `unit`: Unit
- `reference_range`: Reference range (string)
- `reference_min`: Lower reference limit
- `reference_max`: Upper reference limit
- `status`: Status ("normal", "abnormal_low", "abnormal_high")
- `trend`: Trend ("improved", "worsened", "stable", "new")

### Reading Method
```javascript
// Read all lab reports
const labFiles = glob('data/medical_records/biochemical_tests/**/*.json');
const labReports = labFiles.map(file => JSON.parse(readFile(file)));

// Extract time series for a specific indicator
function getIndicatorHistory(reports, indicatorName) {
  const history = [];

  reports.forEach(report => {
    const indicator = report.indicators.find(ind => ind.name === indicatorName);
    if (indicator) {
      history.push({
        date: report.test_date,
        value: indicator.value,
        unit: indicator.unit,
        status: indicator.status,
        trend: indicator.trend
      });
    }
  });

  // Sort by date
  return history.sort((a, b) => new Date(a.date) - new Date(b.date));
}

// Get all abnormal indicators
function getAbnormalIndicators(reports) {
  const abnormal = {};

  reports.forEach(report => {
    report.indicators.forEach(indicator => {
      if (indicator.status !== 'normal') {
        if (!abnormal[indicator.name]) {
          abnormal[indicator.name] = [];
        }
        abnormal[indicator.name].push({
          date: report.test_date,
          value: indicator.value,
          status: indicator.status
        });
      }
    });
  });

  return abnormal;
}
```

### Availability Check
```javascript
function checkLabResultsAvailable(startDate, endDate) {
  const labFiles = glob('data/medical_records/biochemical_tests/**/*.json');

  if (labFiles.length === 0) {
    return { available: false, message: "No lab records available" };
  }

  const reports = labFiles.map(file => JSON.parse(readFile(file)));
  const filtered = reports.filter(r => {
    const date = new Date(r.test_date);
    return date >= startDate && date <= endDate;
  });

  return {
    available: true,
    totalReports: filtered.length,
    hasMultipleReports: filtered.length >= 2, // At least 2 reports needed to analyze trends
    indicators: [...new Set(filtered.flatMap(r => r.indicators.map(i => i.name)))]
  };
}
```

### Missing Data Handling
- If no lab records: Skip lab result analysis
- If only 1 report: Display current values, prompt "At least 2 reports needed to analyze trends"
- If report interval < 1 month: Prompt "Lab report interval is short, recommend follow-up every 3-6 months"

---

## 7. Women's Health Data (Conditional Data Sources)

### 7.1 Cycle Tracking (cycle-tracker.json)

#### File Path
`data/cycle-tracker.json`

#### Data Structure (Summary)
```json
{
  "cycles": [
    {
      "cycle_id": "cycle_20251101",
      "period_start": "2025-11-01",
      "period_end": "2025-11-05",
      "cycle_length": 28,
      "daily_logs": [
        {
          "date": "2025-11-01",
          "symptoms": ["abdominal pain", "lower back pain"],
          "mood": "normal",
          "flow": { "intensity": "medium" }
        }
      ]
    }
  ]
}
```

#### Reading Method
```javascript
function checkCycleDataAvailable() {
  const profile = JSON.parse(readFile('data/profile.json'));

  // Only read cycle data if user is female
  if (profile.basic_info.gender !== 'female') {
    return { available: false, reason: "not_applicable" };
  }

  try {
    const cycleData = JSON.parse(readFile('data/cycle-tracker.json'));
    return {
      available: true,
      totalCycles: cycleData.cycles.length,
      hasSymptoms: cycleData.cycles.some(c => c.daily_logs.some(l => l.symptoms.length > 0))
    };
  } catch (error) {
    return { available: false, error: error.message };
  }
}
```

### 7.2 Pregnancy Tracking (pregnancy-tracker.json)

#### File Path
`data/pregnancy-tracker.json`

#### Data Structure (Summary)
```json
{
  "current_pregnancy": {
    "start_date": "2025-06-01",
    "current_week": 30,
    "weight_gain": 8.5,
    "checkups": [...]
  }
}
```

#### Reading Method
```javascript
function checkPregnancyDataAvailable() {
  try {
    const pregnancyData = JSON.parse(readFile('data/pregnancy-tracker.json'));
    const hasActivePregnancy = pregnancyData.current_pregnancy !== null;

    return {
      available: hasActivePregnancy,
      currentWeek: hasActivePregnancy ? pregnancyData.current_pregnancy.current_week : null
    };
  } catch (error) {
    return { available: false, error: error.message };
  }
}
```

### 7.3 Menopause Tracking (menopause-tracker.json)

#### File Path
`data/menopause-tracker.json`

#### Data Structure (Summary)
```json
{
  "menopause_tracking": {
    "start_date": "2025-01-01",
    "symptoms": ["hot flashes", "sweating"],
    "hrt_use": true
  }
}
```

#### Reading Method
```javascript
function checkMenopauseDataAvailable() {
  try {
    const menopauseData = JSON.parse(readFile('data/menopause-tracker.json'));
    const hasTracking = menopauseData.menopause_tracking !== null;

    return {
      available: hasTracking,
      symptoms: hasTracking ? menopauseData.menopause_tracking.symptoms : []
    };
  } catch (error) {
    return { available: false, error: error.message };
  }
}
```

---

## 8. Other Data Sources

### 8.1 Allergy History (allergies.json)

```json
{
  "allergies": [
    {
      "allergen": { "name": "Penicillin", "type": "drug" },
      "severity_level": 4,
      "current_status": { "status": "active" }
    }
  ]
}
```

**Purpose**: Flag allergy risks in trend analysis, remind user to watch for related symptoms

### 8.2 Radiation Records (radiation-records.json)

```json
{
  "records": [
    {
      "exam_date": "2025-12-31",
      "exam_type": "CT",
      "dose": 5.2,
      "dose_unit": "mSv"
    }
  ]
}
```

**Purpose**: Track cumulative radiation dose, assess risk

---

## Data Aggregation Strategy

### Complete Data Reading Process

```javascript
function analyzeHealthTrends(timePeriod = "3months") {
  // 1. Determine time range
  const endDate = new Date();
  const startDate = calculateStartDate(endDate, timePeriod);

  // 2. Check availability of each data source
  const dataAvailability = {
    profile: checkProfileAvailable(),
    symptoms: checkSymptomsAvailable(startDate, endDate),
    mood: checkMoodAvailable(startDate, endDate),
    diet: checkDietAvailable(startDate, endDate),
    medications: checkMedicationLogsAvailable(startDate, endDate),
    labResults: checkLabResultsAvailable(startDate, endDate),
    cycle: checkCycleDataAvailable(),
    pregnancy: checkPregnancyDataAvailable(),
    menopause: checkMenopauseDataAvailable()
  };

  // 3. Read available data
  const data = {};

  if (dataAvailability.profile.available) {
    data.profile = readProfile();
  }

  if (dataAvailability.symptoms.available) {
    data.symptoms = readSymptoms(startDate, endDate);
  }

  if (dataAvailability.mood.available) {
    data.mood = readMood(startDate, endDate);
  }

  // ... read other data sources

  // 4. Analyze trends
  const trends = analyzeTrends(data);

  // 5. Generate report
  return generateReport(trends, dataAvailability);
}
```

---

## Data Quality Standards

### Minimum Data Requirements

| Analysis Type | Minimum Data | Recommended Data |
|--------------|--------------|-----------------|
| Weight/BMI trend | 2 time points | 5+ time points |
| Symptom patterns | 1 month records | 3 months records |
| Medication adherence | 2 weeks records | 1 month records |
| Lab result trends | 2 reports | 3+ reports |
| Mood-sleep correlation | 2 weeks (daily) | 1 month records |
| Correlation analysis | 30 data points | 60+ data points |

### Data Completeness Assessment

```javascript
function assessDataCompleteness(data, startDate, endDate) {
  const daysInRange = getDaysBetween(startDate, endDate);
  const assessment = {};

  // Symptom data completeness
  if (data.symptoms) {
    const symptomDays = new Set(data.symptoms.map(s => s.date.split('T')[0])).size;
    assessment.symptoms = {
      completeness: symptomDays / daysInRange,
      rating: symptomDays / daysInRange >= 0.3 ? 'good' : symptomDays / daysInRange >= 0.1 ? 'fair' : 'poor'
    };
  }

  // Mood data completeness
  if (data.mood) {
    const moodDays = new Set(data.mood.map(m => m.timestamp.split('T')[0])).size;
    assessment.mood = {
      completeness: moodDays / daysInRange,
      rating: moodDays / daysInRange >= 0.5 ? 'good' : moodDays / daysInRange >= 0.3 ? 'fair' : 'poor'
    };
  }

  // ... assess other data sources

  return assessment;
}
```

---

## Data Filtering and Cleaning

### Time Range Filter
```javascript
function filterByDate(data, startDate, endDate) {
  return data.filter(item => {
    const itemDate = new Date(item.date || item.created_at || item.timestamp);
    return itemDate >= startDate && itemDate <= endDate;
  });
}
```

### Outlier Detection
```javascript
function detectOutliers(values) {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const stdDev = Math.sqrt(values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length);

  const outliers = values.filter(v => Math.abs(v - mean) > 2 * stdDev);
  return outliers;
}
```

### Missing Value Handling
```javascript
function handleMissingValues(timeSeries) {
  // Linear interpolation
  function interpolate(series, index) {
    const prev = series[index - 1];
    const next = series[index + 1];
    if (prev && next) {
      return (prev.value + next.value) / 2;
    }
    return null;
  }

  // Forward fill
  function forwardFill(series, index) {
    for (let i = index; i >= 0; i--) {
      if (series[i].value !== null) {
        return series[i].value;
      }
    }
    return null;
  }

  return series.map((point, index) => {
    if (point.value === null) {
      point.value = interpolate(series, index) || forwardFill(series, index);
    }
    return point;
  });
}
```

---

## Data Export Format

### JSON Export (for HTML reports)

```json
{
  "analysis_date": "2025-12-31",
  "period": {
    "start": "2025-10-01",
    "end": "2025-12-31",
    "days": 92
  },
  "data_sources": {
    "profile": "available",
    "symptoms": "available",
    "mood": "available",
    "diet": "not_available"
  },
  "trends": {
    "weight": { "direction": "decreasing", "change": -2.3, "unit": "kg" },
    "symptoms": { "most_frequent": "headache", "frequency": 12, "trend": "decreasing" },
    "medications": { "adherence": 78, "missed_doses": 8 },
    "mood": { "average_score": 6.8, "trend": "stable" }
  },
  "correlations": [
    { "x": "Sleep duration", "y": "Mood score", "coefficient": 0.78, "significance": "high" }
  ],
  "recommendations": [
    "Increase sleep duration to 7-8 hours",
    "Set evening medication reminders",
    "Recheck blood lipids in 3 months"
  ]
}
```
