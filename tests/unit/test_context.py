from uuid import uuid4

import pytest

from synapsemd_platform.core.context import (
    RequestContext,
    clear_request_context,
    get_request_context,
    set_request_context,
)


def test_request_context_lifecycle() -> None:
    ctx = RequestContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=("patient",),
        scopes=("read:own",),
    )
    set_request_context(ctx)
    assert get_request_context() == ctx
    clear_request_context()
    with pytest.raises(RuntimeError, match="not set"):
        get_request_context()
