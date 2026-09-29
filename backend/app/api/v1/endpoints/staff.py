from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.staff import StaffCreate, StaffResponse, StaffUpdate
from app.services.user import UserService

router = APIRouter(prefix="/staff", tags=["staff"])


@router.get("", response_model=list[StaffResponse])
def list_staff(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> list[StaffResponse]:
    service = UserService(db)
    return service.list_staff(skip, limit)


@router.post("", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(
    payload: StaffCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> StaffResponse:
    service = UserService(db)
    return service.create_staff(payload.model_dump())


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> StaffResponse:
    service = UserService(db)
    return service.get_staff(staff_id)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
    staff_id: int,
    payload: StaffUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> StaffResponse:
    service = UserService(db)
    return service.update_staff(staff_id, payload.model_dump(exclude_unset=True))


@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = UserService(db)
    service.delete_staff(staff_id)
