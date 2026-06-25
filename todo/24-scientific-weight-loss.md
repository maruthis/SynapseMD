# Scientific Exercise and Healthy Weight Loss Feature Extension Proposal

**Module Number**: 24
**Category**: Specialized Health Feature - Scientific Exercise and Healthy Weight Loss
**Status**: 📝 Pending Development
**Priority**: High
**Created Date**: 2025-12-31

---

## Feature Overview

The scientific exercise and healthy weight loss module provides science-based healthy weight management, emphasizing healthy weight reduction rather than simply losing weight. It integrates multi-dimensional management across diet, exercise, and lifestyle.

### Core Principles

- **Scientific** - Based on nutritional science and exercise science principles
- **Health-Focused** - Focuses on improving body composition, not just the number on the scale
- **Sustainable** - Building long-term healthy habits
- **Personalized** - Plans tailored to individual constitution
- **Safe** - Avoids extreme weight loss methods

### Core Features

1. **Body Composition Analysis** - Muscle, fat, water, and bone content
2. **Basal Metabolic Rate Calculation** - BMR and TDEE calculations
3. **Energy Deficit Management** - Scientifically established caloric deficit
4. **Weight Loss Phase Management** - Weight loss phase, plateau phase, maintenance phase
5. **Diet and Exercise Balance** - Nutritional ratios, exercise prescription
6. **Preventing Rebound** - Long-term maintenance strategies
7. **Health Indicator Monitoring** - Blood pressure, blood glucose, blood lipids, etc.

---

## Sub-module 1: Body Composition Analysis

### Feature Description

Comprehensively analyze body composition, focusing on fat loss and muscle gain rather than simple weight reduction.

### Core Metrics

#### 1. Weight-Related
- **Body Weight**
- **BMI** (Body Mass Index) = Weight (kg) / Height² (m)
- **Ideal Weight** = Height² (m) × 22 (Asian standard)

#### 2. Body Fat-Related
- **Body Fat Percentage**
  - Male: Normal 10-20%, Overweight 20-25%, Obese >25%
  - Female: Normal 18-28%, Overweight 28-33%, Obese >33%
- **Fat Mass** = Body Weight × Body Fat Percentage
- **Lean Body Mass** = Body Weight - Fat Mass

#### 3. Muscle-Related
- **Skeletal Muscle Mass**
- **Muscle Mass**
- **Muscle Distribution** (limbs, trunk)

#### 4. Other Components
- **Total Body Water**
- **Protein**
- **Minerals**
- **Bone Mineral Content**

#### 5. Circumference Measurements
- **Waist Circumference**
  - Male: <85cm normal, 85-95cm overweight, >95cm abdominal obesity
  - Female: <80cm normal, 80-90cm overweight, >90cm abdominal obesity
- **Hip Circumference**
- **Waist-to-Hip Ratio**
  - Male: <0.9 normal, >0.95 abdominal obesity
  - Female: <0.85 normal, >0.9 abdominal obesity
- **Thigh Circumference**
- **Upper Arm Circumference**

### Data Structure

```json
{
  "body_composition": {
    "date": "2025-06-20",
    "height_cm": 170,
    "weight_kg": 75.5,

    "bmi": {
      "value": 26.1,
      "category": "overweight",
      "ideal_weight": 63.6,
      "weight_to_lose": 11.9
    },

    "body_fat": {
      "percentage": 28.5,
      "mass_kg": 21.5,
      "category": "overweight",
      "target_percentage": 20,
      "fat_to_lose_kg": 6.4
    },

    "muscle": {
      "skeletal_muscle_kg": 32.5,
      "percentage": 43.0,
      "target_kg": 34.0
    },

    "other_components": {
      "water_kg": 42.5,
      "water_percentage": 56.3,
      "protein_kg": 9.5,
      "minerals_kg": 2.5
    },

    "circumferences": {
      "waist_cm": 92,
      "hip_cm": 98,
      "waist_hip_ratio": 0.94,
      "abdominal_obesity": true,
      "thigh_cm": 58,
      "arm_cm": 32
    },

    "visceral_fat": {
      "level": 12,
      "category": "high",
      "target_level": 10
    },

    "basal_metabolic_rate": {
      "bmr_calories": 1650,
      "tdee_calories": 2300,
      "method": "mifflin_st_jeor"
    },

    "weight_history": [
      {
        "date": "2025-01-01",
        "weight": 82.0
      },
      {
        "date": "2025-03-01",
        "weight": 78.5
      },
      {
        "date": "2025-06-20",
        "weight": 75.5
      }
    ],

    "goals": {
      "target_weight": 68.0,
      "target_body_fat_percentage": 20,
      "target_waist_cm": 85,
      "timeline_months": 6
    }
  }
}
```

### Command Interface

```bash
# Record body composition
/weightloss record weight 75.5            # Record weight
/weightloss record body-fat 28.5%         # Record body fat percentage
/weightloss record muscle 32.5kg          # Record muscle mass
/weightloss record waist 92cm             # Record waist circumference

# Comprehensive analysis
/weightloss body-composition              # Body composition analysis
/weightloss bmr                           # Calculate basal metabolic rate
/weightloss tdee                          # Calculate total daily energy expenditure

# View trends
/weightloss trend weight                 # Weight trend
/weightloss trend body-fat               # Body fat trend
/weightloss progress                      # Weight loss progress
```

---

## Sub-module 2: Basal Metabolic Rate Calculation

### Feature Description

Accurately calculate the basal metabolic rate (BMR) and total daily energy expenditure (TDEE) to provide a scientific basis for energy deficit management.

### Calculation Formulas

#### 1. Harris-Benedict Formula (Original 1919)

**Male**:
BMR = 88.362 + (13.397 × weight kg) + (4.799 × height cm) - (5.677 × age)

**Female**:
BMR = 447.593 + (9.247 × weight kg) + (3.098 × height cm) - (4.330 × age)

#### 2. Mifflin-St Jeor Formula (Recommended, more accurate)

**Male**:
BMR = (10 × weight kg) + (6.25 × height cm) - (5 × age) + 5

**Female**:
BMR = (10 × weight kg) + (6.25 × height cm) - (5 × age) - 161

#### 3. Katch-McArdle Formula (Based on lean body mass)

BMR = 370 + (21.6 × lean body mass kg)

#### 4. Activity Factors

- **Sedentary** (little or no exercise): 1.2
- **Lightly active** (light exercise 1-3 days/week): 1.375
- **Moderately active** (moderate exercise 3-5 days/week): 1.55
- **Very active** (hard exercise 6-7 days/week): 1.725
- **Extra active** (physical labor or twice-daily training): 1.9

#### 5. TDEE Calculation

TDEE = BMR × Activity Factor

### Data Structure

```json
{
  "metabolic_rate": {
    "assessment_date": "2025-06-20",
    "personal_info": {
      "gender": "male",
      "age": 35,
      "height_cm": 170,
      "weight_kg": 75.5,
      "body_fat_percentage": 28.5
    },

    "bmr_calculations": {
      "harris_benedict": {
        "bmr": 1728,
        "formula": "original_1919"
      },
      "mifflin_st_jeor": {
        "bmr": 1650,
        "formula": "recommended",
        "used": true
      },
      "katch_mcardle": {
        "lean_body_mass_kg": 54.0,
        "bmr": 1536,
        "formula": "based_on_lean_mass"
      }
    },

    "activity_level": {
      "current": "moderate",
      "factor": 1.55,
      "description": "Moderate exercise 3-5 days per week"
    },

    "tdee": {
      "calories": 2558,
      "calculation": "BMR_1650 × 1.55"
    },

    "target_calories": {
      "weight_loss_maintenance": 2558,
      "mild_deficit_250": 2308,
      "moderate_deficit_500": 2058,
      "aggressive_deficit_750": 1808,
      "recommended": 2058
    },

    "macronutrient_distribution": {
      "protein": {
        "grams": 154,
        "calories": 616,
        "percentage": 30
      },
      "carbs": {
        "grams": 206,
        "calories": 824,
        "percentage": 40
      },
      "fat": {
        "grams": 68,
        "calories": 618,
        "percentage": 30
      }
    },

    "adjustments": {
      "strength_training_days": 3,
      "cardio_days": 2,
      "rest_days": 2,
      "activity_burn_calories": 500
    }
  }
}
```

### Command Interface

```bash
# Calculate metabolic rate
/weightloss bmr                           # Calculate BMR
/weightloss tdee                          # Calculate TDEE
/weightloss activity-level moderate       # Set activity level

# Energy targets
/weightloss calorie-target                # View calorie target
/weightloss deficit 500                   # Set energy deficit
/weightloss macros                        # View macronutrient distribution
```

---

## Sub-module 3: Energy Deficit Management

### Feature Description

Scientifically manage the energy deficit to achieve healthy weight loss.

### Energy Deficit Principles

**Weight Loss Principle**:
Losing 1 kg of fat requires burning approximately 7,700 calories

**Safe Weight Loss Speed**:
- **Mild weight loss**: 0.25-0.5 kg per week (daily energy deficit of 250-500 calories)
- **Moderate weight loss**: 0.5-1 kg per week (daily energy deficit of 500-1,000 calories)
- **Rapid weight loss**: 1-1.5 kg per week (daily energy deficit of 1,000-1,500 calories; requires medical supervision)

**Recommendation**: 0.5-1 kg per week, daily energy deficit of 500-1,000 calories

### Energy Balance

**Energy Intake** < **Energy Expenditure** = **Weight Loss**

**Energy Intake** = Dietary intake + Exercise expenditure + Basal metabolism

**Energy Expenditure** = BMR + Activity expenditure + Thermic effect of food + NEAT (Non-Exercise Activity Thermogenesis)

### Diet Management

#### 1. Calorie Control
- **Not recommended**: <1,200 calories/day (women), <1,500 calories/day (men)
- **Recommended**: TDEE - 500 calories
- **Minimum safe calories**: BMR × 1.2

#### 2. Macronutrient Ratios

**Recommended ratios during fat loss phase**:
- **Protein**: 25-35% (to prevent muscle loss)
- **Carbohydrates**: 35-45% (to control blood sugar)
- **Fat**: 25-30% (essential fatty acids)

#### 3. Dietary Principles

- High protein: prevents muscle loss
- Moderate carbohydrates: choose low-GI foods
- Healthy fats: nuts, fish, olive oil
- High fiber: increases satiety
- Adequate hydration: 2-3L per day

### Exercise Management

#### 1. Exercise Types

**Aerobic Exercise** (fat burning):
- Recommended: 3-5 days per week, 30-60 minutes per session
- Moderate intensity: 50-70% of heart rate reserve
- Types: brisk walking, jogging, cycling, swimming

**Strength Training** (preserve muscle):
- Recommended: 2-3 days per week, full-body training
- Focus: large muscle groups (legs, back, chest)
- Weight: failure at 8-12 reps

**HIIT** (efficient fat burning):
- Recommended: 1-2 times per week
- Pattern: 30 seconds high intensity + 90 seconds low intensity, repeat 8-12 rounds

#### 2. Increasing NEAT

NEAT (Non-Exercise Activity Thermogenesis) accounts for 15-30% of daily expenditure

**Ways to increase NEAT**:
- Walk more: target 10,000 steps per day
- Standing desk: stand for 5 minutes every hour
- Take stairs: instead of elevator
- Household activities: actively participate

### Data Structure

```json
{
  "energy_balance": {
    "date": "2025-06-20",
    "energy_deficit_target": 500,

    "energy_intake": {
      "target_calories": 2058,
      "actual_calories": 1980,
      "protein": 154,
      "carbs": 206,
      "fat": 68
    },

    "energy_expenditure": {
      "bmr": 1650,
      "exercise": 400,
      "neat": 300,
      "tef": 150,
      "total": 2500
    },

    "deficit_achieved": 520,
    "deficit_target_met": true,

    "weekly_deficit": 3640,
    "estimated_weight_loss_kg": 0.47,

    "food_diary": [
      {
        "meal": "breakfast",
        "foods": ["Eggs", "Whole wheat bread", "Milk"],
        "calories": 450
      }
    ],

    "exercise_log": {
      "type": "running",
      "duration_minutes": 45,
      "calories_burned": 400
    },

    "neat_activities": {
      "steps": 10500,
      "stairs_floors": 5,
      "standing_minutes": 60
    },

    "weight_change": {
      "date": "2025-06-20",
      "weight": 75.5,
      "change_from_last_week": -0.6,
      "cumulative_loss": 6.5
    }
  }
}
```

### Command Interface

```bash
# Energy logging
/weightloss intake breakfast 450           # Log dietary intake for breakfast
/weightloss intake daily 1980              # Log total daily intake
/weightloss exercise running 45 400        # Log exercise expenditure
/weightloss neat steps 10500               # Log step count

# View energy balance
/weightloss balance                        # View energy balance
/weightloss deficit                        # View energy deficit
/weightloss estimate-loss                  # Estimate weight loss
```

---

## Sub-module 4: Weight Loss Phase Management

### Feature Description

Manage the weight loss process in phases, adapting to the needs and challenges of different phases.

### Three Phases of Weight Loss

#### 1. Weight Loss Phase

**Target**: Lose 0.5-1 kg per week

**Strategy**:
- Energy deficit: 500-1,000 calories/day
- Diet control: high protein, moderate carbs, low fat
- Exercise: combination of aerobic and strength training
- Monitoring: weigh weekly

**Common Challenges**:
- Hunger: high protein, high fiber, adequate hydration
- Plateau: adjust diet, increase exercise
- Muscle loss: strength training, adequate protein

#### 2. Plateau Phase

**Characteristics**:
- Weight unchanged for 2-3 weeks
- Despite continuing diet and exercise control

**Causes**:
- Metabolic adaptation: BMR decreases
- Water retention: glycogen storage recovery
- Muscle gain: muscle is denser than fat
- Diet relaxation: unknowingly eating more

**Coping Strategies**:
- **Short-term (1-2 weeks)**:
  - Keep persisting, don't give up
  - Review food diary
  - Increase NEAT

- **Medium-term (3-4 weeks)**:
  - Adjust calories: reduce by another 100-200 calories
  - Increase exercise: add 10-15 minutes of aerobic activity
  - Change exercise type: new exercise stimulus

- **Long-term (>4 weeks)**:
  - Re-evaluate goals
  - Diet break (maintain calories for 1-2 weeks)
  - Consult a nutritionist

**Breakthrough Methods**:
- Carbohydrate cycling: alternating high and low carb days
- Intermittent fasting: 16:8 or 5:2
- HIIT training: increase metabolic stimulus
- Protein cycling: alternating high-protein and normal days

#### 3. Maintenance Phase

**Target**: Maintain weight, prevent rebound

**Challenges**:
- Metabolic adaptation: BMR lower than expected
- Hunger hormone: Ghrelin elevated
- Satiety hormone: Leptin decreased
- Habit relapse: return to old habits

**Strategy**:
- **Calories**: Gradually increase to TDEE (+100 calories per week)
- **Exercise**: Maintain exercise habits
- **Monitoring**: Weigh weekly; ±2 kg is normal
- **Diet**: 80/20 principle (80% healthy, 20% flexible)

**Keys to Long-Term Maintenance**:
- Regular exercise: at least 150 minutes of moderate-intensity exercise per week
- High-protein diet: 1.2-1.6 g per kg of body weight
- Regular weighing: 1-2 times per week
- Self-monitoring: continuously record diet and exercise
- Social support: family and friend support

### Data Structure

```json
{
  "weight_loss_phases": {
    "current_phase": "weight_loss",
    "start_date": "2025-01-01",
    "target_date": "2025-07-01",

    "phases": {
      "weight_loss": {
        "duration_months": 6,
        "target_weight_loss_kg": 10,
        "actual_weight_loss_kg": 6.5,
        "progress": 0.65,
        "status": "on_track"
      },

      "plateau": {
        "occurrences": 2,
        "first_plateau_start": "2025-03-01",
        "first_plateau_duration_weeks": 2,
        "breakthrough_method": "increased_cardio",
        "current_plateau": false
      },

      "maintenance": {
        "start_date": "2025-07-01",
        "target_duration_months": "ongoing",
        "maintenance_weight": 68.0,
        "allowable_range_kg": 2.0,
        "strategy": "80/20_principle"
      }
    },

    "milestones": [
      {
        "date": "2025-02-01",
        "achievement": "lost_5kg",
        "celebration": "new_workout_clothes"
      },
      {
        "date": "2025-04-01",
        "achievement": "body_fat_below_25%",
        "celebration": "spa_day"
      }
    ],

    "challenges": [
      {
        "challenge": "plateau",
        "frequency": "every_6-8_weeks",
        "coping_strategies": ["adjust_calories", "change_exercise"]
      },
      {
        "challenge": "social_events",
        "frequency": "weekly",
        "coping_strategies": ["plan_ahead", "portion_control"]
      }
    ]
  }
}
```

### Command Interface

```bash
# Phase management
/weightloss phase weight-loss              # Set to weight loss phase
/weightloss phase plateau                 # Record entering the plateau phase
/weightloss phase breakdown method        # Record breakthrough method
/weightloss phase maintenance             # Enter maintenance phase

# Milestones
/weightloss milestone 5kg new-clothes     # Record a milestone
/weightloss milestones list               # View all milestones
```

---

## Sub-module 5: Scientific Diet Management

### Feature Description

Diet management based on nutritional science, focusing not only on calories but also on nutritional quality.

### Dietary Principles

#### 1. High-Protein Diet

**Recommended Intake**:
- Weight loss phase: 1.6-2.2 g/kg body weight
- Maintenance phase: 1.2-1.6 g/kg body weight

**Protein Sources**:
- High-quality protein: eggs, chicken, fish, beef, tofu
- Distribution: 20-30 g protein per meal
- Timing: supplement within 30 minutes after exercise

#### 2. Low-GI Carbohydrates

**GI Values** (Glycemic Index):
- **Low GI (<55)**: Oats, brown rice, quinoa, legumes
- **Medium GI (55-70)**: Whole wheat bread, bananas, rolled oats
- **High GI (>70)**: White rice, white bread, potatoes, candy

**Recommendations**:
- Choose low-GI carbs: stable blood sugar, lasting satiety
- Moderate carbs: 35-45% of total calories
- Timing: eat carbs before and after training

#### 3. Healthy Fats

**Recommended Fat Sources**:
- **Monounsaturated fats**: Olive oil, nuts, avocado
- **Polyunsaturated fats**: Fish (Omega-3), flaxseeds
- **Avoid**: Trans fats, excessive saturated fat

**Fat Intake**:
- 25-30% of total calories
- 0.8-1.0 g per kg body weight
- Omega-3: fatty fish twice per week

#### 4. High-Fiber Diet

**Recommended Intake**: 25-35 g/day

**High-Fiber Foods**:
- Vegetables: broccoli, spinach, carrots
- Fruits: apples, berries, pears (with skin)
- Whole grains: oats, brown rice, whole wheat bread
- Legumes: black beans, chickpeas, lentils
- Nuts: almonds, walnuts, chia seeds

**Benefits**:
- Increases satiety
- Stabilizes blood sugar
- Improves gut health
- Lowers cholesterol

### Intermittent Fasting

#### 1. 16:8 Method

**Pattern**: Fast for 16 hours per day, eat within an 8-hour window

**Example**:
- Fasting window: 20:00 - 12:00 (next day)
- Eating window: 12:00 - 20:00

**Benefits**:
- Automatically limits calorie intake
- Improves insulin sensitivity
- Promotes fat burning
- Simple and easy to execute

#### 2. 5:2 Method

**Pattern**: Eat normally 5 days per week, restrict calories (500 calories) 2 days per week

**Benefits**:
- High flexibility
- Easy to sustain
- Metabolic benefits

### Diet Logging

#### Food Diary

**What to Record**:
- Food name and portion size
- Time of intake
- Calories and macronutrients
- Hunger/fullness level
- Emotional state

#### Dietary Analysis

**Analysis Dimensions**:
- Calorie intake vs. target
- Macronutrient ratios
- Micronutrient adequacy
- Dietary pattern identification (binge eating, late-night snacking, etc.)

### Data Structure

```json
{
  "diet_management": {
    "approach": "balanced_deficit",
    "target_calories": 2058,
    "macro_targets": {
      "protein_percentage": 30,
      "carbs_percentage": 40,
      "fat_percentage": 30
    },

    "meal_plan": {
      "meals_per_day": 4,
      "timing": ["08:00", "12:00", "16:00", "20:00"],
      "structure": {
        "breakfast": {
          "calories": 450,
          "protein": 30,
          "carbs": 50,
          "fat": 15,
          "example": "2 eggs + 50g oats + 250ml milk"
        },
        "lunch": {
          "calories": 600,
          "protein": 40,
          "carbs": 60,
          "fat": 20,
          "example": "150g chicken breast + 150g brown rice + 200g vegetables"
        },
        "snack": {
          "calories": 200,
          "protein": 15,
          "carbs": 15,
          "fat": 10,
          "example": "100g Greek yogurt + 20g nuts"
        },
        "dinner": {
          "calories": 550,
          "protein": 45,
          "carbs": 45,
          "fat": 18,
          "example": "150g fish + 150g sweet potato + 200g vegetables"
        }
      }
    },

    "food_diary": [
      {
        "date": "2025-06-20",
        "meal": "breakfast",
        "time": "08:00",
        "foods": [
          {
            "name": "Eggs",
            "amount": "2",
            "calories": 140,
            "protein": 12
          },
          {
            "name": "Whole wheat bread",
            "amount": "2 slices",
            "calories": 160,
            "carbs": 30
          },
          {
            "name": "Milk",
            "amount": "250ml",
            "calories": 150,
            "protein": 8
          }
        ],
        "total_calories": 450,
        "satiety": 7,
        "hunger_before": 6
      }
    ],

    "weekly_analysis": {
      "week_start": "2025-06-14",
      "average_calories": 2030,
      "protein_grams_avg": 152,
      "carbs_grams_avg": 195,
      "fat_grams_avg": 67,
      "adherence": 0.85,
      "days_on_target": 6,
      "days_off_target": 1
    },

    "intermittent_fasting": {
      "method": "16_8",
      "eating_window_start": "12:00",
      "eating_window_end": "20:00",
      "fasting_window_start": "20:00",
      "fasting_window_end": "12:00",
      "adherence": 0.90
    },

    "hydration": {
      "target_liters": 2.5,
      "actual_liters": 2.2,
      "water_intake": 8,
      "other_fluids": 2
    }
  }
}
```

### Command Interface

```bash
# Diet logging
/weightloss meal breakfast eggs milk      # Log breakfast
/weightloss meal dinner 600               # Log dinner calories
/weightloss snack apple                   # Log snack

# Dietary analysis
/weightloss diet analysis                # Dietary analysis
/weightloss protein                      # Protein intake analysis
/weightloss adherence                     # Dietary adherence

# Intermittent fasting
/weightloss if 16-8                       # Set 16:8 fasting
/weightloss if eating-window 12:00-20:00 # Set eating window
```

---

## Sub-module 6: Scientific Exercise Prescription

### Feature Description

Personalized exercise prescription based on weight loss goals, optimized for fat loss results.

### Exercise Prescription Elements (FITT)

#### 1. Frequency

**Recommended Frequency**:
- **Aerobic exercise**: 3-5 days per week
- **Strength training**: 2-3 days per week
- **HIIT**: 1-2 days per week
- **Rest days**: 1-2 days per week

#### 2. Intensity

**Aerobic Exercise Intensity**:
- **Low intensity**: 50-60% of heart rate reserve (Zone 2)
- **Moderate intensity**: 60-70% of heart rate reserve (Zone 3)
- **High intensity**: 70-80% of heart rate reserve (Zone 4)

**Maximum Heart Rate Estimation**:
- Simple formula: 220 - age
- More accurate (Tanaka): 208 - (0.7 × age)
- Heart rate reserve: (Max HR - Resting HR) × intensity% + Resting HR

**Strength Training Intensity**:
- Weight: failure at 8-12 reps (muscle hypertrophy range)
- Sets: 3-4 sets
- Rest: 60-90 seconds

#### 3. Time

**Aerobic Exercise Duration**:
- Recommended: 30-60 minutes per session
- Minimum effective time: 20 minutes
- Risk of excessive duration: >90 minutes may increase muscle loss

**Strength Training Duration**:
- Recommended: 45-60 minutes per session
- Including 5-10 minute warm-up

#### 4. Type

**Aerobic Exercise Options**:
- **Low impact**: Brisk walking, elliptical, swimming, cycling
- **High impact**: Running, jump rope, aerobics
- **Recommendation**: Choose low-impact exercises during the early weight loss phase to protect joints

**Strength Training Options**:
- **Compound movements**: Squats, deadlifts, bench press, pull-ups
- **Full-body training**: Train large muscle groups each session
- **Progressive overload**: Gradually increase weight or reps

### Sample Exercise Schedule

#### 5 Days Aerobic + 3 Days Strength Per Week

```
Monday: 45 min aerobic + strength training (upper body)
Tuesday: 30 min aerobic
Wednesday: Strength training (lower body)
Thursday: 30 min aerobic
Friday: 45 min aerobic + strength training (full body)
Saturday: 20 min HIIT
Sunday: Rest or light activity (yoga, walking)
```

### Exercise Nutrition Timing

#### 1. Pre-workout (1-2 hours before)

**Recommendations**:
- Carbs: 25-50g (medium to low GI)
- Protein: 10-20g
- Avoid high fat and high fiber

**Example**: Banana + yogurt

#### 2. Post-workout (within 30-60 minutes)

**Recommendations**:
- Protein: 20-30g (muscle repair)
- Carbs: 30-50g (glycogen replenishment)
- Hydration: rehydrate adequately

**Example**: Protein powder + banana + sports drink

### Data Structure

```json
{
  "exercise_prescription": {
    "goals": ["fat_loss", "muscle_preservation"],
    "fitness_level": "intermediate",
    "limitations": ["knee_issue"],

    "cardio_prescription": {
      "type": "mixed",
      "frequency": "5_days_per_week",
      "sessions": [
        {
          "day": "monday",
          "type": "running",
          "duration_minutes": 45,
          "intensity": "moderate",
          "target_hr_zone": "zone_3"
        },
        {
          "day": "wednesday",
          "type": "cycling",
          "duration_minutes": 45,
          "intensity": "moderate"
        },
        {
          "day": "friday",
          "type": "swimming",
          "duration_minutes": 45,
          "intensity": "moderate"
        },
        {
          "day": "saturday",
          "type": "hiit",
          "duration_minutes": 20,
          "intensity": "high",
          "intervals": "30s_on_90s_off_x8"
        }
      ]
    },

    "strength_prescription": {
      "frequency": "3_days_per_week",
      "split": "full_body",
      "exercises": [
        {
          "name": "goblet_squat",
          "sets": 3,
          "reps": "12-15",
          "rest_seconds": 60
        },
        {
          "name": "push_up",
          "sets": 3,
          "reps": "8-12",
          "rest_seconds": 90
        },
        {
          "name": "dumbbell_row",
          "sets": 3,
          "reps": "10-12",
          "rest_seconds": 90
        },
        {
          "name": "lunges",
          "sets": 3,
          "reps": "10_each_leg",
          "rest_seconds": 60
        },
        {
          "name": "plank",
          "sets": 3,
          "reps": "30-60_seconds",
          "rest_seconds": 60
        }
      ]
    },

    "weekly_schedule": {
      "monday": "cardio_45min + strength_upper",
      "tuesday": "cardio_30min",
      "wednesday": "strength_lower",
      "thursday": "cardio_30min",
      "friday": "cardio_45min + strength_full",
      "saturday": "hiit_20min",
      "sunday": "rest_or_yoga"
    },

    "progression": {
      "cardio": {
        "week_1_2": "build_base_30_min",
        "week_3_4": "increase_to_45_min",
        "week_5_8": "add_intervals",
        "progression": "increase_duration_or_intensity"
      },
      "strength": {
        "progression": "progressive_overload",
        "frequency": "increase_when_reps_reach_top_end"
      }
    },

    "pre_workout_nutrition": {
      "timing": "1-2_hours_before",
      "carbs": "25-50g",
      "protein": "10-20g"
    },

    "post_workout_nutrition": {
      "timing": "within_30-60_minutes",
      "protein": "20-30g",
      "carbs": "30-50g",
      "hydration": "500ml_water"
    }
  }
}
```

### Command Interface

```bash
# Exercise prescription
/weightloss exercise plan                  # Generate exercise prescription
/weightloss exercise add running 45 moderate  # Add exercise
/weightloss exercise strength               # Strength training plan
/weightloss exercise schedule               # View exercise schedule

# Exercise logging
/weightloss workout running 45 400         # Log exercise session
/weightloss workout strength               # Log strength training

# View progress
/weightloss exercise progress              # Exercise progress
```

---

## Sub-module 7: Preventing Rebound and Long-Term Maintenance

### Feature Description

Establish long-term maintenance strategies to prevent weight rebound.

### Causes of Rebound

#### 1. Physiological Factors

- **Metabolic adaptation**: BMR decreases
- **Hunger hormone**: Ghrelin elevated
- **Satiety hormone**: Leptin decreased
- **Fat cells**: Fat cell count does not decrease, only shrinks in size

#### 2. Behavioral Factors

- **Diet relaxation**: Unknowingly increasing calorie intake
- **Reduced exercise**: Stopping or reducing exercise frequency
- **Reduced monitoring**: No longer recording and weighing
- **Habit relapse**: Return to unhealthy habits

#### 3. Psychological Factors

- **Sense of goal achievement**: Feeling successful and relaxing
- **Reward mindset**: Rewarding oneself with food
- **Stress and emotions**: Emotional eating

### Maintenance Strategies

#### 1. Weight Monitoring

**Frequency**: 1-2 times per week

**Allowable Range**: ±2 kg is normal

**Action Thresholds**:
- More than +2 kg: Initiate action plan
- More than +3 kg: Return to weight loss phase

#### 2. Maintenance Phase Calories

**Target Calories**: TDEE (no deficit)

**Adjustment Strategy**:
- Stable phase: maintain calories
- Weight rising: reduce by 100-200 calories
- Weight falling: increase by 100-200 calories

#### 3. Continued Exercise

**Minimum Requirements**:
- 150 minutes of moderate-intensity aerobic activity per week
- Or 75 minutes of high-intensity aerobic activity per week
- 2 strength training sessions per week

#### 4. Long-Term Habits

**80/20 Principle**:
- Follow healthy eating 80% of the time
- Be flexible 20% of the time (social events, enjoyment)

**One cheat meal per week**:
- Can eat favorite foods
- But not an all-day indulgence
- Return to normal the next day

#### 5. Self-Monitoring

**Continuous Recording**:
- Weekly weight
- Monthly body fat
- Food diary (flexible)
- Exercise records

**Regular Assessment**:
- Monthly body composition analysis
- Quarterly health checkup
- Annual goal reset

### Data Structure

```json
{
  "maintenance": {
    "start_date": "2025-07-01",
    "goal_weight": 68.0,
    "allowable_range_kg": 2.0,
    "upper_limit": 70.0,
    "lower_limit": 66.0,

    "current_weight": 68.5,
    "weight_status": "within_range",
    "weeks_in_maintenance": 4,

    "maintenance_strategy": "80_20_principle",
    "target_calories": 2558,
    "exercise_minimum": {
      "cardio_minutes_per_week": 150,
      "strength_sessions_per_week": 2
    },

    "weight_tracking": [
      {
        "date": "2025-07-01",
        "weight": 68.0
      },
      {
        "date": "2025-07-08",
        "weight": 68.2
      },
      {
        "date": "2025-07-15",
        "weight": 68.5
      },
      {
        "date": "2025-07-22",
        "weight": 68.3
      }
    ],

    "alerts": [],
    "action_triggered": false,

    "indulgences": {
      "cheat_meals_per_week": 1,
      "preferred_meal": "pizza",
      "adherence": "good"
    },

    "challenges": [],
    "support_system": {
      "accountability_partner": true,
      "support_group": false,
      "professional_support": false
    },

    "relapse_prevention_plan": {
      "triggers": ["stress", "social_events", "vacations"],
      "early_warning_signs": [
        "weight_gain_1kg",
        "clothes_feel_tighter",
        "less_exercise"
      ],
      "action_plan": [
        "increase_monitoring",
        "reduce_calories_200",
        "add_one_extra_cardio_session",
        "revisit_goals_and_motivation"
      ]
    }
  }
}
```

### Command Interface

```bash
# Maintenance phase setup
/weightloss maintenance start               # Enter maintenance phase
/weightloss maintenance weight 68.0        # Set target weight
/weightloss maintenance range 2.0          # Set allowable range

# Monitoring
/weightloss check-in                       # Weekly check-in
/weightloss alert                          # View alerts
/weightloss action-plan                    # Action plan
```

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **No extreme weight loss recommended**
   - Not recommended: <1,200 calories/day (women)
   - Not recommended: <1,500 calories/day (men)
   - Weight loss >1.5 kg/week requires medical supervision

2. **No weight loss medications prescribed**
   - No specific weight loss drugs recommended
   - Medications require a doctor's prescription

3. **No diagnosis of obesity complications**
   - No diagnosis of metabolic syndrome
   - Diagnosis requires a doctor

4. **No treatment of eating disorders**
   - Suspected anorexia or bulimia requires medical attention
   - Requires psychological treatment

### ✅ What the System Can Do

- Body composition analysis
- BMR/TDEE calculation
- Energy deficit management
- Diet and exercise recommendations
- Progress tracking and motivation
- Rebound prevention strategies

---

## Notes

### Weight Loss Safety

- Safest speed: 0.5-1 kg per week
- Do not go below BMI 21-22
- Female body fat not below 20%
- Male body fat not below 15%

### Nutritional Adequacy

- Adequate protein (1.6-2.2 g/kg)
- Adequate micronutrients
- Adequate hydration (2-3 L/day)
- Avoid nutritional deficiencies

### Exercise Safety

- Progress gradually
- Warm up thoroughly
- Avoid overtraining
- Rest and recovery

### Mental Health

- Set realistic goals
- Focus on non-scale victories
- Avoid perfectionism
- Seek support

---

## Reference Resources

### Weight Loss Guidelines
- [Chinese Guidelines for the Diagnosis and Treatment of Obesity](https://www.csco.org.cn/)
- [AHA/ACC Guidelines on the Management of Overweight and Obesity in Adults](https://www.heart.org/)
- [WHO Healthy Diet Guidelines](https://www.who.int/)

### Nutritional Science
- [Chinese Dietary Guidelines](http://www.cnsoc.org/)
- [US Dietary Guidelines](https://www.dietaryguidelines.gov/)
- [Society for Nutrition and Metabolism](https://nutrition.org/)

### Exercise Science
- [ACSM Guidelines for Exercise Testing and Prescription](https://www.acsm.org/)
- [ACE Personal Training Manual](https://www.acefitness.org/)

---

**Document Version**: v1.0
**Last Updated**: 2025-12-31
**Maintainer**: WellAlly Tech
