from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.finance import FeeStructureCreate, FeeStructureResponse, FeeStructureUpdate
from app.services.finance import FinanceService

router = APIRouter(prefix="/fees", tags=["fees"])


@router.get("", response_model=list[FeeStructureResponse])
def list_fees(
    hostel_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[FeeStructureResponse]:
    service = FinanceService(db)
    return service.list_fees(hostel_id, skip, limit)


@router.post("", response_model=FeeStructureResponse, status_code=status.HTTP_201_CREATED)
def create_fee(
    payload: FeeStructureCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> FeeStructureResponse:
    service = FinanceService(db)
    return service.create_fee(payload.model_dump())


@router.get("/{fee_id}", response_model=FeeStructureResponse)
def get_fee(
    fee_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> FeeStructureResponse:
    service = FinanceService(db)
    return service.get_fee(fee_id)


@router.put("/{fee_id}", response_model=FeeStructureResponse)
def update_fee(
    fee_id: int,
    payload: FeeStructureUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> FeeStructureResponse:
    service = FinanceService(db)
    return service.update_fee(fee_id, payload.model_dump(exclude_unset=True))


@router.delete("/{fee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fee(
    fee_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = FinanceService(db)
    service.delete_fee(fee_id)
