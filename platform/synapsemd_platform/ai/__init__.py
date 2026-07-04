"""SynapseMD AI analysis modules (Module 21 platform integration)."""

from synapsemd_platform.ai.config_defaults import DEFAULT_AI_CONFIG, MEDICAL_DISCLAIMER
from synapsemd_platform.ai.config_store import TenantAIConfigStore
from synapsemd_platform.ai.data_adapter import HealthDataContext, TenantHealthDataAdapter, TenantIsolationError
from synapsemd_platform.ai.history import record_ai_interaction
from synapsemd_platform.ai.prediction import AIPredictionEngine, SUPPORTED_RISK_TYPES

__all__ = [
    "AIPredictionEngine",
    "DEFAULT_AI_CONFIG",
    "HealthDataContext",
    "MEDICAL_DISCLAIMER",
    "SUPPORTED_RISK_TYPES",
    "TenantAIConfigStore",
    "TenantHealthDataAdapter",
    "TenantIsolationError",
    "record_ai_interaction",
]
