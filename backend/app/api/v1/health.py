import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    service: str = "integrai-ops-api"


class DBHealthResponse(HealthResponse):
    database: str


@router.get("", response_model=HealthResponse)
async def liveness() -> HealthResponse:
    """Liveness check — confirms the API process is running and able to handle requests."""
    return HealthResponse(status="ok")


@router.get("/db", response_model=DBHealthResponse)
async def readiness(db: AsyncSession = Depends(get_db)) -> DBHealthResponse:
    """Readiness check — confirms the API can reach the database.
    Returns 503 if the database connection fails."""
    try:
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as exc:
        logger.error("Database health check failed", extra={"error": str(exc)})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed.",
        )

    return DBHealthResponse(status="ok", database=db_status)