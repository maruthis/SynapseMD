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

    fhir_base_url: str = "http://localhost:8080/fhir"
    fhir_local_store: str = "./data/fhir"

    kafka_bootstrap_servers: str = "localhost:9092"
    audit_use_memory: bool = True

    llm_default_provider: str = "mock"
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    rag_vector_store: str = "memory"
    rag_embedding_model: str = "local-hash"

    presidio_enabled: bool = False
    phi_block_on_failure: bool = True

    kms_master_key_id: str = ""
    enable_metrics: bool = True
    enable_tracing: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
