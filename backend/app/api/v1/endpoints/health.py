from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter(prefix="/health", tags=["health"])

logging.basicConfig(level=logging.INFO)


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    database: str = Field(examples=["up"])
    version: str = Field(examples=["1.0.0"])


@router.get("", response_model=HealthResponse, summary="Service health check")
def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    try:
        db.execute(text("SELECT 1"))
        database = "up"
    except Exception:  # noqa: BLE001
        database = "down"
    return HealthResponse(
        status="ok" if database == "up" else "degraded",
        database=database,
        version="1.0.0",
    )
