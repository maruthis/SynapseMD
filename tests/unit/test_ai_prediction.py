from datetime import datetime, timedelta

import pytest

from synapsemd_platform.ai.prediction import AIPredictionEngine
from synapsemd_platform.ai.schemas import SUPPORTED_RISK_TYPES


@pytest.fixture
def low_risk_profile() -> dict:
    birth = (datetime.now() - timedelta(days=365 * 30)).strftime("%Y-%m-%d")
    return {
        "basic_info": {"birth_date": birth, "gender": "female"},
        "calculated": {"bmi": 22},
        "lifestyle": {"activity_level": "moderate", "smoking": False, "diet_quality": "good"},
        "family_history": {},
        "medical_history": {},
        "vitals": {"blood_pressure": [{"systolic": 115, "diastolic": 75}]},
        "lab_results": {
            "fasting_glucose": [{"value": 5.0}],
            "total_cholesterol": [{"value": 180}],
            "hdl_cholesterol": [{"value": 60}],
        },
    }


@pytest.fixture
def high_risk_profile() -> dict:
    birth = (datetime.now() - timedelta(days=365 * 70)).strftime("%Y-%m-%d")
    return {
        "basic_info": {"birth_date": birth, "gender": "male"},
        "calculated": {"bmi": 32},
        "lifestyle": {"activity_level": "sedentary", "smoking": True, "diet_quality": "poor"},
        "family_history": {"hypertension": True, "diabetes": True},
        "medical_history": {"diabetes": True},
        "vitals": {"blood_pressure": [{"systolic": 150, "diastolic": 95}]},
        "lab_results": {
            "fasting_glucose": [{"value": 7.5}],
            "total_cholesterol": [{"value": 260}],
            "hdl_cholesterol": [{"value": 40}],
        },
    }


@pytest.fixture
def nutrition_data_low() -> dict:
    return {
        "daily_records": [
            {
                "nutrients": {
                    "vitamin_d": {"rda_ratio": 0.9},
                    "calcium": {"rda_ratio": 0.85},
                    "iron": {"rda_ratio": 0.9},
                }
            }
        ]
    }


@pytest.fixture
def nutrition_data_deficient() -> dict:
    return {
        "daily_records": [
            {
                "nutrients": {
                    "vitamin_d": {"rda_ratio": 0.4},
                    "calcium": {"rda_ratio": 0.3},
                    "iron": {"rda_ratio": 0.45},
                }
            }
        ]
    }


@pytest.fixture
def sleep_data_good() -> dict:
    records = []
    for _ in range(7):
        records.append(
            {
                "sleep_quality": {"subjective_quality": "good"},
                "sleep_metrics": {"sleep_duration_hours": 7.5, "sleep_efficiency": 90},
            }
        )
    return {"sleep_records": records}


@pytest.fixture
def sleep_data_poor() -> dict:
    records = []
    for _ in range(7):
        records.append(
            {
                "sleep_quality": {"subjective_quality": "poor"},
                "sleep_metrics": {"sleep_duration_hours": 5.0, "sleep_efficiency": 70},
            }
        )
    return {"sleep_records": records}


def test_supported_risk_types() -> None:
    assert len(SUPPORTED_RISK_TYPES) == 5
    assert "hypertension" in SUPPORTED_RISK_TYPES


def test_hypertension_low_risk(low_risk_profile: dict) -> None:
    engine = AIPredictionEngine(user_profile=low_risk_profile, ai_config={})
    result = engine.predict_hypertension_risk()
    assert result["risk_type"] == "hypertension"
    assert result["risk_level"] == "low"
    assert result["probability"] < 0.15
    assert result["model"]


def test_hypertension_high_risk(high_risk_profile: dict) -> None:
    engine = AIPredictionEngine(user_profile=high_risk_profile, ai_config={})
    result = engine.predict_hypertension_risk()
    assert result["risk_level"] in {"moderate", "high"}
    assert result["probability"] > 0.15
    assert any(r["level"] == 3 for r in result["recommendations"])


def test_diabetes_risk(high_risk_profile: dict) -> None:
    engine = AIPredictionEngine(user_profile=high_risk_profile, ai_config={})
    result = engine.predict_diabetes_risk()
    assert result["risk_type"] == "diabetes"
    assert result["risk_level"] in {"moderate", "high"}


def test_cardiovascular_risk_male(high_risk_profile: dict) -> None:
    engine = AIPredictionEngine(user_profile=high_risk_profile, ai_config={})
    result = engine.predict_cardiovascular_risk()
    assert result["risk_type"] == "cardiovascular"
    assert result["probability"] <= 0.50


def test_cardiovascular_risk_female(low_risk_profile: dict) -> None:
    engine = AIPredictionEngine(user_profile=low_risk_profile, ai_config={})
    result = engine.predict_cardiovascular_risk()
    assert result["risk_level"] == "low"


def test_nutritional_deficiency_low(
    low_risk_profile: dict, nutrition_data_low: dict
) -> None:
    engine = AIPredictionEngine(
        user_profile=low_risk_profile,
        ai_config={},
        nutrition_data=nutrition_data_low,
    )
    result = engine.predict_nutritional_deficiency_risk()
    assert result["risk_level"] == "low"
    assert result["deficiencies"] == []


def test_nutritional_deficiency_high_female(
    low_risk_profile: dict, nutrition_data_deficient: dict
) -> None:
    engine = AIPredictionEngine(
        user_profile=low_risk_profile,
        ai_config={},
        nutrition_data=nutrition_data_deficient,
    )
    result = engine.predict_nutritional_deficiency_risk()
    assert result["risk_level"] in {"moderate", "high"}
    assert len(result["deficiencies"]) >= 2


def test_sleep_disorder_low(low_risk_profile: dict, sleep_data_good: dict) -> None:
    engine = AIPredictionEngine(
        user_profile=low_risk_profile,
        ai_config={},
        sleep_data=sleep_data_good,
    )
    result = engine.predict_sleep_disorder_risk()
    assert result["risk_level"] == "low"


def test_sleep_disorder_high(low_risk_profile: dict, sleep_data_poor: dict) -> None:
    engine = AIPredictionEngine(
        user_profile=low_risk_profile,
        ai_config={},
        sleep_data=sleep_data_poor,
    )
    result = engine.predict_sleep_disorder_risk()
    assert result["risk_level"] in {"moderate", "high"}
    assert result["sleep_metrics"]["poor_sleep_days"] >= 4


def test_sleep_insufficient_data(low_risk_profile: dict) -> None:
    engine = AIPredictionEngine(
        user_profile=low_risk_profile,
        ai_config={},
        sleep_data={"sleep_records": [{"sleep_metrics": {}}]},
    )
    result = engine.predict_sleep_disorder_risk()
    assert result["error"] is True


def test_missing_profile_returns_error() -> None:
    engine = AIPredictionEngine(user_profile={}, ai_config={})
    engine.user_profile = None
    result = engine.predict_hypertension_risk()
    assert result["error"] is True


def test_predict_dispatch_all(low_risk_profile: dict, sleep_data_good: dict) -> None:
    engine = AIPredictionEngine(
        user_profile=low_risk_profile,
        ai_config={},
        sleep_data=sleep_data_good,
        nutrition_data={"daily_records": [{"nutrients": {"vitamin_d": {"rda_ratio": 0.9}}}]},
    )
    results = engine.predict("all")
    assert set(results.keys()) == set(SUPPORTED_RISK_TYPES)


def test_predict_unknown_type(low_risk_profile: dict) -> None:
    engine = AIPredictionEngine(user_profile=low_risk_profile, ai_config={})
    result = engine.predict("unknown")
    assert result["error"] is True


def test_load_config_from_files(tmp_path) -> None:
    profile = {"basic_info": {"birth_date": "1990-01-01"}, "calculated": {"bmi": 23}}
    (tmp_path / "profile.json").write_text(
        __import__("json").dumps(profile), encoding="utf-8"
    )
    (tmp_path / "ai-config.json").write_text(
        __import__("json").dumps({"ai_features": {"predictions": {"enabled": True}}}),
        encoding="utf-8",
    )
    engine = AIPredictionEngine(base_dir=tmp_path)
    assert engine.user_profile == profile
    result = engine.predict_hypertension_risk()
    assert "risk_type" in result


def test_nutrition_data_missing_file(low_risk_profile: dict, tmp_path) -> None:
    engine = AIPredictionEngine(
        user_profile=low_risk_profile,
        ai_config={},
        supplemental_data_dir=tmp_path,
    )
    result = engine.predict_nutritional_deficiency_risk()
    assert result["error"] is True


def test_hypertension_moderate_branches() -> None:
    birth = (datetime.now() - timedelta(days=365 * 50)).strftime("%Y-%m-%d")
    profile = {
        "basic_info": {"birth_date": birth, "gender": "male"},
        "calculated": {"bmi": 26},
        "lifestyle": {"activity_level": "sedentary", "smoking": False},
        "family_history": {"hypertension": True},
        "vitals": {"blood_pressure": [{"systolic": 125, "diastolic": 82}]},
    }
    engine = AIPredictionEngine(user_profile=profile, ai_config={})
    result = engine.predict_hypertension_risk()
    assert result["risk_level"] in {"moderate", "high", "low"}


def test_diabetes_glucose_branches() -> None:
    birth = (datetime.now() - timedelta(days=365 * 45)).strftime("%Y-%m-%d")
    profile = {
        "basic_info": {"birth_date": birth},
        "calculated": {"bmi": 28},
        "lifestyle": {"activity_level": "sedentary", "diet_quality": "poor"},
        "family_history": {"diabetes": True},
        "lab_results": {"fasting_glucose": [{"value": 6.0}]},
    }
    engine = AIPredictionEngine(user_profile=profile, ai_config={})
    result = engine.predict_diabetes_risk()
    assert result["risk_score"] >= 3


def test_cardiovascular_female_age_branches() -> None:
    birth = (datetime.now() - timedelta(days=365 * 60)).strftime("%Y-%m-%d")
    profile = {
        "basic_info": {"birth_date": birth, "gender": "female"},
        "calculated": {"bmi": 24},
        "lifestyle": {"smoking": True},
        "medical_history": {"diabetes": True},
        "vitals": {"blood_pressure": [{"systolic": 145, "diastolic": 90}]},
        "lab_results": {"total_cholesterol": 210, "hdl_cholesterol": 45},
    }
    engine = AIPredictionEngine(user_profile=profile, ai_config={})
    result = engine.predict_cardiovascular_risk()
    assert result["probability"] > 0


def test_calculate_age_invalid_birth_date() -> None:
    engine = AIPredictionEngine(
        user_profile={"basic_info": {"birth_date": "invalid-date"}},
        ai_config={},
    )
    assert engine._calculate_age() == 45


def test_lab_results_scalar_values() -> None:
    profile = {
        "basic_info": {"birth_date": "1980-01-01"},
        "calculated": {"bmi": 24},
        "lab_results": {
            "fasting_glucose": 5.2,
            "total_cholesterol": 190,
            "hdl_cholesterol": 55,
        },
    }
    engine = AIPredictionEngine(user_profile=profile, ai_config={})
    assert engine._get_latest_lab_result("fasting_glucose") == 5.2


def test_run_cli_demo(capsys) -> None:
    from synapsemd_platform.ai.prediction import run_cli_demo

    run_cli_demo()
    captured = capsys.readouterr()
    assert "AI risk prediction demo" in captured.out

