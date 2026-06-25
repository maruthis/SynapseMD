# Scientific Exercise & Health Weight Loss Module - Detailed Design Document

**Module Number**: 24
**Creation Date**: 2025-01-14
**Design Version**: v1.0
**Status**: Design complete, pending implementation

---

## Table of Contents

1. [Overview](#overview)
2. [Overall Architecture](#overall-architecture)
3. [Data Structure Design](#data-structure-design)
4. [Command Interface Design](#command-interface-design)
5. [Python Script Extensions](#python-script-extensions)
6. [Health Report Integration](#health-report-integration)
7. [Error Handling and Safety](#error-handling-and-safety)
8. [Implementation Roadmap](#implementation-roadmap)

---

## Overview

### Design Goals

The scientific exercise & health weight loss module adopts a **cross-module integration architecture**, extending weight-loss-specific features based on the existing `fitness-tracker.json` and `nutrition-tracker.json` to achieve:

- Body composition analysis (weight, body fat, muscle mass, measurements)
- Basal metabolic rate calculations (BMR/TDEE, multiple formulas)
- Energy deficit management (scientific calorie control)
- Weight loss phase management (weight loss / plateau / maintenance phases)
- Diet and exercise balance
- Rebound prevention strategies

### Design Principles

| Principle | Description |
|-----|------|
| Integration first | Reuse existing fitness/nutrition modules, avoid reinventing the wheel |
| Scientific safety | Follow nutritional and exercise science principles, set safety boundaries |
| Progressive implementation | Build the framework first, then fill in features, ensure architectural consistency |
| Visualization-friendly | Integrate with health reports, provide intuitive chart displays |

---

## Overall Architecture

### Cross-Module Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Weight Loss Module                      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐      ┌──────────────────────┐ │
│  │ /fitness:weightloss-* │      │ /nutrition:weightloss-*││
│  │                      │      │                      │ │
│  │ • body-composition   │      │ • deficit           │ │
│  │ • bmr/tdee           │◄────►│ • meal              │ │
│  │ • phase              │      │ • target            │ │
│  │ • progress           │      │ • balance           │ │
│  └──────────┬───────────┘      └──────────┬───────────┘ │
│             │                             │             │
│             └──────────┬──────────────────┘             │
│                        ▼                                │
│         ┌──────────────────────────┐                    │
│         │  fitness-tracker.json     │                    │
│         │  nutrition-tracker.json   │                    │
│         └──────────────────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

### Data Layer Architecture

**fitness-tracker.json extensions**:
- `weight_loss_program.body_composition` - Body composition records
- `weight_loss_program.metabolic_profile` - Metabolic rate data
- `weight_loss_program.phase_management` - Phase management
- `weight_loss_program.exercise_prescription` - Exercise prescription

**nutrition-tracker.json extensions**:
- `weight_loss_energy` - Energy deficit tracking
- `weight_loss_meal_plan` - Weight loss meal plan
- `intermittent_fasting` - Intermittent fasting settings

---

## Data Structure Design

### fitness-tracker.json Extension

```json
{
  "fitness_tracking": {
    "weight_loss_program": {
      "active": false,
      "start_date": null,

      "body_composition": {
        "current": {
          "date": "2025-01-15",
          "weight_kg": 75.5,
          "height_cm": 170,
          "body_fat_percentage": 28.5,
          "muscle_mass_kg": 32.5,
          "waist_cm": 92,
          "hip_cm": 98,
          "thigh_cm": 58,
          "arm_cm": 32
        },
        "history": [
          {
            "date": "2025-01-01",
            "weight_kg": 78.0,
            "body_fat_percentage": 30.0,
            "waist_cm": 95
          }
        ],
        "goals": {
          "target_weight_kg": 68.0,
          "target_body_fat_percentage": 20,
          "target_waist_cm": 85,
          "timeline_months": 6
        },
        "analysis": {
          "bmi": 26.1,
          "bmi_category": "overweight",
          "ideal_weight": 63.6,
          "weight_to_lose": 7.5,
          "waist_hip_ratio": 0.94,
          "abdominal_obesity": true
        }
      },

      "metabolic_profile": {
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
          "calculation": "BMR_1650 × 1.55",
          "breakdown": {
            "bmr_percent": 65,
            "exercise_percent": 20,
            "neat_percent": 15
          }
        },
        "last_calculated": "2025-01-15"
      },

      "phase_management": {
        "current_phase": "weight_loss",
        "phase_start_date": "2025-01-01",
        "phases": {
          "weight_loss": {
            "start_date": "2025-01-01",
            "target_weight_loss_kg": 10,
            "actual_weight_loss_kg": 2.5,
            "progress": 0.25,
            "status": "on_track"
          },
          "plateau": {
            "occurrences": 0,
            "current_plateau": false,
            "breakthrough_methods": []
          },
          "maintenance": {
            "start_date": null,
            "goal_weight": 68.0,
            "allowable_range_kg": 2.0
          }
        },
        "milestones": [
          {
            "title": "Lost 2.5 kg",
            "target_value": 72.5,
            "achieved_date": null,
            "achieved": false
          }
        ]
      },

      "exercise_prescription": {
        "goals": ["fat_loss", "muscle_preservation"],
        "fitness_level": "intermediate",

        "cardio_prescription": {
          "frequency": "5_days_per_week",
          "sessions": [
            {
              "day": "monday",
              "type": "running",
              "duration_minutes": 45,
              "intensity": "moderate"
            },
            {
              "day": "saturday",
              "type": "hiit",
              "duration_minutes": 20,
              "intensity": "high"
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
              "reps": "12-15"
            },
            {
              "name": "push_up",
              "sets": 3,
              "reps": "8-12"
            }
          ]
        }
      }
    }
  }
}
```

### nutrition-tracker.json Extension

```json
{
  "nutrition_tracking": {
    "weight_loss_energy": {
      "calorie_target": 2058,
      "deficit_target": 500,

      "daily_tracking": {
        "date": "2025-01-15",
        "intake_calories": 1980,
        "exercise_burn": 400,
        "neat_burn": 300,
        "deficit_achieved": 520,
        "deficit_target_met": true
      },

      "daily_history": [],

      "weekly_summary": {
        "week_start": "2025-01-13",
        "avg_intake": 2030,
        "avg_burn": 2510,
        "avg_deficit": 480,
        "days_on_target": 5,
        "days_off_target": 2,
        "estimated_weight_loss_kg": 0.44
      },

      "macros_target": {
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
  }
}
```

---

## Command Interface Design

### /fitness Module Commands

```bash
# Body composition recording
/fitness:weightloss-record weight 75.5           # Record weight (kg)
/fitness:weightloss-record body-fat 28.5%        # Record body fat percentage
/fitness:weightloss-record muscle 32.5kg         # Record muscle mass
/fitness:weightloss-record waist 92              # Record waist circumference (cm)
/fitness:weightloss-record hip 98                # Record hip circumference (cm)

# Body composition analysis
/fitness:weightloss-body                         # Full body composition analysis
/fitness:weightless-trend weight                 # Weight trend analysis
/fitness:weightloss-trend body-fat               # Body fat trend analysis
/fitness:weightloss-progress                     # Weight loss progress report

# Metabolic rate calculation
/fitness:weightloss-bmr                          # Calculate BMR (shows multiple formulas)
/fitness:weightloss-tdee                         # Calculate TDEE
/fitness:weightloss-activity moderate            # Set activity level
# Activity level options: sedentary, light, moderate, active, very_active

# Phase management
/fitness:weightloss-phase weight-loss            # Set to weight loss phase
/fitness:weightloss-phase plateau                # Mark entering plateau phase
/fitness:weightloss-phase breakdown <method>     # Record breakthrough method
/fitness:weightloss-maintenance start            # Enter maintenance phase
/fitness:weightloss-maintenance weight 68.0      # Set maintenance weight

# Exercise prescription
/fitness:weightloss-exercise plan                # Generate exercise prescription
/fitness:weightloss-exercise schedule            # View exercise schedule
```

### /nutrition Module Commands

```bash
# Energy deficit tracking
/nutrition:weightloss-deficit                    # View today's energy deficit
/nutrition:weightloss-target                     # View calorie target
/nutrition:weightloss-balance                    # Energy balance report
/nutrition:weightloss-estimate-loss              # Estimate weight loss

# Diet records
/nutrition:weightloss-meal breakfast 450         # Record breakfast calories
/nutrition:weightloss-meal dinner 600            # Record dinner calories
/nutrition:weightloss-intake 1980                # Record total daily intake
/nutrition:weightloss-protein                    # Protein intake analysis
/nutrition:weightloss-adherence                  # Diet adherence analysis

# Intermittent fasting
/nutrition:weightloss-if 16-8                    # Enable 16:8 fasting
/nutrition:weightloss-if 5-2                     # Enable 5:2 fasting
/nutrition:weightloss-if window 12:00-20:00      # Set eating window
/nutrition:weightloss-if disable                 # Disable intermittent fasting
```

### Cross-Module Combined Commands

```bash
# Comprehensive analysis (reads both files)
/fitness:weightloss-comprehensive                # Comprehensive weight loss report
# Or shorthand
/wl:report                                      # Weight loss comprehensive report

# Milestone records
/fitness:weightloss-milestone 5kg new-clothes    # Record milestone
/fitness:weightloss-milestones list              # View all milestones
```

---

## Python Script Extensions

### Create weightloss_calculations.py

**File path**: `scripts/weightloss_calculations.py

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
    "sedentary": 1.2,      # Sedentary, little or no exercise
    "light": 1.375,        # Light activity
    "moderate": 1.55,      # Moderate activity
    "active": 1.725,       # High activity
    "very_active": 1.9     # Extreme activity
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


def calculate_all_bmr(
    gender: str,
    weight_kg: float,
    height_cm: float,
    age: int,
    body_fat_percentage: Optional[float] = None
) -> Dict[str, Any]:
    """Calculate all BMR formulas and return comparison results"""
    results = {
        "harris_benedict": {
            "bmr": calculate_bmr_harris_benedict(gender, weight_kg, height_cm, age),
            "formula": "original_1919"
        },
        "mifflin_st_jeor": {
            "bmr": calculate_bmr_mifflin_st_jeor(gender, weight_kg, height_cm, age),
            "formula": "recommended",
            "used": True
        }
    }

    if body_fat_percentage is not None:
        results["katch_mcardle"] = {
            "bmr": calculate_bmr_katch_mcardle(weight_kg, body_fat_percentage),
            "formula": "based_on_lean_mass",
            "lean_body_mass_kg": round(weight_kg * (1 - body_fat_percentage / 100), 1)
        }

    return results


def calculate_tdee(bmr: int, activity_level: str) -> int:
    """Calculate Total Daily Energy Expenditure (TDEE)"""
    factor = ACTIVITY_FACTORS.get(activity_level, 1.2)
    return int(bmr * factor)


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


# ==================== Safety Validation ====================

def validate_calorie_target(
    target_calories: int,
    bmr: int,
    gender: str
) -> Dict[str, Any]:
    """Validate whether calorie target is safe"""
    minimum_safe = int(bmr * 1.2)

    result = {"safe": True, "warnings": []}

    if target_calories < minimum_safe:
        result["safe"] = False
        result["minimum"] = minimum_safe
        result["warnings"].append(
            f"Calorie target ({target_calories}) is below the safe minimum ({minimum_safe}), "
            "which may affect metabolic health"
        )

    gender_minimum = 1200 if gender.lower() == "female" else 1500
    if target_calories < gender_minimum:
        result["warnings"].append(
            f"Calorie target is below the minimum recommended value of {gender_minimum} kcal"
        )

    return result


def validate_weight_loss_rate(
    weight_loss_kg: float,
    weeks: int
) -> Dict[str, Any]:
    """Validate whether weight loss rate is safe"""
    weekly_rate = weight_loss_kg / weeks

    result = {"safe": True, "warnings": [], "weekly_rate": round(weekly_rate, 2)}

    if weekly_rate > 1.5:
        result["safe"] = False
        result["warnings"].append(
            f"Weight loss rate ({weekly_rate:.1f} kg/week) is too fast; medical supervision required"
        )
    elif weekly_rate > 1.0:
        result["warnings"].append(
            f"Weight loss rate ({weekly_rate:.1f} kg/week) is fast; recommend staying within 0.5-1 kg/week"
        )

    return result


# ==================== Main Analysis Functions ====================

def analyze_body_composition(
    gender: str,
    age: int,
    height_cm: float,
    weight_kg: float,
    body_fat_percentage: Optional[float] = None,
    waist_cm: Optional[float] = None,
    hip_cm: Optional[float] = None
) -> Dict[str, Any]:
    """Comprehensive body composition analysis"""
    result = {
        "assessment_date": str(date.today()),
        "personal_info": {
            "gender": gender,
            "age": age,
            "height_cm": height_cm,
            "weight_kg": weight_kg
        }
    }

    # BMI analysis
    bmi = calculate_bmi(weight_kg, height_cm)
    result["bmi"] = {
        "value": bmi,
        "category": get_bmi_category(bmi),
        "ideal_weight": calculate_ideal_weight(height_cm),
        "weight_to_lose": round(weight_kg - calculate_ideal_weight(height_cm), 1)
    }

    # Body fat analysis
    if body_fat_percentage:
        result["body_fat"] = {
            "percentage": body_fat_percentage,
            "category": get_body_fat_category(gender, body_fat_percentage),
            "mass_kg": round(weight_kg * body_fat_percentage / 100, 1)
        }

    # Circumference analysis
    if waist_cm:
        waist_data = {"waist_cm": waist_cm}
        if hip_cm:
            waist_data["hip_cm"] = hip_cm
            waist_data["waist_hip_ratio"] = calculate_waist_hip_ratio(waist_cm, hip_cm)
        waist_data["abdominal_obesity"] = has_abdominal_obesity(gender, waist_cm)
        result["circumferences"] = waist_data

    return result


def analyze_metabolic_profile(
    gender: str,
    age: int,
    height_cm: float,
    weight_kg: float,
    activity_level: str = "moderate",
    body_fat_percentage: Optional[float] = None
) -> Dict[str, Any]:
    """Comprehensive metabolic analysis"""
    # Calculate BMR
    bmr_results = calculate_all_bmr(
        gender, weight_kg, height_cm, age, body_fat_percentage
    )
    primary_bmr = bmr_results["mifflin_st_jeor"]["bmr"]

    # Calculate TDEE
    tdee = calculate_tdee(primary_bmr, activity_level)

    result = {
        "assessment_date": str(date.today()),
        "personal_info": {
            "gender": gender,
            "age": age,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "activity_level": activity_level
        },
        "bmr_calculations": bmr_results,
        "activity_level": {
            "current": activity_level,
            "factor": ACTIVITY_FACTORS[activity_level],
            "description": _get_activity_description(activity_level)
        },
        "tdee": {
            "calories": tdee,
            "calculation": f"BMR_{primary_bmr} × {ACTIVITY_FACTORS[activity_level]}"
        },
        "target_calories": {
            "weight_loss_maintenance": tdee,
            "mild_deficit_250": tdee - 250,
            "moderate_deficit_500": tdee - 500,
            "aggressive_deficit_750": tdee - 750,
            "recommended": tdee - 500
        }
    }

    return result


def _get_activity_description(level: str) -> str:
    """Get activity level description"""
    descriptions = {
        "sedentary": "Sedentary, little or no exercise",
        "light": "Light exercise 1-3 days per week",
        "moderate": "Moderate exercise 3-5 days per week",
        "active": "High-intensity exercise 6-7 days per week",
        "very_active": "Physical labor or daily training"
    }
    return descriptions.get(level, "")


if __name__ == "__main__":
    # Test code
    print("=== Weight Loss Calculation Module Test ===\n")

    # Example: 35-year-old male, 170cm, 75.5kg, 28.5% body fat
    gender, age = "male", 35
    height, weight = 170, 75.5
    body_fat = 28.5

    print("1. Body composition analysis:")
    body_analysis = analyze_body_composition(
        gender, age, height, weight, body_fat, waist_cm=92
    )
    print(json.dumps(body_analysis, indent=2, ensure_ascii=False))

    print("\n2. Metabolic analysis:")
    metabolic = analyze_metabolic_profile(
        gender, age, height, weight, "moderate", body_fat
    )
    print(json.dumps(metabolic, indent=2, ensure_ascii=False))

    print("\n3. Energy deficit analysis:")
    deficit = calculate_deficit(intake_calories=1980, bmr=1650, exercise_burn=400, neat_burn=300)
    print(json.dumps(deficit, indent=2, ensure_ascii=False))
```

---

## Health Report Integration

### Report Section Structure

Add a weight loss section in `generate_health_report.py`:

```python
def generate_weight_loss_section(data: Dict) -> str:
    """Generate weight loss section HTML"""

    html = '''
    <section id="weight-loss" class="mb-8">
        <div class="flex items-center gap-2 mb-4">
            <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
            </svg>
            <h2 class="text-xl font-bold text-gray-800">Scientific Exercise & Health Weight Loss</h2>
        </div>

        <!-- Body composition overview -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="bg-white rounded-lg shadow p-4">
                <div class="text-sm text-gray-500">Weight</div>
                <div class="text-2xl font-bold text-gray-800">75.5 kg</div>
                <div class="text-xs text-emerald-600 mt-1">Target: 68.0 kg</div>
                <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div class="bg-emerald-600 h-2 rounded-full" style="width: 35%"></div>
                </div>
            </div>
            <!-- More cards... -->
        </div>

        <!-- Weight trend chart -->
        <div class="bg-white rounded-lg shadow p-4 mb-6">
            <h3 class="text-lg font-semibold mb-4">Weight Change Trend</h3>
            <canvas id="weightTrendChart" height="200"></canvas>
        </div>

        <!-- Energy deficit chart -->
        <div class="bg-white rounded-lg shadow p-4">
            <h3 class="text-lg font-semibold mb-4">Energy Deficit Tracking</h3>
            <canvas id="deficitChart" height="200"></canvas>
        </div>
    </section>
    '''

    return html
```

### Chart Configuration

Use Chart.js to draw weight loss-related charts:

```javascript
// Weight trend chart
const weightTrendCtx = document.getElementById('weightTrendChart').getContext('2d');
new Chart(weightTrendCtx, {
    type: 'line',
    data: {
        labels: ['Jan 1', 'Jan 8', 'Jan 15'],
        datasets: [{
            label: 'Weight (kg)',
            data: [78.0, 76.5, 75.5],
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        plugins: {
            annotation: {
                annotations: {
                    targetLine: {
                        type: 'line',
                        yMin: 68.0,
                        yMax: 68.0,
                        borderColor: '#f59e0b',
                        borderDash: [5, 5],
                        label: { display: true, content: 'Target' }
                    }
                }
            }
        }
    }
});
```

---

## Error Handling and Safety

### Data Validation Rules

```python
VALID_WEIGHT_RANGE = (30, 300)  # kg
VALID_HEIGHT_RANGE = (100, 250)  # cm
VALID_BODY_FAT_RANGE = (3, 50)   # %
VALID_WAIST_RANGE = (50, 150)    # cm
```

### Safety Boundary Checks

| Check Item | Safety Threshold | Handling |
|-------|---------|---------|
| Minimum calories | BMR × 1.2 | Warn and reject |
| Weight loss rate | ≤1.5 kg/week | Warn |
| Minimum body fat | Male ≥15%, Female ≥20% | Warn |
| Minimum BMI | ≥21 | Warn |

### Medical Disclaimer

Automatically append to every weight loss-related analysis output:

```
⚠️ Disclaimer: The weight loss recommendations provided by this tool are based on
general scientific principles and do not constitute medical diagnosis or prescription.
For extreme weight loss, eating disorders, or obesity-related diseases, please consult a professional physician.
```

---

## Implementation Roadmap

### Phase 0: Framework Setup

| Task | File | Description |
|-----|------|------|
| Extend fitness-tracker.json | `data-example/` | Add weight_loss_program structure |
| Extend nutrition-tracker.json | `data-example/` | Add weight_loss_energy structure |
| Update actual data files | `data/` | Sync user data files |
| Create structure validation test | `scripts/test-weightloss.sh` | Validate data structure integrity |

### Phase 1: Core Calculations

| Task | File | Description |
|-----|------|------|
| Create calculation module | `scripts/weightloss_calculations.py` | BMR/TDEE/body composition calculations |
| Implement BMR calculation | Above file | 3 formulas (Harris-Benedict, Mifflin-St Jeor, Katch-McArdle) |
| Implement body composition analysis | Above file | BMI, body fat assessment, circumference analysis |
| Implement energy deficit calculation | Above file | Intake vs. expenditure, weight loss estimation |
| Extend test script | `scripts/test-weightloss.sh` | Validate calculation accuracy |

### Phase 2: Command Interface

| Task | File | Description |
|-----|------|------|
| Implement fitness commands | `/fitness:weightloss-*` | Body composition, BMR, phase management |
| Implement nutrition commands | `/nutrition:weightloss-*` | Energy deficit, diet records |
| Add data persistence | Module handler functions | Read/write JSON data |
| Implement trend analysis | Calculation module | Historical data analysis and visualization |

### Phase 3: Report Integration

| Task | File | Description |
|-----|------|------|
| Extend report generator | `scripts/generate_health_report.py` | Add weight loss section |
| Create HTML template | Inline in above file | Medical-style layout |
| Integrate Chart.js | Inline in above file | Weight trend, energy deficit charts |
| Implement milestone visualization | Inline in above file | Progress bars, milestone markers |

### Phase 4: Advanced Features (as needed)

| Task | Priority | Description |
|-----|-------|------|
| Plateau detection and recommendations | Medium | Auto-detect and provide breakthrough suggestions |
| Intermittent fasting tracking | Medium | Support for 16:8, 5:2 methods |
| Exercise prescription generation | Low | Personalized FITT principle plans |
| Maintenance phase alert system | Low | Weight rebound reminders |

---

## Appendix

### Reference Standards

- [China Obesity Diagnosis and Treatment Guidelines](https://www.csco.org.cn/)
- [AHA/ACC Guidelines for Management of Obesity in Adults](https://www.heart.org/)
- [ACSM Guidelines for Exercise Testing and Prescription](https://www.acsm.org/)
- [Chinese Dietary Guidelines for Residents](http://www.cnsoc.org/)

### Version History

| Version | Date | Description |
|-----|------|------|
| v1.0 | 2025-01-14 | Initial design document |

---

**Document Maintainer**: WellAlly Tech
**Last Updated**: 2025-01-14
