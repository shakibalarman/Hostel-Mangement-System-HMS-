from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.complaint import ComplaintCreate, ComplaintResponse, ComplaintUpdate
from app.services.operations import OperationsService
from app.services.user import UserService

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.get("", response_model=list[ComplaintResponse])
def list_complaints(
    student_id: int | None = None,
    status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ComplaintResponse]:
    service = OperationsService(db)
    if current_user.role.name == "STUDENT":
        student = UserService(db).get_student_by_user(current_user.id)
        if not student:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Student profile not found")
        student_id = student.id
    return service.list_complaints(student_id, status, skip, limit)


@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(
    payload: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ComplaintResponse:
    student = UserService(db).get_student_by_user(current_user.id)
    if not student:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Student profile not found")
    service = OperationsService(db)
    return service.create_complaint({**payload.model_dump(), "student_id": student.id})


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> ComplaintResponse:
    service = OperationsService(db)
    return service.get_complaint(complaint_id)


@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: int,
    payload: ComplaintUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ComplaintResponse:
    service = OperationsService(db)
    return service.update_complaint(
        complaint_id,
        status=payload.status,
        resolution_notes=payload.resolution_notes,
        resolved_by=current_user.id,
    )
