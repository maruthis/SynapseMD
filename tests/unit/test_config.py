from synapsemd_platform.core.config import Settings, get_settings


def test_settings_defaults() -> None:
    get_settings.cache_clear()
    settings = Settings()
    assert settings.app_name == "SynapseMD Platform"
    assert settings.phi_block_on_failure is True


def test_get_settings_cached() -> None:
    get_settings.cache_clear()
    a = get_settings()
    b = get_settings()
    assert a is b
