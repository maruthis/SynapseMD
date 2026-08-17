"""OpenTelemetry traces + JSON logs (C-1)."""

from __future__ import annotations

import json
import logging
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from synapsemd_platform.core.config import get_settings
from synapsemd_platform.observability.log_filter import install_phi_log_filter, redact_log_message

_span_exporter = InMemorySpanExporter()
_provider_set = False
_logging_configured = False


class JsonPhiFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = redact_log_message(super().format(record))
        payload: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "msg": message,
        }
        if getattr(record, "request_id", None):
            payload["request_id"] = record.request_id
        return json.dumps(payload, default=str)


def get_span_exporter() -> InMemorySpanExporter:
    return _span_exporter


def setup_tracing() -> InMemorySpanExporter:
    global _provider_set
    settings = get_settings()
    if not settings.enable_tracing:
        return _span_exporter
    if not _provider_set:
        provider = TracerProvider(resource=Resource.create({"service.name": "synapsemd-platform"}))
        provider.add_span_processor(SimpleSpanProcessor(_span_exporter))
        trace.set_tracer_provider(provider)
        _provider_set = True
    return _span_exporter


def configure_json_logging() -> None:
    global _logging_configured
    if _logging_configured:
        return
    install_phi_log_filter()
    handler = logging.StreamHandler()
    handler.setFormatter(JsonPhiFormatter())
    root = logging.getLogger()
    has_json = any(
        isinstance(existing.formatter, JsonPhiFormatter)
        for existing in root.handlers
        if existing.formatter
    )
    if not has_json:
        root.addHandler(handler)
    _logging_configured = True


def get_tracer(name: str = "synapsemd"):
    setup_tracing()
    return trace.get_tracer(name)
