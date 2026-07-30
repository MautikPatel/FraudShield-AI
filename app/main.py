from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.constants import HEALTH_ENDPOINT, ROOT_ENDPOINT
from app.core.logger import app_logger

from app.core.version import (APP_DESCRIPTION, APP_NAME,VERSION,)
from app.api.transactions import router as transaction_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""

    app_logger.info(
        f"Starting {settings.app_name} v{settings.app_version}"
    )

    yield

    app_logger.info("Application shutdown complete.")


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=VERSION,
    lifespan=lifespan,
)


@app.get(ROOT_ENDPOINT)
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


app.include_router(transaction_router)


@app.get(HEALTH_ENDPOINT)
async def health():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }