import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.middleware import CorrelationIDMiddleware

from app.api.v1.health import router as health_router


setup_logging()

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Application factory — builds and configures the FastAPI instance."""
    settings = get_settings()

    app = FastAPI(
        title="IntegrAI Ops API",
        description="AI-powered integration monitoring and incident resolution platform.",
        version="0.1.0",
        docs_url="/api/v1/docs",
        openapi_url="/api/v1/openapi.json",
    )

    app.add_middleware(CorrelationIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(health_router, prefix="/api/v1")



    logger.info("IntegrAI Ops API starting", extra={"environment": settings.APP_ENV})

    return app


app = create_app()