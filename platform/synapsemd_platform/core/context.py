from contextvars import ContextVar
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RequestContext:
    user_id: UUID
    tenant_id: UUID
    roles: tuple[str, ...]
    scopes: tuple[str, ...]


_request_context: ContextVar[RequestContext | None] = ContextVar("request_context", default=None)


def set_request_context(ctx: RequestContext) -> None:
    _request_context.set(ctx)


def get_request_context() -> RequestContext:
    ctx = _request_context.get()
    if ctx is None:
        raise RuntimeError("Request context is not set")
    return ctx


def clear_request_context() -> None:
    _request_context.set(None)
