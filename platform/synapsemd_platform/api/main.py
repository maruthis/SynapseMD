from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from synapsemd_platform.api.routes import admin, ai, auth, commands, models, privacy, scim
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.database import init_db
from synapsemd_platform.observability.middleware import CorrelationMiddleware
from synapsemd_platform.observability.otel import configure_json_logging, setup_tracing


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_tracing()
    configure_json_logging()
    await init_db()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    setup_tracing()
    configure_json_logging()
    origins = settings.cors_allow_origins()
    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials="*" not in origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(CorrelationMiddleware)
    app.include_router(admin.router)
    app.include_router(models.router)
    app.include_router(privacy.router)
    app.include_router(auth.router, prefix=settings.api_prefix)
    app.include_router(ai.router, prefix=settings.api_prefix)
    app.include_router(commands.router, prefix=settings.api_prefix)
    app.include_router(scim.router, prefix=settings.api_prefix)
    return app


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run("synapsemd_platform.api.main:app", host="0.0.0.0", port=8000, reload=True)
