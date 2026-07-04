"""Default AI feature configuration (tenant override via Tenant.ai_settings or file)."""

from typing import Any

DEFAULT_AI_CONFIG: dict[str, Any] = {
    "ai_features": {
        "enabled": True,
        "model_version": "v2.0",
        "analysis": {
            "data_integration": True,
            "pattern_recognition": True,
            "anomaly_detection": True,
            "trend_analysis": True,
        },
        "predictions": {
            "enabled": True,
            "supported_risks": [
                "hypertension",
                "diabetes",
                "cardiovascular",
                "nutritional_deficiency",
                "sleep_disorder",
            ],
        },
        "nl_interaction": {"enabled": True},
        "reports": {"enabled": True, "formats": ["html", "json"]},
    }
}

MEDICAL_DISCLAIMER = (
    "This AI analysis is for reference only and does not constitute medical diagnosis. "
    "Please consult a healthcare professional for medical advice."
)
