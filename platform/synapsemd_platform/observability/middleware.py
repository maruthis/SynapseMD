"""Request correlation headers (C-2)."""

from __future__ import annotations

from uuid import uuid4

from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("x-request-id") or uuid4().hex
        span = trace.get_current_span()
        context = span.get_span_context() if span is not None else None
        if context is not None and context.trace_id:
            trace_id = format(context.trace_id, "032x")
        else:
            trace_id = request_id
        request.state.request_id = request_id
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id
        return response
