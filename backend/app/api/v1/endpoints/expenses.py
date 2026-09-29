from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.finance import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.finance import FinanceService

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("", response_model=list[ExpenseResponse])
def list_expenses(
    hostel_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> list[ExpenseResponse]:
    service = FinanceService(db)
    return service.list_expenses(hostel_id, skip, limit)


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> ExpenseResponse:
    service = FinanceService(db)
    return service.create_expense(payload.model_dump())


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> ExpenseResponse:
    service = FinanceService(db)
    return service.get_expense(expense_id)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> ExpenseResponse:
    service = FinanceService(db)
    return service.update_expense(expense_id, payload.model_dump(exclude_unset=True))


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = FinanceService(db)
    service.delete_expense(expense_id)
