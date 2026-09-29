from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.allocation import (
    AllocationCheckout,
    AllocationCreate,
    AllocationResponse,
    AllocationTransfer,
)
from app.services.allocation import AllocationService
from app.services.user import UserService

router = APIRouter(prefix="/allocations", tags=["allocations"])


@router.get("", response_model=list[AllocationResponse])
def list_allocations(
    student_id: int | None = None,
    status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AllocationResponse]:
    service = AllocationService(db)
    if current_user.role.name == "STUDENT":
        student = UserService(db).get_student_by_user(current_user.id)
        if not student:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Student profile not found")
        student_id = student.id
    return service.list_allocations(student_id, status, skip, limit)


@router.post("", response_model=AllocationResponse, status_code=status.HTTP_201_CREATED)
def create_allocation(
    payload: AllocationCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> AllocationResponse:
    service = AllocationService(db)
    return service.allocate_bed(payload.model_dump())


@router.get("/{allocation_id}", response_model=AllocationResponse)
def get_allocation(
    allocation_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> AllocationResponse:
    service = AllocationService(db)
    return service.get_allocation(allocation_id)


@router.post("/{allocation_id}/checkout", response_model=AllocationResponse)
def checkout(
    allocation_id: int,
    payload: AllocationCheckout,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> AllocationResponse:
    service = AllocationService(db)
    return service.checkout(allocation_id, payload.check_out_date)


@router.post("/{allocation_id}/transfer", response_model=AllocationResponse)
def transfer(
    allocation_id: int,
    payload: AllocationTransfer,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> AllocationResponse:
    service = AllocationService(db)
    return service.transfer(
        allocation_id,
        payload.new_room_id,
        payload.new_bed_id,
        payload.transfer_date,
        payload.notes,
    )
