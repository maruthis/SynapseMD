# Scientific Exercise & Health Weight Loss Module - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend the existing fitness-tracker.json and nutrition-tracker.json to add scientific weight loss features, including body composition analysis, BMR/TDEE calculation, energy deficit management, and weight loss phase tracking.

**Architecture:** Adopt a cross-module integration architecture, adding weight-loss-specific data sections to existing data files, using `module:feature` format command interfaces (e.g., `/fitness:weightloss-body`, `/nutrition:weightloss-deficit`), and reusing existing test script patterns.

**Tech Stack:** Python 3.6+, Bash, JSON, Chart.js, Tailwind CSS

---

## Project Structure

```
SynapseMD/
├── .claude/
│   ├── commands/
│   │   ├── fitness.md          # Extended: add weightloss commands
│   │   └── nutrition.md        # Extended: add weightloss commands
│   └── skills/
│       └── weightloss-analyzer/  # New: weight loss analysis skill
│           └── SKILL.md
├── scripts/
│   ├── weightloss_calculations.py  # New: core calculation module
│   ├── test-weightloss.sh          # New: test script
│   └── generate_health_report.py   # Modified: add weight loss section
├── data-example/
│   ├── fitness-tracker.json    # Modified: add weight_loss_program
│   └── nutrition-tracker.json  # Modified: add weight_loss_energy
└── data/
    ├── fitness-tracker.json    # Modified: sync user data
    └── nutrition-tracker.json  # Modified: sync user data
```

---

## Task Overview

| Task | Description | Estimated Time |
|-----|------|---------|
| Tasks 1-5 | Phase 0: Framework setup (data structures) | 30 minutes |
| Tasks 6-15 | Phase 1: Core calculation module | 45 minutes |
| Tasks 16-25 | Phase 2: Command interface extension | 45 minutes |
| Tasks 26-35 | Phase 3: Test scripts | 30 minutes |
| Tasks 36-40 | Phase 4: Report integration | 30 minutes |

---

## Phase 0: Framework Setup (Data Structures)

### Task 1: Extend data-example/fitness-tracker.json

**Files:**
- Modify: `data-example/fitness-tracker.json`

**Step 1: Back up original file**

```bash
cp data-example/fitness-tracker.json data-example/fitness-tracker.json.backup
```

**Step 2: Add weight_loss_program structure**

Add the `weight_loss_program` field inside the `fitness_tracking` object:

```json
"weight_loss_program": {
  "active": false,
  "start_date": null,

  "body_composition": {
    "current": {
      "date": null,
      "weight_kg": null,
      "height_cm": null,
      "body_fat_percentage": null,
      "muscle_mass_kg": null,
      "waist_cm": null,
      "hip_cm": null,
      "thigh_cm": null,
      "arm_cm": null
    },
    "history": [],
    "goals": {
      "target_weight_kg": null,
      "target_body_fat_percentage": null,
      "target_waist_cm": null,
      "timeline_months": null
    },
    "analysis": {
      "bmi": null,
      "bmi_category": null,
      "ideal_weight": null,
      "weight_to_lose": null,
      "waist_hip_ratio": null,
      "abdominal_obesity": null
    }
  },

  "metabolic_profile": {
    "personal_info": {
      "gender": null,
      "age": null,
      "height_cm": null,
      "weight_kg": null,
      "body_fat_percentage": null
    },
    "bmr_calculations": {
      "harris_benedict": {"bmr": null, "formula": "original_1919"},
      "mifflin_st_jeor": {"bmr": null, "formula": "recommended", "used": true},
      "katch_mcardle": {"bmr": null, "formula": "based_on_lean_mass"}
    },
    "activity_level": {
      "current": "moderate",
      "factor": 1.55,
      "description": "Moderate exercise 3-5 days per week"
    },
    "tdee": {
      "calories": null,
      "calculation": null,
      "breakdown": {
        "bmr_percent": 65,
        "exercise_percent": 20,
        "neat_percent": 15
      }
    },
    "last_calculated": null
  },

  "phase_management": {
    "current_phase": null,
    "phase_start_date": null,
    "phases": {
      "weight_loss": {
        "start_date": null,
        "target_weight_loss_kg": null,
        "actual_weight_loss_kg": null,
        "progress": null,
        "status": null
      },
      "plateau": {
        "occurrences": 0,
        "current_plateau": false,
        "breakthrough_methods": []
      },
      "maintenance": {
        "start_date": null,
        "goal_weight": null,
        "allowable_range_kg": 2.0
      }
    },
    "milestones": []
  }
}
```

**Step 3: Validate JSON format**

```bash
jq . data-example/fitness-tracker.json > /dev/null
echo $?  # Should output 0
```

**Step 4: Commit**

```bash
git add data-example/fitness-tracker.json
git commit -m "feat: add weight_loss_program structure to fitness-tracker.json"
```

---

### Task 2: Extend data-example/nutrition-tracker.json

**Files:**
- Modify: `data-example/nutrition-tracker.json`

**Step 1: Back up original file**

```bash
cp data-example/nutrition-tracker.json data-example/nutrition-tracker.json.backup
```

**Step 2: Add weight_loss_energy structure**

Add the `weight_loss_energy` field inside the `nutrition_tracking` object:

```json
"weight_loss_energy": {
  "calorie_target": null,
  "deficit_target": null,

  "daily_tracking": {
    "date": null,
    "intake_calories": null,
    "exercise_burn": null,
    "neat_burn": null,
    "deficit_achieved": null,
    "deficit_target_met": null
  },

  "daily_history": [],

  "weekly_summary": {
    "week_start": null,
    "avg_intake": null,
    "avg_burn": null,
    "avg_deficit": null,
    "days_on_target": null,
    "days_off_target": null,
    "estimated_weight_loss_kg": null
  },

  "macros_target": {
    "protein": {"grams": null, "calories": null, "percentage": 30},
    "carbs": {"grams": null, "calories": null, "percentage": 40},
    "fat": {"grams": null, "calories": null, "percentage": 30}
  },

  "intermittent_fasting": {
    "enabled": false,
    "method": "16_8",
    "eating_window_start": "12:00",
    "eating_window_end": "20:00",
    "fasting_window_start": "20:00",
    "fasting_window_end": "12:00"
  }
},

"weight_loss_meal_plan": {
  "approach": "balanced_deficit",
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
}
```

**Step 3: Validate JSON format**

```bash
jq . data-example/nutrition-tracker.json > /dev/null
echo $?  # Should output 0
```

**Step 4: Commit**

```bash
git add data-example/nutrition-tracker.json
git commit -m "feat: add weight_loss_energy structure to nutrition-tracker.json"
```

---

### Task 3: Sync user data file data/fitness-tracker.json

**Files:**
- Modify: `data/fitness-tracker.json` (if it exists)

**Step 1: Check if file exists**

```bash
if [ -f "data/fitness-tracker.json" ]; then
    echo "File exists, preparing to extend"
    cp data/fitness-tracker.json data/fitness-tracker.json.backup
else
    echo "File does not exist, skipping"
fi
```

**Step 2: Add the same weight_loss_program structure**

Use the same JSON structure from Task 1 and add it to the user data file.

**Step 3: Validate and commit**

```bash
jq . data/fitness-tracker.json > /dev/null && git add data/fitness-tracker.json
git commit -m "feat: add weight_loss_program to user fitness-tracker.json"
```

---

### Task 4: Sync user data file data/nutrition-tracker.json

**Files:**
- Modify: `data/nutrition-tracker.json` (if it exists)

**Step 1: Check and back up**

```bash
if [ -f "data/nutrition-tracker.json" ]; then
    cp data/nutrition-tracker.json data/nutrition-tracker.json.backup
fi
```

**Step 2: Add the same weight_loss_energy structure**

Use the same JSON structure from Task 2.

**Step 3: Validate and commit**

```bash
jq . data/nutrition-tracker.json > /dev/null && git add data/nutrition-tracker.json
git commit -m "feat: add weight_loss_energy to user nutrition-tracker.json"
```

---

### Task 5: Create weight loss analysis skill directory

**Files:**
- Create: `.claude/skills/weightloss-analyzer/SKILL.md`

**Step 1: Create directory**

```bash
mkdir -p .claude/skills/weightloss-analyzer
```

**Step 2: Create SKILL.md file**

```markdown
---
description: Analyze weight loss data, calculate metabolic rate, track energy deficit, manage weight loss phases
---

# Weight Loss Analysis Skill

## Features

1. **Body Composition Analysis**
   - BMI calculation and classification
   - Body fat percentage assessment
   - Circumference analysis (waist, hip, waist-to-hip ratio)
   - Ideal weight calculation

2. **Metabolic Rate Calculation**
   - Harris-Benedict formula
   - Mifflin-St Jeor formula (recommended)
   - Katch-McArdle formula
   - TDEE calculation

3. **Energy Deficit Management**
   - Daily energy intake tracking
   - Energy expenditure calculation
   - Deficit target analysis
   - Weight loss estimation

4. **Phase Management**
   - Weight loss phase tracking
   - Plateau detection
   - Maintenance phase management

## Usage

Invoked via `/fitness:weightloss-*` and `/nutrition:weightloss-*` commands.

## Safety Principles

- Do not recommend <1200 kcal/day (female) or <1500 kcal/day (male)
- Weight loss rate controlled within 0.5-1 kg/week
- Minimum calories not below BMR × 1.2
- Medical disclaimer
```

**Step 3: Commit**

```bash
git add .claude/skills/weightloss-analyzer/SKILL.md
git commit -m "feat: create weightloss-analyzer skill"
```

---

## Phase 1: Core Calculation Module

### Task 6: Create weightloss_calculations.py framework

**Files:**
- Create: `scripts/weightloss_calculations.py`

**Step 1: Create file header and constants**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scientific weight loss calculation module
Provides scientific calculations for BMR, TDEE, body composition, energy deficit, etc.
"""

from typing import Dict, Any, Tuple, Optional
from datetime import date, datetime
import json


# ==================== Constants ====================

# Body data validation ranges
VALID_WEIGHT_RANGE = (30, 300)  # kg
VALID_HEIGHT_RANGE = (100, 250)  # cm
VALID_BODY_FAT_RANGE = (3, 50)   # %
VALID_WAIST_RANGE = (50, 150)    # cm

# Activity factors
ACTIVITY_FACTORS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9
}

# Body fat percentage standards
BODY_FAT_STANDARDS = {
    "male": {
        "essential": (2, 5),
        "athletic": (6, 13),
        "fitness": (14, 17),
        "average": (18, 24),
        "obese": (25, None)
    },
    "female": {
        "essential": (10, 13),
        "athletic": (14, 20),
        "fitness": (21, 24),
        "average": (25, 31),
        "obese": (32, None)
    }
}

# Energy deficit standard (7700 kcal = 1 kg of fat)
CALORIES_PER_KG_FAT = 7700


def main():
    """Test entry point"""
    print("Weight loss calculation module")


if __name__ == "__main__":
    main()
```

**Step 2: Test run**

```bash
python3 scripts/weightloss_calculations.py
# Expected output: Weight loss calculation module
```

**Step 3: Commit**

```bash
git add scripts/weightloss_calculations.py
git commit -m "feat: create weightloss_calculations.py framework"
```

---

### Task 7: Implement BMR calculation functions

**Files:**
- Modify: `scripts/weightloss_calculations.py`

**Step 1: Add three BMR calculation formulas**

Add after the constants:

```python
# ==================== BMR Calculation Formulas ====================

def calculate_bmr_harris_benedict(
    gender: str,
    weight_kg: float,
    height_cm: float,
    age: int
) -> int:
    """
    Harris-Benedict original formula (1919)

    Male: BMR = 88.362 + (13.397 × weight) + (4.799 × height) - (5.677 × age)
    Female: BMR = 447.593 + (9.247 × weight) + (3.098 × height) - (4.330 × age)
    """
    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    return int(bmr)


def calculate_bmr_mifflin_st_jeor(
    gender: str,
    weight_kg: float,
    height_cm: float,
    age: int
) -> int:
    """
    Mifflin-St Jeor formula (recommended, more accurate)

    Male: BMR = (10 × weight) + (6.25 × height) - (5 × age) + 5
    Female: BMR = (10 × weight) + (6.25 × height) - (5 × age) - 161
    """
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    return int(bmr)


def calculate_bmr_katch_mcardle(
    weight_kg: float,
    body_fat_percentage: float
) -> int:
    """
    Katch-McArdle formula (based on lean body mass)

    BMR = 370 + (21.6 × lean body mass kg)
    """
    lean_mass_kg = weight_kg * (1 - body_fat_percentage / 100)
    bmr = 370 + (21.6 * lean_mass_kg)
    return int(bmr)
```

**Step 2: Update main function for testing**

```python
def main():
    """Test BMR calculations"""
    # Test data: 35-year-old male, 170cm, 75.5kg
    gender, age = "male", 35
    height, weight = 170, 75.5

    print("=== BMR Calculation Test ===")
    print(f"Harris-Benedict: {calculate_bmr_harris_benedict(gender, weight, height, age)}")
    print(f"Mifflin-St Jeor: {calculate_bmr_mifflin_st_jeor(gender, weight, height, age)}")
    print(f"Katch-McArdle (28.5% body fat): {calculate_bmr_katch_mcardle(weight, 28.5)}")
```

**Step 3: Run test**

```bash
python3 scripts/weightloss_calculations.py
# Expected output:
# === BMR Calculation Test ===
# Harris-Benedict: 1728
# Mifflin-St Jeor: 1650
# Katch-McArdle (28.5% body fat): 1536
```

**Step 4: Commit**

```bash
git add scripts/weightloss_calculations.py
git commit -m "feat: implement BMR calculation formulas"
```

---

### Task 8: Implement body composition analysis functions

**Files:**
- Modify: `scripts/weightloss_calculations.py`

**Step 1: Add body composition analysis functions**

```python
# ==================== Body Composition Analysis ====================

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate Body Mass Index (BMI)"""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def get_bmi_category(bmi: float) -> str:
    """Get BMI classification (Asian standard)"""
    if bmi < 18.5:
        return "underweight"
    elif bmi < 24:
        return "normal"
    elif bmi < 28:
        return "overweight"
    else:
        return "obese"


def calculate_ideal_weight(height_cm: float) -> float:
    """Calculate ideal weight (Asian standard BMI=22)"""
    height_m = height_cm / 100
    return round(height_m ** 2 * 22, 1)


def calculate_waist_hip_ratio(waist_cm: float, hip_cm: float) -> float:
    """Calculate waist-to-hip ratio"""
    return round(waist_cm / hip_cm, 2)


def has_abdominal_obesity(gender: str, waist_cm: float) -> bool:
    """Determine if there is abdominal obesity"""
    if gender.lower() == "male":
        return waist_cm > 90
    else:
        return waist_cm > 85


def get_body_fat_category(gender: str, body_fat_pct: float) -> str:
    """Get body fat percentage classification"""
    standards = BODY_FAT_STANDARDS.get(gender.lower(), BODY_FAT_STANDARDS["male"])

    for category, (low, high) in standards.items():
        if high is None:
            if body_fat_pct >= low:
                return category
        elif low <= body_fat_pct <= high:
            return category

    return "obese"
```

**Step 2: Add test to main function**

```python
def main():
    """Test body composition analysis"""
    print("=== Body Composition Analysis Test ===")

    # Test data: 170cm, 75.5kg
    height, weight = 170, 75.5
    bmi = calculate_bmi(weight, height)
    print(f"BMI: {bmi} ({get_bmi_category(bmi)})")
    print(f"Ideal weight: {calculate_ideal_weight(height)}kg")
    print(f"Waist-to-hip ratio (92/98): {calculate_waist_hip_ratio(92, 98)}")
    print(f"Abdominal obesity (male, 92cm): {has_abdominal_obesity('male', 92)}")
    print(f"Body fat classification (male, 28.5%): {get_body_fat_category('male', 28.5)}")
```

**Step 3: Run test**

```bash
python3 scripts/weightloss_calculations.py
# Expected output:
# === Body Composition Analysis Test ===
# BMI: 26.1 (overweight)
# Ideal weight: 63.6kg
# Waist-to-hip ratio (92/98): 0.94
# Abdominal obesity (male, 92cm): True
# Body fat classification (male, 28.5%): obese
```

**Step 4: Commit**

```bash
git add scripts/weightloss_calculations.py
git commit -m "feat: implement body composition analysis functions"
```

---

### Task 9: Implement energy deficit calculation functions

**Files:**
- Modify: `scripts/weightloss_calculations.py`

**Step 1: Add energy deficit calculation functions**

```python
# ==================== Energy Deficit Calculation ====================

def calculate_deficit(
    intake_calories: int,
    bmr: int,
    exercise_burn: int = 0,
    neat_burn: int = 0,
    tef_factor: float = 0.1
) -> Dict[str, Any]:
    """
    Calculate energy deficit

    Energy intake < energy expenditure = weight loss
    Energy expenditure = BMR + exercise + NEAT + Thermic Effect of Food (TEF)
    """
    tef = int(intake_calories * tef_factor)
    total_expenditure = bmr + exercise_burn + neat_burn + tef
    deficit = total_expenditure - intake_calories

    return {
        "intake": intake_calories,
        "expenditure": {
            "bmr": bmr,
            "exercise": exercise_burn,
            "neat": neat_burn,
            "tef": tef,
            "total": total_expenditure
        },
        "deficit": deficit if deficit > 0 else 0,
        "surplus": -deficit if deficit < 0 else 0
    }


def estimate_weight_loss(
    deficit_calories: int,
    days: int = 7
) -> float:
    """
    Estimate weight loss

    Losing 1 kg of fat requires burning approximately 7700 kcal
    """
    total_deficit = deficit_calories * days
    weight_loss_kg = total_deficit / CALORIES_PER_KG_FAT
    return round(weight_loss_kg, 2)


def calculate_macros(
    target_calories: int,
    protein_pct: float = 0.30,
    carbs_pct: float = 0.40,
    fat_pct: float = 0.30
) -> Dict[str, Dict[str, Any]]:
    """Calculate macronutrient distribution"""
    protein_cals = int(target_calories * protein_pct)
    carbs_cals = int(target_calories * carbs_pct)
    fat_cals = int(target_calories * fat_pct)

    return {
        "protein": {
            "grams": round(protein_cals / 4),
            "calories": protein_cals,
            "percentage": int(protein_pct * 100)
        },
        "carbs": {
            "grams": round(carbs_cals / 4),
            "calories": carbs_cals,
            "percentage": int(carbs_pct * 100)
        },
        "fat": {
            "grams": round(fat_cals / 9),
            "calories": fat_cals,
            "percentage": int(fat_pct * 100)
        }
    }
```

**Step 2: Add test to main function**

```python
def main():
    """Test energy deficit calculation"""
    print("=== Energy Deficit Calculation Test ===")

    deficit = calculate_deficit(intake_calories=1980, bmr=1650, exercise_burn=400, neat_burn=300)
    print(f"Intake: {deficit['intake']} kcal")
    print(f"Expenditure: {deficit['expenditure']['total']} kcal")
    print(f"Deficit: {deficit['deficit']} kcal")
    print(f"Estimated weekly weight loss: {estimate_weight_loss(deficit['deficit'], 7)} kg")

    macros = calculate_macros(2058)
    print(f"\nMacronutrients (2058 kcal):")
    print(f"  Protein: {macros['protein']['grams']}g ({macros['protein']['percentage']}%)")
    print(f"  Carbs: {macros['carbs']['grams']}g ({macros['carbs']['percentage']}%)")
    print(f"  Fat: {macros['fat']['grams']}g ({macros['fat']['percentage']}%)")
```

**Step 3: Run test**

```bash
python3 scripts/weightloss_calculations.py
# Expected output includes:
# Deficit: 520 kcal
# Estimated weekly weight loss: 0.47 kg
```

**Step 4: Commit**

```bash
git add scripts/weightloss_calculations.py
git commit -m "feat: implement energy deficit calculation functions"
```

---

### Task 10: Implement plateau detection functions

**Files:**
- Modify: `scripts/weightloss_calculations.py`

**Step 1: Add plateau detection functions**

```python
# ==================== Phase Management ====================

def detect_plateau(
    weight_history: list,
    weeks: int = 2,
    threshold_kg: float = 0.5
) -> Dict[str, Any]:
    """
    Detect whether a weight loss plateau has been reached

    Criteria: weight change less than threshold within specified number of weeks
    """
    if len(weight_history) < weeks:
        return {"in_plateau": False, "reason": "Insufficient data"}

    recent = weight_history[-weeks:]
    weights = [w.get("weight", 0) for w in recent]

    weight_change = abs(weights[-1] - weights[0])

    if weight_change < threshold_kg:
        return {
            "in_plateau": True,
            "duration_weeks": weeks,
            "weight_change_kg": round(weight_change, 2),
            "recent_weights": weights
        }

    return {"in_plateau": False, "weight_change_kg": round(weight_change, 2)}


def suggest_plateau_breakthrough(
    plateau_duration_weeks: int
) -> list:
    """Suggest plateau breakthrough methods based on plateau duration"""
    suggestions = []

    if plateau_duration_weeks <= 2:
        suggestions = [
            "Keep going, don't give up",
            "Check if your food records are accurate",
            "Increase NEAT (daily activity)"
        ]
    elif plateau_duration_weeks <= 4:
        suggestions = [
            "Adjust calories: reduce by another 100-200 kcal",
            "Increase cardio exercise time by 10-15 minutes",
            "Try a new type of exercise to stimulate metabolism"
        ]
    else:
        suggestions = [
            "Consider a diet break (maintain calories for 1-2 weeks)",
            "Try carb cycling",
            "Try intermittent fasting (16:8)",
            "Consider consulting a nutritionist"
        ]

    return suggestions
```

**Step 2: Add test to main function**

```python
def main():
    """Test plateau detection"""
    print("=== Plateau Detection Test ===")

    # Simulate weight history
    weight_history = [
        {"date": "2025-01-01", "weight": 78.0},
        {"date": "2025-01-08", "weight": 77.8},
        {"date": "2025-01-15", "weight": 77.7},  # Change of 0.3kg, less than 0.5kg threshold
    ]

    plateau = detect_plateau(weight_history, weeks=2)
    print(f"Plateau: {plateau['in_plateau']}")
    if plateau.get('in_plateau'):
        print(f"Duration: {plateau['duration_weeks']} weeks")
        print(f"Weight change: {plateau['weight_change_kg']} kg")
        print(f"Breakthrough suggestions: {suggest_plateau_breakthrough(plateau['duration_weeks'])}")
```

**Step 3: Run test**

```bash
python3 scripts/weightloss_calculations.py
# Expected output: Plateau: True
```

**Step 4: Commit**

```bash
git add scripts/weightloss_calculations.py
git commit -m "feat: implement plateau detection functions"
```

---

### Tasks 11-15: Implement comprehensive analysis functions and helper functions

**Brief descriptions (detailed steps omitted)**:

**Task 11**: Implement `calculate_tdee()` and `calculate_all_bmr()` functions
**Task 12**: Implement `validate_calorie_target()` and `validate_weight_loss_rate()` safety validation functions
**Task 13**: Implement `analyze_body_composition()` comprehensive analysis function
**Task 14**: Implement `analyze_metabolic_profile()` comprehensive metabolic analysis function
**Task 15**: Complete `main()` function, add full test suite

Each task follows: write code → run tests → commit

---

## Phase 2: Command Interface Extension

### Task 16: Extend .claude/commands/fitness.md

**Files:**
- Modify: `.claude/commands/fitness.md`

**Step 1: Add weight loss command section at the end of the file**

```markdown
---

## Weight Loss Management Commands

⚠️ **Weight Loss Safety Statement**
The weight loss recommendations provided by this system are based on scientific principles and do not constitute medical prescriptions.
For extreme weight loss or eating disorders, please consult a doctor.

### Body Composition Recording

```bash
# Record weight
/fitness:weightloss-record weight 75.5

# Record body fat percentage
/fitness:weightloss-record body-fat 28.5%

# Record measurements
/fitness:weightloss-record waist 92
/fitness:weightloss-record hip 98
```

### Body Composition Analysis

```bash
/fitness:weightloss-body              # Full body composition analysis
/fitness:weightloss-trend weight      # Weight trend
/fitness:weightless-progress          # Weight loss progress
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
```

**Step 2: Commit**

```bash
git add .claude/commands/fitness.md
git commit -m "feat: add weightloss commands to fitness.md"
```

---

### Task 17: Extend .claude/commands/nutrition.md

**Files:**
- Modify: `.claude/commands/nutrition.md`

**Step 1: Add weight loss diet command section at the end of the file**

```markdown
---

## Weight Loss Diet Management

### Energy Deficit Tracking

```bash
/nutrition:weightloss-deficit          # View today's energy deficit
/nutrition:weightloss-target           # View calorie target
/nutrition:weightloss-balance          # Energy balance report
```

### Diet Records

```bash
/nutrition:weightloss-meal breakfast 450   # Record breakfast
/nutrition:weightloss-intake 1980          # Record total daily intake
/nutrition:weightloss-protein              # Protein analysis
```

### Intermittent Fasting

```bash
/nutrition:weightloss-if 16-8                   # Enable 16:8 fasting
/nutrition:weightloss-if window 12:00-20:00     # Set eating window
/nutrition:weightloss-if disable                # Disable
```
```

**Step 2: Commit**

```bash
git add .claude/commands/nutrition.md
git commit -m "feat: add weightloss commands to nutrition.md"
```

---

### Tasks 18-25: Implement command handling logic

**Since the current project uses the Claude Code skill system to handle commands**, these tasks mainly ensure the skill files can correctly parse and respond to new commands.

Brief descriptions:
- Task 18: Verify `/fitness:weightloss-*` commands are correctly routed
- Task 19: Verify `/nutrition:weightloss-*` commands are correctly routed
- Tasks 20-25: Feature implementation for each command (in skill files)

---

## Phase 3: Test Scripts

### Task 26: Create test-weightloss.sh framework

**Files:**
- Create: `scripts/test-weightloss.sh`

**Step 1: Create test script framework**

```bash
#!/bin/bash

# Scientific exercise & health weight loss feature test script
# Version: v1.0
# Creation date: 2025-01-14

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
declare -a FAILED_TEST_NAMES

# ========================================
# Helper functions
# ========================================

test_file() {
    local file="$1"
    local description="$2"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo -n "Test $TOTAL_TESTS: $description ... "

    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ Pass${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ Fail${NC}"
        echo "   File does not exist: $file"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        FAILED_TEST_NAMES+=("$description")
        return 1
    fi
}

test_json_structure() {
    local file="$1"
    local key="$2"
    local description="$3"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo -n "Test $TOTAL_TESTS: $description ... "

    if grep -q "\"$key\"" "$file" 2>/dev/null; then
        echo -e "${GREEN}✅ Pass${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ Fail${NC}"
        echo "   Key '$key' does not exist in $file"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        FAILED_TEST_NAMES+=("$description")
        return 1
    fi
}

test_disclaimer_in_file() {
    local file="$1"
    local description="$2"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo -n "Test $TOTAL_TESTS: $description ... "

    if grep -q "disclaimer\|Disclaimer\|DISCLAIMER" "$file" 2>/dev/null; then
        echo -e "${GREEN}✅ Pass${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ Fail${NC}"
        echo "   Disclaimer not found in file"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        FAILED_TEST_NAMES+=("$description")
        return 1
    fi
}

# ========================================
# Start tests
# ========================================

echo "========================================="
echo "Scientific Exercise & Health Weight Loss Feature Test"
echo "========================================="
echo ""

# Group 1: Basic functionality tests
echo -e "${YELLOW}Group 1: Basic Functionality Tests${NC}"
echo ""

test_file "scripts/weightloss_calculations.py" "Calculation module exists"
test_file "scripts/test-weightloss.sh" "Test script exists"
test_file ".claude/skills/weightloss-analyzer/SKILL.md" "Weight loss analysis skill exists"

echo ""

# Group 2: Data structure tests
echo -e "${YELLOW}Group 2: Data Structure Tests${NC}"
echo ""

test_file "data-example/fitness-tracker.json" "Exercise data file exists"
test_json_structure "data-example/fitness-tracker.json" "weight_loss_program" "Weight loss program structure exists"
test_json_structure "data-example/fitness-tracker.json" "body_composition" "Body composition structure exists"
test_json_structure "data-example/fitness-tracker.json" "metabolic_profile" "Metabolic analysis structure exists"

test_file "data-example/nutrition-tracker.json" "Nutrition data file exists"
test_json_structure "data-example/nutrition-tracker.json" "weight_loss_energy" "Energy management structure exists"
test_json_structure "data-example/nutrition-tracker.json" "intermittent_fasting" "Intermittent fasting structure exists"

echo ""

# Group 3: Command interface tests
echo -e "${YELLOW}Group 3: Command Interface Tests${NC}"
echo ""

test_disclaimer_in_file ".claude/commands/fitness.md" "fitness commands include disclaimer"
test_disclaimer_in_file ".claude/commands/nutrition.md" "nutrition commands include disclaimer"

echo ""
echo "========================================="
echo "Tests complete"
echo "========================================="
echo -e "Total: ${TOTAL_TESTS} | ${GREEN}Passed: ${PASSED_TESTS}${NC} | ${RED}Failed: ${FAILED_TESTS}${NC}"

if [ $FAILED_TESTS -gt 0 ]; then
    echo ""
    echo "Failed tests:"
    for name in "${FAILED_TEST_NAMES[@]}"; do
        echo "  - $name"
    done
    exit 1
else
    echo ""
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
```

**Step 2: Add execute permission**

```bash
chmod +x scripts/test-weightloss.sh
```

**Step 3: Run test**

```bash
bash scripts/test-weightloss.sh
```

**Step 4: Commit**

```bash
git add scripts/test-weightloss.sh
git commit -m "feat: create weightloss test script"
```

---

### Tasks 27-35: Complete test script

Add more test cases:
- Task 27: Add medical safety tests
- Task 28: Add command format tests
- Task 29: Add calculation function unit tests
- Tasks 30-35: Other edge case tests

---

## Phase 4: Report Integration

### Task 36: Add weight loss section function in generate_health_report.py

**Files:**
- Modify: `scripts/generate_health_report.py`

**Step 1: Add weight loss section generation function**

Find the location of other section functions in the file and add:

```python
def generate_weight_loss_section(data: Dict) -> str:
    """
    Generate weight loss section HTML

    Includes: body composition overview, metabolic analysis, energy balance, weight loss progress
    """
    html = '''
    <section id="weight-loss" class="mb-8">
        <div class="flex items-center gap-2 mb-4">
            <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
            </svg>
            <h2 class="text-xl font-bold text-gray-800">Scientific Exercise & Health Weight Loss</h2>
        </div>

        <div class="bg-amber-50 border-l-4 border-amber-400 p-4 mb-6">
            <div class="flex">
                <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-amber-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                </div>
                <div class="ml-3">
                    <p class="text-sm text-amber-700">
                        <strong>Disclaimer:</strong> The weight loss recommendations provided by this tool are based on general scientific principles and do not constitute medical diagnosis or prescription.
                        For extreme weight loss, eating disorders, or obesity-related diseases, please consult a professional physician.
                    </p>
                </div>
            </div>
        </div>

        <!-- Body composition overview -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-lg shadow p-4">
                <div class="text-sm text-gray-500">Weight</div>
                <div class="text-2xl font-bold text-gray-800">{{ weight }} kg</div>
                <div class="text-xs text-emerald-600 mt-1">Target: {{ target_weight }} kg</div>
            </div>
            <!-- More cards... -->
        </div>

        <!-- Weight trend chart -->
        <div class="bg-white rounded-lg shadow p-4 mb-6">
            <h3 class="text-lg font-semibold mb-4">Weight Change Trend</h3>
            <canvas id="weightTrendChart" height="200"></canvas>
        </div>
    </section>
    '''

    return html
```

**Step 2: Commit**

```bash
git add scripts/generate_health_report.py
git commit -m "feat: add weight loss section to health report"
```

---

### Tasks 37-40: Complete report charts and integration

- Task 37: Add weight trend Chart.js chart
- Task 38: Add energy deficit chart
- Task 39: Call weight loss section in main report generation function
- Task 40: Test full report generation

---

## Completion Checklist

After completing all tasks, verify:

- [ ] `data-example/fitness-tracker.json` contains `weight_loss_program` structure
- [ ] `data-example/nutrition-tracker.json` contains `weight_loss_energy` structure
- [ ] `scripts/weightloss_calculations.py` all calculation functions work correctly
- [ ] `scripts/test-weightloss.sh` all tests pass
- [ ] `/fitness:weightloss-*` and `/nutrition:weightloss-*` commands are available
- [ ] Health report includes weight loss section

---

## Run Full Tests

```bash
# Run weight loss module tests
bash scripts/test-weightloss.sh

# Test calculation module
python3 scripts/weightloss_calculations.py

# Generate health report (verify integration)
python3 scripts/generate_health_report.py comprehensive
```

---

**Plan Version**: v1.0
**Creation Date**: 2025-01-14
**Estimated Total Duration**: 3-4 hours
