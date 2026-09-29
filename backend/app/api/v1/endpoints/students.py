from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.services.user import UserService

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentResponse])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[StudentResponse]:
    service = UserService(db)
    return service.list_students(skip, limit)


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> StudentResponse:
    service = UserService(db)
    return service.create_student(payload.model_dump())


@router.get("/me", response_model=StudentResponse)
def get_my_student_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StudentResponse:
    service = UserService(db)
    student = service.get_student_by_user(current_user.id)
    if not student:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    return student


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> StudentResponse:
    service = UserService(db)
    return service.get_student(student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> StudentResponse:
    service = UserService(db)
    return service.update_student(student_id, payload.model_dump(exclude_unset=True))


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = UserService(db)
    service.delete_student(student_id)
