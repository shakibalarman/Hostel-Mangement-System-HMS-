from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.leave import LeaveCreate, LeaveResponse, LeaveReview
from app.services.operations import OperationsService
from app.services.user import UserService

router = APIRouter(prefix="/leaves", tags=["leaves"])


@router.get("", response_model=list[LeaveResponse])
def list_leaves(
    student_id: int | None = None,
    status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[LeaveResponse]:
    service = OperationsService(db)
    if current_user.role.name == "STUDENT":
        student = UserService(db).get_student_by_user(current_user.id)
        if not student:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Student profile not found")
        student_id = student.id
    return service.list_leaves(student_id, status, skip, limit)


@router.post("", response_model=LeaveResponse, status_code=status.HTTP_201_CREATED)
def create_leave(
    payload: LeaveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LeaveResponse:
    student = UserService(db).get_student_by_user(current_user.id)
    if not student:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Student profile not found")
    service = OperationsService(db)
    return service.create_leave({**payload.model_dump(), "student_id": student.id})


@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> LeaveResponse:
    service = OperationsService(db)
    return service.get_leave(leave_id)


@router.put("/{leave_id}/review", response_model=LeaveResponse)
def review_leave(
    leave_id: int,
    payload: LeaveReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LeaveResponse:
    service = OperationsService(db)
    return service.review_leave(leave_id, current_user.id, payload.status, payload.remarks)
