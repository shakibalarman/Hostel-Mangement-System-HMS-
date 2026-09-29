from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceUpdate
from app.services.operations import OperationsService
from app.services.user import UserService

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.get("", response_model=list[AttendanceResponse])
def list_attendance(
    student_id: int | None = None,
    attendance_date: date | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AttendanceResponse]:
    service = OperationsService(db)
    if current_user.role.name == "STUDENT":
        student = UserService(db).get_student_by_user(current_user.id)
        if not student:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Student profile not found")
        student_id = student.id
    return service.list_attendance(student_id, attendance_date, skip, limit)


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AttendanceResponse:
    service = OperationsService(db)
    return service.mark_attendance(payload.model_dump(), current_user.id)


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    payload: AttendanceUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> AttendanceResponse:
    service = OperationsService(db)
    return service.update_attendance(attendance_id, payload.model_dump(exclude_unset=True))
