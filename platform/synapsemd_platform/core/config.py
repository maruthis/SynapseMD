from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "SynapseMD Platform"
    app_env: str = "development"
    debug: bool = True
    api_prefix: str = "/api/v1"

    database_url: str = "sqlite+aiosqlite:///./synapsemd.db"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    oidc_issuer: str = ""
    oidc_audience: str = "synapsemd-api"

    vault_url: str = ""
    vault_token: str = ""
    vault_enabled: bool = False

    fhir_base_url: str = "http://localhost:8080/fhir"
    fhir_local_store: str = "./data/fhir"
    fhir_use_hapi: bool = False

    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_audit_topic: str = "synapsemd.audit.events"
    audit_use_memory: bool = True
    audit_use_kafka: bool = False

    llm_default_provider: str = "mock"
    anthropic_api_key: str = ""
    anthropic_base_url: str = "https://api.anthropic.com"
    anthropic_baa_signed: bool = False
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_baa_signed: bool = False
    google_api_key: str = ""
    google_base_url: str = "https://generativelanguage.googleapis.com"
    google_baa_signed: bool = False

    rag_vector_store: str = "memory"  # memory | file
    rag_vector_store_path: str = "./data/rag"
    rag_embedding_model: str = "local-hash"
    org_intelligence_enabled: bool = False

    presidio_enabled: bool = False
    phi_block_on_failure: bool = True

    kms_master_key_id: str = ""
    enable_metrics: bool = True
    enable_tracing: bool = True

    mcp_enabled: bool = True
    legacy_data_root: str = "./data"


@lru_cache
def get_settings() -> Settings:
    return Settings()
