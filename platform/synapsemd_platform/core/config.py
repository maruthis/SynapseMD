from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "SynapseMD Platform"
    app_env: str = "development"
    debug: bool = True
    api_prefix: str = "/api/v1"

    database_url: str = "sqlite+aiosqlite:///./synapsemd.db"
    # json = local IDE/CLI files; postgres = SoR; dual = read postgres then JSON
    health_store: str = "json"
    auto_create_schema: bool = False
    jwt_secret: str = "change-me-in-production"
    jwt_secret_previous: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 15
    jwt_refresh_expire_days: int = 7
    auth_bff_cookies: bool = False

    oidc_issuer: str = ""
    oidc_audience: str = "synapsemd-api"
    oidc_client_id: str = ""
    oidc_client_secret: str = ""
    oidc_redirect_uri: str = "http://localhost:8000/api/v1/auth/oidc/callback"
    cors_origins: str = "*"
    require_mfa_privileged: bool | None = None

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
    audit_legal_hold: bool = False

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

    presidio_enabled: bool | None = None
    phi_block_on_failure: bool = True
    ai_narrative_overlay: bool = False

    kms_master_key_id: str = ""
    enable_metrics: bool = True
    enable_tracing: bool = True

    vllm_base_url: str = "http://localhost:8001/v1"
    vllm_model: str = "local-model"
    vllm_mtls_cert: str = ""
    vllm_mtls_key: str = ""

    mcp_enabled: bool = True
    legacy_data_root: str = "./data"
    object_store_backend: str = "memory"
    object_store_bucket: str = "synapsemd"
    object_store_endpoint: str = ""

    def is_production_like(self) -> bool:
        return self.app_env.lower() in {"staging", "production"}

    def password_login_enabled(self) -> bool:
        return not self.is_production_like()

    def mfa_required_for_privileged(self) -> bool:
        if self.require_mfa_privileged is not None:
            return self.require_mfa_privileged
        return self.app_env.lower() == "production"

    def cors_allow_origins(self) -> list[str]:
        parts = [item.strip() for item in self.cors_origins.split(",") if item.strip()]
        if self.is_production_like():
            return [origin for origin in parts if origin != "*"]
        return parts or ["*"]

    def presidio_is_enabled(self) -> bool:
        if self.presidio_enabled is not None:
            return self.presidio_enabled
        return self.is_production_like()


@lru_cache
def get_settings() -> Settings:
    return Settings()
