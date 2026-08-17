from synapsemd_platform.observability.otel import (
    JsonPhiFormatter,
    configure_json_logging,
    get_span_exporter,
    get_tracer,
    setup_tracing,
)


def test_setup_tracing_records_span() -> None:
    exporter = setup_tracing()
    exporter.clear()
    tracer = get_tracer()
    with tracer.start_as_current_span("commands.execute"):
        pass
    names = [span.name for span in get_span_exporter().get_finished_spans()]
    assert "commands.execute" in names


def test_json_phi_formatter_redacts_email() -> None:
    configure_json_logging()
    import logging

    record = logging.LogRecord(
        name="synapsemd",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="email john.doe@example.com",
        args=(),
        exc_info=None,
    )
    record.request_id = "req-1"  # type: ignore[attr-defined]
    formatted = JsonPhiFormatter().format(record)
    assert "john.doe@example.com" not in formatted
    assert '"level": "INFO"' in formatted
    assert "req-1" in formatted


def test_setup_tracing_disabled(monkeypatch) -> None:
    from synapsemd_platform.core.config import get_settings

    monkeypatch.setenv("ENABLE_TRACING", "false")
    get_settings.cache_clear()
    exporter = setup_tracing()
    assert exporter is get_span_exporter()
    get_settings.cache_clear()
