"""Evidence-based health risk prediction engine (Module 21)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from synapsemd_platform.ai.schemas import SUPPORTED_RISK_TYPES, RiskType

RISK_LEVEL_LABELS = {
    "low": "Low risk",
    "moderate": "Moderate risk",
    "high": "High risk",
}


class AIPredictionEngine:
    """Predicts health risks using simplified evidence-based scoring models."""

    def __init__(
        self,
        base_dir: str | Path = "data",
        *,
        user_profile: dict[str, Any] | None = None,
        ai_config: dict[str, Any] | None = None,
        nutrition_data: dict[str, Any] | None = None,
        sleep_data: dict[str, Any] | None = None,
        supplemental_data_dir: str | Path | None = None,
    ) -> None:
        self.base_dir = Path(base_dir)
        self.supplemental_data_dir = (
            Path(supplemental_data_dir)
            if supplemental_data_dir is not None
            else self.base_dir.parent / "data-example"
        )
        self.ai_config = ai_config
        self.user_profile = user_profile
        self.nutrition_data = nutrition_data
        self.sleep_data = sleep_data
        if user_profile is None or ai_config is None:
            self.load_config()

    def load_config(self) -> None:
        if self.ai_config is None:
            self.ai_config = self._load_json(self.base_dir / "ai-config.json") or {
                "ai_features": {"predictions": {"enabled": True}}
            }
        if self.user_profile is None:
            self.user_profile = self._load_json(self.base_dir / "profile.json") or {}

    def predict(self, risk_type: str) -> dict[str, Any]:
        if risk_type == "all":
            return {rt: self.predict(rt) for rt in SUPPORTED_RISK_TYPES}
        if risk_type not in SUPPORTED_RISK_TYPES:
            return self._error_result(f"Unknown risk type: {risk_type}")

        predictors = {
            "hypertension": self.predict_hypertension_risk,
            "diabetes": self.predict_diabetes_risk,
            "cardiovascular": self.predict_cardiovascular_risk,
            "nutritional_deficiency": self.predict_nutritional_deficiency_risk,
            "sleep_disorder": self.predict_sleep_disorder_risk,
        }
        return predictors[risk_type]()

    def predict_hypertension_risk(self) -> dict[str, Any]:
        if not self.user_profile:
            return self._error_result("User profile not found")

        factors = {
            "age": self._calculate_age(),
            "bmi": self.user_profile.get("calculated", {}).get("bmi", 0),
            "systolic_bp": self._get_latest_bp("systolic"),
            "diastolic_bp": self._get_latest_bp("diastolic"),
            "family_history": self._check_family_history("hypertension"),
            "smoking": self._check_smoking_status(),
            "activity_level": self.user_profile.get("lifestyle", {}).get("activity_level", "moderate"),
        }

        risk_score = 0
        age = factors["age"]
        if age > 65:
            risk_score += 3
        elif age > 55:
            risk_score += 2
        elif age > 45:
            risk_score += 1

        bmi = factors["bmi"] or 24
        if bmi > 30:
            risk_score += 3
        elif bmi > 25:
            risk_score += 2
        elif bmi > 24:
            risk_score += 1

        sbp = factors["systolic_bp"]
        if sbp and sbp > 140:
            risk_score += 3
        elif sbp and sbp > 130:
            risk_score += 2
        elif sbp and sbp > 120:
            risk_score += 1

        if factors["family_history"]:
            risk_score += 2
        if factors["smoking"]:
            risk_score += 2
        if factors["activity_level"] == "sedentary":
            risk_score += 1

        probability = min(risk_score / 15.0, 0.95)
        risk_level = self._risk_level_from_probability(probability, high=0.3, moderate=0.15)

        return self._build_result(
            risk_type="hypertension",
            risk_name="Hypertension",
            probability=probability,
            risk_level=risk_level,
            model="Framingham Risk Score (simplified)",
            risk_score=risk_score,
            factors=factors,
            modifiable_factors=["bmi", "activity_level", "smoking"],
        )

    def predict_diabetes_risk(self) -> dict[str, Any]:
        if not self.user_profile:
            return self._error_result("User profile not found")

        factors = {
            "age": self._calculate_age(),
            "bmi": self.user_profile.get("calculated", {}).get("bmi", 0),
            "fasting_glucose": self._get_latest_lab_result("fasting_glucose"),
            "family_history": self._check_family_history("diabetes"),
            "activity_level": self.user_profile.get("lifestyle", {}).get("activity_level", "moderate"),
            "diet_quality": self._assess_diet_quality(),
        }

        risk_score = 0
        age = factors["age"]
        if age > 60:
            risk_score += 3
        elif age > 50:
            risk_score += 2
        elif age > 40:
            risk_score += 1

        bmi = factors["bmi"] or 24
        if bmi > 35:
            risk_score += 3
        elif bmi > 30:
            risk_score += 2
        elif bmi > 25:
            risk_score += 1

        glucose = factors["fasting_glucose"]
        if glucose and glucose > 7.0:
            risk_score += 5
        elif glucose and glucose > 5.6:
            risk_score += 3

        if factors["family_history"]:
            risk_score += 2
        if factors["activity_level"] == "sedentary":
            risk_score += 1
        if factors["diet_quality"] == "poor":
            risk_score += 1

        probability = min(risk_score / 18.0, 0.90)
        risk_level = self._risk_level_from_probability(probability, high=0.25, moderate=0.12)

        return self._build_result(
            risk_type="diabetes",
            risk_name="Type 2 diabetes",
            probability=probability,
            risk_level=risk_level,
            model="ADA Diabetes Risk Score",
            risk_score=risk_score,
            factors=factors,
            modifiable_factors=["bmi", "activity_level", "diet_quality"],
        )

    def predict_cardiovascular_risk(self) -> dict[str, Any]:
        if not self.user_profile:
            return self._error_result("User profile not found")

        factors = {
            "age": self._calculate_age(),
            "gender": self.user_profile.get("basic_info", {}).get("gender", "unknown"),
            "systolic_bp": self._get_latest_bp("systolic"),
            "total_cholesterol": self._get_latest_lab_result("total_cholesterol"),
            "hdl_cholesterol": self._get_latest_lab_result("hdl_cholesterol"),
            "smoking": self._check_smoking_status(),
            "diabetes": self._check_medical_history("diabetes"),
        }

        risk_score = 0
        age = factors["age"]
        gender = factors["gender"]

        if gender == "male":
            if age > 65:
                risk_score += 4
            elif age > 55:
                risk_score += 3
            elif age > 45:
                risk_score += 2
            elif age > 35:
                risk_score += 1
        else:
            if age > 65:
                risk_score += 3
            elif age > 55:
                risk_score += 2
            elif age > 45:
                risk_score += 1

        sbp = factors["systolic_bp"]
        if sbp and sbp > 160:
            risk_score += 3
        elif sbp and sbp > 140:
            risk_score += 2
        elif sbp and sbp > 120:
            risk_score += 1

        total_chol = factors["total_cholesterol"]
        if total_chol and total_chol > 240:
            risk_score += 2
        elif total_chol and total_chol > 200:
            risk_score += 1

        if factors["smoking"]:
            risk_score += 2
        if factors["diabetes"]:
            risk_score += 2

        probability = min(risk_score / 14.0, 0.50)
        risk_level = self._risk_level_from_probability(probability, high=0.10, moderate=0.05)

        return self._build_result(
            risk_type="cardiovascular",
            risk_name="Cardiovascular disease",
            probability=probability,
            risk_level=risk_level,
            model="ACC/AHA ASCVD Risk Calculator (simplified)",
            risk_score=risk_score,
            factors=factors,
            modifiable_factors=["systolic_bp", "total_cholesterol", "smoking", "diabetes"],
        )

    def predict_nutritional_deficiency_risk(self) -> dict[str, Any]:
        nutrition_data = self._load_nutrition_data()
        if nutrition_data is None:
            return self._error_result("Nutrition data not found")

        deficiencies: list[dict[str, Any]] = []
        rda_threshold = 0.8

        vitamin_d_avg = self._calculate_average_rda(nutrition_data, "vitamin_d")
        if vitamin_d_avg < rda_threshold:
            deficiencies.append(
                {
                    "nutrient": "Vitamin D",
                    "rda_achievement": f"{round(vitamin_d_avg * 100)}%",
                    "risk_level": "high" if vitamin_d_avg < 0.5 else "moderate",
                }
            )

        calcium_avg = self._calculate_average_rda(nutrition_data, "calcium")
        if calcium_avg < rda_threshold:
            deficiencies.append(
                {
                    "nutrient": "Calcium",
                    "rda_achievement": f"{round(calcium_avg * 100)}%",
                    "risk_level": "high" if calcium_avg < 0.5 else "moderate",
                }
            )

        gender = self.user_profile.get("basic_info", {}).get("gender", "")
        if gender == "female":
            iron_avg = self._calculate_average_rda(nutrition_data, "iron")
            if iron_avg < rda_threshold:
                deficiencies.append(
                    {
                        "nutrient": "Iron",
                        "rda_achievement": f"{round(iron_avg * 100)}%",
                        "risk_level": "high" if iron_avg < 0.5 else "moderate",
                    }
                )

        if len(deficiencies) == 0:
            overall_risk = "low"
            probability = 0.05
        elif len(deficiencies) == 1:
            overall_risk = "moderate"
            probability = 0.20
        else:
            overall_risk = "high"
            probability = 0.40

        return {
            "risk_type": "nutritional_deficiency",
            "risk_name": "Nutritional deficiency",
            "probability": round(probability, 3),
            "probability_percent": f"{round(probability * 100)}%",
            "risk_level": overall_risk,
            "risk_level_label": RISK_LEVEL_LABELS[overall_risk],
            "deficiencies": deficiencies,
            "recommendations": self._generate_nutrition_recommendations(deficiencies),
        }

    def predict_sleep_disorder_risk(self) -> dict[str, Any]:
        sleep_data = self._load_sleep_data()
        if sleep_data is None:
            return self._error_result("Sleep data not found")

        records = sleep_data.get("sleep_records", [])
        if len(records) < 7:
            return self._error_result("Insufficient sleep data (minimum 7 days required)")

        poor_sleep_count = 0
        short_sleep_count = 0
        low_efficiency_count = 0

        for record in records[-7:]:
            quality = record.get("sleep_quality", {}).get("subjective_quality", "good")
            if quality in ["poor", "very poor"]:
                poor_sleep_count += 1

            duration = record.get("sleep_metrics", {}).get("sleep_duration_hours", 0)
            if duration < 6:
                short_sleep_count += 1

            efficiency = record.get("sleep_metrics", {}).get("sleep_efficiency", 100)
            if efficiency < 85:
                low_efficiency_count += 1

        risk_score = 0
        if poor_sleep_count >= 4:
            risk_score += 3
        elif poor_sleep_count >= 2:
            risk_score += 1

        if short_sleep_count >= 5:
            risk_score += 3
        elif short_sleep_count >= 3:
            risk_score += 2

        if low_efficiency_count >= 4:
            risk_score += 2

        probability = min(risk_score / 8.0, 0.60)
        risk_level = self._risk_level_from_probability(probability, high=0.30, moderate=0.15)

        return {
            "risk_type": "sleep_disorder",
            "risk_name": "Sleep disorder",
            "probability": round(probability, 3),
            "probability_percent": f"{round(probability * 100)}%",
            "risk_level": risk_level,
            "risk_level_label": RISK_LEVEL_LABELS[risk_level],
            "sleep_metrics": {
                "poor_sleep_days": poor_sleep_count,
                "short_sleep_days": short_sleep_count,
                "low_efficiency_days": low_efficiency_count,
            },
            "recommendations": self._generate_sleep_recommendations(risk_level),
        }

    def _build_result(
        self,
        *,
        risk_type: RiskType,
        risk_name: str,
        probability: float,
        risk_level: str,
        model: str,
        risk_score: int,
        factors: dict[str, Any],
        modifiable_factors: list[str],
    ) -> dict[str, Any]:
        return {
            "risk_type": risk_type,
            "risk_name": risk_name,
            "probability": round(probability, 3),
            "probability_percent": f"{round(probability * 100)}%",
            "risk_level": risk_level,
            "risk_level_label": RISK_LEVEL_LABELS[risk_level],
            "time_horizon_years": 10,
            "model": model,
            "risk_score": risk_score,
            "factors": factors,
            "key_factors": self._identify_key_factors(factors, risk_score),
            "modifiable_factors": modifiable_factors,
            "recommendations": self._generate_recommendations(risk_type, probability),
            "prevention_measures": self._get_prevention_measures(risk_type),
        }

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def _load_nutrition_data(self) -> dict[str, Any] | None:
        if self.nutrition_data is not None:
            return self.nutrition_data
        path = self.supplemental_data_dir / "nutrition-tracker.json"
        return self._load_json(path)

    def _load_sleep_data(self) -> dict[str, Any] | None:
        if self.sleep_data is not None:
            return self.sleep_data
        path = self.supplemental_data_dir / "sleep-tracker.json"
        return self._load_json(path)

    def _calculate_age(self) -> int:
        birth_date = self.user_profile.get("basic_info", {}).get("birth_date")
        if birth_date:
            try:
                birth = datetime.strptime(birth_date, "%Y-%m-%d")
                today = datetime.now()
                return today.year - birth.year - (
                    (today.month, today.day) < (birth.month, birth.day)
                )
            except ValueError:
                pass
        return 45

    def _get_latest_bp(self, bp_type: str) -> float | None:
        vitals = self.user_profile.get("vitals", {})
        readings = vitals.get("blood_pressure", [])
        if readings:
            latest = readings[-1]
            key = "systolic" if bp_type == "systolic" else "diastolic"
            return latest.get(key)
        return 120 if bp_type == "systolic" else 80

    def _get_latest_lab_result(self, test_name: str) -> float | None:
        labs = self.user_profile.get("lab_results", {})
        if test_name in labs:
            values = labs[test_name]
            if isinstance(values, list) and values:
                return values[-1].get("value")
            if isinstance(values, (int, float)):
                return float(values)
        defaults = {
            "fasting_glucose": 5.4,
            "total_cholesterol": 200,
            "hdl_cholesterol": 50,
        }
        return defaults.get(test_name)

    def _check_family_history(self, condition: str) -> bool:
        return bool(self.user_profile.get("family_history", {}).get(condition, False))

    def _check_smoking_status(self) -> bool:
        return bool(self.user_profile.get("lifestyle", {}).get("smoking", False))

    def _check_medical_history(self, condition: str) -> bool:
        return bool(self.user_profile.get("medical_history", {}).get(condition, False))

    def _assess_diet_quality(self) -> str:
        return self.user_profile.get("lifestyle", {}).get("diet_quality", "moderate")

    def _calculate_average_rda(self, nutrition_data: dict[str, Any], nutrient: str) -> float:
        entries = nutrition_data.get("daily_records", [])
        if not entries:
            return 0.75
        values = [
            entry.get("nutrients", {}).get(nutrient, {}).get("rda_ratio", 0.75)
            for entry in entries
        ]
        return sum(values) / len(values) if values else 0.75

    def _identify_key_factors(self, factors: dict[str, Any], risk_score: int) -> list[dict[str, Any]]:
        key_factors = []
        for factor_name, factor_value in factors.items():
            if factor_value in [True, "high", "poor", "sedentary"] or (
                isinstance(factor_value, (int, float)) and factor_value > 0
            ):
                key_factors.append(
                    {
                        "name": factor_name,
                        "value": factor_value,
                        "contribution": "significant",
                    }
                )
        return key_factors[:5]

    @staticmethod
    def _risk_level_from_probability(
        probability: float, *, high: float, moderate: float
    ) -> str:
        if probability > high:
            return "high"
        if probability > moderate:
            return "moderate"
        return "low"

    def _generate_recommendations(self, risk_type: str, probability: float) -> list[dict[str, Any]]:
        recommendations: list[dict[str, Any]] = []

        if probability > 0.3:
            recommendations.append(
                {
                    "level": 3,
                    "category": "medical_consultation",
                    "title": "Consult a healthcare provider",
                    "content": (
                        f"Based on AI risk prediction, your {risk_type} risk is elevated "
                        f"({round(probability * 100)}%). Please consult a clinician."
                    ),
                    "disclaimer": "For reference only; not a medical diagnosis.",
                    "requires_medical_supervision": True,
                }
            )

        recommendations.append(
            {
                "level": 1,
                "category": "lifestyle",
                "title": "Lifestyle interventions",
                "content": "Healthy lifestyle changes can reduce modifiable risk factors.",
                "actionable_steps": [
                    "Maintain regular physical activity",
                    "Follow a balanced diet",
                    "Manage body weight",
                    "Avoid smoking and limit alcohol",
                ],
            }
        )
        return recommendations

    def _generate_nutrition_recommendations(
        self, deficiencies: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        recommendations = []
        for deficiency in deficiencies:
            nutrient = deficiency["nutrient"]
            recommendations.append(
                {
                    "level": 2,
                    "nutrient": nutrient,
                    "title": f"Increase {nutrient} intake",
                    "content": (
                        f"Your {nutrient} intake may be insufficient "
                        f"(RDA achievement {deficiency['rda_achievement']})."
                    ),
                    "actionable_steps": [
                        f"Add {nutrient}-rich foods to your diet",
                        "Discuss supplements with a clinician if needed",
                        "Recheck nutritional status periodically",
                    ],
                }
            )
        return recommendations

    def _generate_sleep_recommendations(self, risk_level: str) -> list[dict[str, Any]]:
        return [
            {
                "level": 1,
                "title": "Improve sleep hygiene",
                "content": "Establish consistent sleep habits.",
                "actionable_steps": [
                    "Keep a regular sleep schedule",
                    "Limit screens before bedtime",
                    "Optimize bedroom environment",
                    "Avoid caffeine and heavy meals late at night",
                ],
            },
            {
                "level": 2 if risk_level == "high" else 1,
                "title": "Seek help if symptoms persist",
                "content": "Persistent sleep problems may need clinical evaluation.",
                "actionable_steps": [
                    "Track sleep in a diary",
                    "Consult a sleep specialist if needed",
                    "Consider a formal sleep assessment",
                ],
            },
        ]

    def _get_prevention_measures(self, risk_type: str) -> list[str]:
        prevention = {
            "hypertension": [
                "Maintain healthy body weight",
                "Follow DASH-style eating patterns",
                "Limit sodium intake",
                "Exercise regularly",
                "Limit alcohol",
                "Manage stress",
            ],
            "diabetes": [
                "Maintain healthy body weight",
                "Eat a high-fiber, low-sugar diet",
                "Exercise regularly",
                "Monitor blood glucose",
                "Avoid smoking",
            ],
            "cardiovascular": [
                "Control blood pressure, lipids, and glucose",
                "Avoid smoking",
                "Exercise regularly",
                "Follow a heart-healthy diet",
                "Maintain healthy weight",
                "Manage stress",
            ],
        }
        return prevention.get(risk_type, [])

    @staticmethod
    def _error_result(message: str) -> dict[str, Any]:
        return {"error": True, "message": message}


def run_cli_demo() -> None:
    engine = AIPredictionEngine()
    print("AI risk prediction demo")
    print("=" * 50)

    for label, predictor in [
        ("Hypertension", engine.predict_hypertension_risk),
        ("Diabetes", engine.predict_diabetes_risk),
        ("Cardiovascular", engine.predict_cardiovascular_risk),
    ]:
        result = predictor()
        if not result.get("error"):
            print(f"\n{label}: {result['probability_percent']} ({result['risk_level_label']})")
            print(f"Model: {result.get('model')}")


def main() -> None:
    run_cli_demo()
