from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationReview
from app.services.allocation import AllocationService
from app.services.user import UserService

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", response_model=list[ApplicationResponse])
def list_applications(
    student_id: int | None = None,
    status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ApplicationResponse]:
    service = AllocationService(db)
    if current_user.role.name == "STUDENT":
        student = UserService(db).get_student_by_user(current_user.id)
        if not student:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Student profile not found")
        student_id = student.id
    return service.list_applications(student_id, status, skip, limit)


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApplicationResponse:
    student = UserService(db).get_student_by_user(current_user.id)
    if not student:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Student profile not found")
    service = AllocationService(db)
    return service.create_application(student.id, payload.model_dump(exclude_unset=True))


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> ApplicationResponse:
    service = AllocationService(db)
    return service.get_application(application_id)


@router.put("/{application_id}/review", response_model=ApplicationResponse)
def review_application(
    application_id: int,
    payload: ApplicationReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApplicationResponse:
    service = AllocationService(db)
    return service.review_application(
        application_id, current_user.id, payload.status, payload.remarks
    )
