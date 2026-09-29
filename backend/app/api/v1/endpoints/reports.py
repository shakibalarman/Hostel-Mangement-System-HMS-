from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.report import DashboardStats
from app.services.report import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> DashboardStats:
    service = ReportService(db)
    return service.get_dashboard_stats()


@router.get("/occupancy")
def get_occupancy_report(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[dict]:
    service = ReportService(db)
    return service.get_occupancy_report()


@router.get("/students")
def get_student_report(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[dict]:
    service = ReportService(db)
    return service.get_student_report()


@router.get("/payments")
def get_payment_report(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[dict]:
    service = ReportService(db)
    return service.get_payment_report()


@router.get("/outstanding-fees")
def get_outstanding_fees_report(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[dict]:
    service = ReportService(db)
    return service.get_outstanding_fees_report()
