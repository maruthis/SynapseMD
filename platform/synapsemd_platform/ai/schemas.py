from typing import Any, Literal

from pydantic import BaseModel, Field

RiskLevel = Literal["low", "moderate", "high"]
RiskType = Literal[
    "hypertension",
    "diabetes",
    "cardiovascular",
    "nutritional_deficiency",
    "sleep_disorder",
]

SUPPORTED_RISK_TYPES: list[RiskType] = [
    "hypertension",
    "diabetes",
    "cardiovascular",
    "nutritional_deficiency",
    "sleep_disorder",
]


class RiskRecommendation(BaseModel):
    level: int
    category: str | None = None
    title: str
    content: str
    disclaimer: str | None = None
    requires_medical_supervision: bool = False
    actionable_steps: list[str] = Field(default_factory=list)
    nutrient: str | None = None


class RiskPredictionResult(BaseModel):
    risk_type: str
    risk_name: str
    probability: float
    probability_percent: str
    risk_level: RiskLevel
    risk_level_label: str
    time_horizon_years: int | None = None
    model: str | None = None
    risk_score: int | None = None
    factors: dict[str, Any] = Field(default_factory=dict)
    key_factors: list[dict[str, Any]] = Field(default_factory=list)
    modifiable_factors: list[str] = Field(default_factory=list)
    recommendations: list[dict[str, Any]] = Field(default_factory=list)
    prevention_measures: list[str] = Field(default_factory=list)
    deficiencies: list[dict[str, Any]] = Field(default_factory=list)
    sleep_metrics: dict[str, Any] = Field(default_factory=dict)


class RiskPredictionError(BaseModel):
    error: bool = True
    message: str
