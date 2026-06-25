---
description: Record exercise, manage fitness goals, generate exercise prescriptions and trend analysis
arguments:
  - name: action
    description: "Action type: record (record exercise) / history (history records) / stats (statistics) / goal (goal management) / analysis (analysis) / prescription (exercise prescription) / precautions (precautions)"
    required: true
  - name: info
    description: Detailed information (exercise type, duration, intensity, distance, etc., in natural language)
    required: false
---

# Exercise and Fitness Management Command

⚠️ **Important Medical Disclaimer**
Exercise recommendations and analysis provided by this system are for reference only and do not constitute medical advice or specific exercise prescriptions.
Please consult a doctor or exercise specialist before starting an exercise plan.
If you feel unwell, stop exercising immediately and seek medical attention.

---

## Usage

### Record Exercise

```bash
# Quick record (natural language)
/fitness record running 30minutes
/fitness record cycling 45minutes moderate_intensity
/fitness record swimming 1hour low_intensity
/fitness record yoga 60minutes

# Detailed record
/fitness record running 30 minutes distance 5km pace 6min_per_km
/fitness record cycling 45 minutes moderate heart_rate 145 calories 400
/fitness record swimming 60 minutes low distance 1000m
/fitness record strength 45 chest_training bench_press 50kg 3x12

# Record strength training
/fitness record strength 60 upper_body bench_press 50kg 3x12 shoulder_press 20kg 3x10

# Record ball sports
/fitness record basketball 90 minutes competitive
/fitness record badminton 45minutes moderate_intensity
```

**Supported Exercise Types**:

**Aerobic Exercise**:
- Running (running), brisk walking (walking)
- Cycling (cycling), swimming (swimming)
- Jump rope (jump_rope), aerobics (aerobics)
- Elliptical machine (elliptical), rowing machine (rowing)

**Strength Training**:
- Bodyweight training (calisthenics)
- Machine weights (machine_weights)
- Free weights (free_weights)
- Resistance bands (resistance_bands)

**Ball Sports**:
- Basketball (basketball), soccer (soccer)
- Badminton (badminton), table tennis (ping_pong)
- Tennis (tennis), volleyball (volleyball)

**Other Exercise**:
- Yoga (yoga), Pilates (pilates)
- Tai chi (tai_chi), dance (dance)
- Hiking (hiking), skiing (skiing)

**Intensity Notation**:
- Descriptive: low (low intensity), moderate (moderate intensity), high (high intensity)
- RPE scale: rpe 13 (RPE 6-20 scale, 13 = somewhat hard)
- Heart rate: heart_rate 145 or hr 145 (bpm)
- Custom: easy, comfortable, challenging, hard

---

### View Exercise History

```bash
# View recent records
/fitness history
/fitness history 10                    # Last 10 sessions

# View this week/this month
/fitness history week
/fitness history month

# View specific date
/fitness history 2025-06-20
/fitness history today
/fitness history yesterday

# View date range
/fitness history 2025-06-01 to 2025-06-30
/fitness history last 7 days
```

---

### Exercise Statistics Analysis

```bash
# Weekly statistics
/fitness stats week
/fitness summary week

# Monthly statistics
/fitness stats month
/fitness summary month

# Detailed statistics
/fitness stats                         # Comprehensive statistics
/fitness stats all                     # All statistics data

# Specific statistics
/fitness stats duration                # Exercise duration statistics
/fitness stats calories                # Calorie consumption statistics
/fitness stats distance                # Distance statistics
```

**Output Content**:
- Number of sessions, total duration, total distance
- Calories burned
- Exercise frequency (workout days per week)
- Intensity distribution
- Exercise type distribution
- Comparison with last week/last month

---

### Fitness Goal Management

```bash
# Set goals
/fitness goal lose_5kg 2025-06-30
/fitness goal weight_loss 5kg 2025-06-30
/fitness goal 5km_run 2025-08-15
/fitness goal workout_4days_per_week
/fitness goal workout_days 4

# Update goal progress
/fitness goal progress weight_loss 0.5kg
/fitness goal progress weight_loss 0.5kg

# View goals
/fitness goal list                     # All goals
/fitness goal active                   # Active goals
/fitness goal completed                # Completed goals

# View specific goal
/fitness goal weight_loss
/fitness goal weight_loss

# Mark goal complete
/fitness goal complete weight_loss
/fitness goal delete 5km_run           # Delete goal
```

**Goal Types**:
- **Weight loss goal** (weight_loss): Target weight loss amount, target weight, target body fat percentage
- **Muscle gain goal** (muscle_gain): Target weight gain amount, target muscle mass
- **Endurance goal** (endurance): 5K/10K/half marathon/full marathon, cycling distance, swimming distance
- **Health goal** (health): Lower resting heart rate, lower blood pressure, improve blood glucose
- **Habit formation** (habit): Workout days per week, daily steps, consecutive workout days

---

### Exercise Analysis

```bash
# Trend analysis
/fitness analysis trend
/fitness trend                          # Exercise trend analysis
/fitness trend 30days                   # Past 30 days trend
/fitness trend 3months                  # Past 3 months trend

# Intensity analysis
/fitness analysis intensity
/fitness analysis distribution          # Intensity distribution analysis

# Progress tracking
/fitness analysis progress
/fitness analysis progress running      # Running progress tracking
/fitness analysis progress strength     # Strength training progress tracking

# Exercise habit analysis
/fitness analysis habit                 # Exercise habit analysis
/fitness analysis pattern               # Exercise pattern recognition

# Correlation analysis
/fitness analysis correlation weight     # Exercise and weight correlation
/fitness analysis correlation blood_pressure    # Exercise and blood pressure correlation
/fitness analysis correlation blood_glucose     # Exercise and blood glucose correlation

# Insights and recommendations
/fitness insights                       # Exercise insights
/fitness recommendations                # Personalized recommendations
```

**Analysis Dimensions**:
- **Exercise volume trend**: Changes in duration, distance, calories
- **Exercise frequency**: Workout days per week, rest day distribution
- **Intensity distribution**: Low/medium/high intensity proportions
- **Exercise type preference**: Most-used exercise types
- **Progress tracking**: Pace improvement, strength increase, endurance improvement
- **Correlation analysis**: Relationship between exercise and weight, blood pressure, blood glucose

---

### Exercise Prescription

⚠️ **Reference Recommendation Level Statement**
The following exercise recommendations are based on authoritative guidelines from WHO, ACSM, AHA, etc., and are for reference only.
They do not constitute specific exercise prescriptions; please consult a doctor or exercise specialist for personalized guidance.

```bash
# Get exercise prescription
/fitness prescription                   # General exercise prescription
/fitness prescription beginner          # Beginner exercise prescription
/fitness prescription intermediate       # Intermediate exercise prescription

# Reference recommendations based on health conditions
/fitness prescription hypertension      # Exercise reference recommendations for hypertension patients
/fitness prescription diabetes          # Exercise reference recommendations for diabetes patients
/fitness prescription weight_loss       # Weight loss exercise recommendations

# View precautions
/fitness precautions                    # Exercise precautions
/fitness contra_indications             # Exercise contraindications
```

**FITT Principle**:
- **Frequency**: Workout days per week
- **Intensity**: Target heart rate zone, RPE, MET value
- **Time**: Duration per session (warm-up + main exercise + cool-down)
- **Type**: Aerobic, strength, flexibility, balance training

---

## Data Structure

### Exercise Record Data

```json
{
  "date": "2025-06-20",
  "time": "07:00",
  "type": "running",
  "duration_minutes": 30,
  "intensity": {
    "level": "moderate",
    "rpe": 13
  },
  "heart_rate": {
    "avg": 145,
    "max": 165,
    "min": 120
  },
  "distance_km": 5.0,
  "pace_min_per_km": "6:00",
  "calories_burned": 300,
  "how_felt": "good",
  "notes": "Felt very comfortable, steady pace"
}
```

### Fitness Goal Data

```json
{
  "goal_id": "goal_20250101",
  "category": "weight_loss",
  "title": "Lose 5 kg",
  "start_date": "2025-01-01",
  "target_date": "2025-06-30",
  "baseline_value": 75.0,
  "current_value": 70.5,
  "target_value": 70.0,
  "unit": "kg",
  "progress": 90,
  "status": "on_track"
}
```

---

## Medical Safety Principles

### ⚠️ Safety Boundaries

1. **Does not provide specific exercise prescriptions**
   - Exercise prescriptions must be formulated by a doctor or exercise specialist
   - System provides general recommendations only

2. **Does not handle exercise injuries**
   - Does not diagnose exercise injuries
   - Injuries require medical attention

3. **Does not evaluate cardiovascular risk**
   - Does not assess exercise risk
   - Medical evaluation required before exercise

4. **Does not replace professional guidance**
   - Complex exercises require professional coach guidance
   - System only provides recording and analysis

### ✅ What the System Can Do

- Exercise data recording and analysis
- Fitness goal management
- Exercise trend identification
- General exercise recommendations
- Reference recommendations based on health conditions

### Exercise Safety Reminders

- Warm up thoroughly before exercise
- Stretch appropriately after exercise
- Gradually increase exercise volume
- Pay attention to body signals
- Stay hydrated

### Special Populations

- Patients with chronic diseases need physician approval for exercise
- Pregnant women need obstetric physician recommendations for exercise
- Elderly should pay attention to balance and fall prevention
- Children's exercise should be age-appropriate

### Exercise Contraindications

- Do not exercise during fever or acute illness
- Do not exercise on an empty stomach or immediately after a large meal
- Do not exercise after alcohol consumption
- Outdoor exercise in extreme weather requires caution

---

## Reference Resources

### Exercise Guidelines
- [WHO Physical Activity and Sedentary Behaviour Guidelines](https://www.who.int/publications/i/item/9789240015128)
- [American Physical Activity Guidelines](https://health.gov/paguidelines/)

### Exercise Prescription
- [ACSM Exercise Testing and Prescription Guidelines](https://www.acsm.org/)
- [Exercise Prescription Professional Training](https://www.acsm.org/certifications)

### Exercise for Special Populations
- [Exercise Guidelines for Hypertension Patients](https://www.ahajournals.org/)
- [Exercise Guidelines for Diabetes Patients](https://www.diabetes.org/)

---

## Weight Loss Management Commands

**Weight Loss Safety Statement**
Weight loss recommendations provided by this system are based on scientific principles and do not constitute medical prescriptions.
For extreme weight loss or eating disorders, please consult a doctor.

### Body Composition Recording

```bash
/fitness:weightloss-record weight 75.5
/fitness:weightloss-record body-fat 28.5%
/fitness:weightloss-record waist 92
```

### Body Composition Analysis

```bash
/fitness:weightloss-body              # Complete body composition analysis
/fitness:weightloss-trend weight      # Weight trend
/fitness:weightloss-progress          # Weight loss progress
```

### Metabolic Rate Calculation

```bash
/fitness:weightloss-bmr               # Calculate BMR
/fitness:weightloss-tdee              # Calculate TDEE
/fitness:weightloss-activity moderate  # Set activity level
```

### Phase Management

```bash
/fitness:weightloss-phase weight-loss     # Set to weight loss phase
/fitness:weightloss-phase plateau         # Mark plateau phase
/fitness:weightloss-maintenance start     # Enter maintenance phase
```

---

**Version**: v1.0
**Last Updated**: 2026-01-02
**Maintainer**: WellAlly Tech
