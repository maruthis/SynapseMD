import pytest

from synapsemd_platform.core.config import Settings, get_settings


def test_settings_defaults() -> None:
    get_settings.cache_clear()
    settings = Settings()
    assert settings.app_name == "SynapseMD Platform"
    assert settings.phi_block_on_failure is True
    assert settings.health_store == "json"
    assert settings.auto_create_schema is False
    assert settings.jwt_expire_minutes == 15
    assert settings.audit_legal_hold is False
    assert settings.password_login_enabled() is True
    assert settings.cors_allow_origins() == ["*"]
    assert settings.presidio_is_enabled() is False
    assert settings.ai_narrative_overlay is False
    assert settings.jwt_secret_previous == ""
    assert settings.object_store_backend == "memory"
    assert settings.object_store_bucket == "synapsemd"
    assert settings.object_store_endpoint == ""


def test_production_cors_strips_wildcard(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("CORS_ORIGINS", "*")
    get_settings.cache_clear()
    settings = Settings()
    assert settings.password_login_enabled() is False
    assert settings.mfa_required_for_privileged() is True
    assert settings.cors_allow_origins() == []
    get_settings.cache_clear()


def test_staging_cors_allowlist(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("CORS_ORIGINS", "https://app.example.com,https://admin.example.com")
    get_settings.cache_clear()
    settings = Settings()
    assert settings.cors_allow_origins() == ["https://app.example.com", "https://admin.example.com"]
    assert settings.password_login_enabled() is False
    get_settings.cache_clear()


def test_presidio_defaults_on_in_staging() -> None:
    settings = Settings(app_env="staging", presidio_enabled=None)
    assert settings.presidio_is_enabled() is True
    prod = Settings(app_env="production", presidio_enabled=None)
    assert prod.presidio_is_enabled() is True


def test_explicit_mfa_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("REQUIRE_MFA_PRIVILEGED", "true")
    get_settings.cache_clear()
    settings = Settings()
    assert settings.mfa_required_for_privileged() is True
    get_settings.cache_clear()


def test_get_settings_cached() -> None:
    get_settings.cache_clear()
    a = get_settings()
    b = get_settings()
    assert a is b
