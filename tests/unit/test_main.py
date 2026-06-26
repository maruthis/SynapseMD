from unittest.mock import patch

import pytest

from synapsemd_platform import __version__
from synapsemd_platform.api.main import create_app, run


def test_package_version() -> None:
    assert __version__ == "0.1.0"


def test_create_app() -> None:
    app = create_app()
    assert app.title == "SynapseMD Platform"


def test_run_invokes_uvicorn() -> None:
    with patch("uvicorn.run") as mock_run:
        run()
        mock_run.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan_initializes_database() -> None:
    from synapsemd_platform.api.main import create_app, lifespan

    app = create_app()
    async with lifespan(app):
        pass
