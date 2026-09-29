from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.finance import PaymentCreate, PaymentResponse, PaymentUpdate
from app.services.finance import FinanceService
from app.services.user import UserService

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("", response_model=list[PaymentResponse])
def list_payments(
    student_id: int | None = None,
    status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PaymentResponse]:
    service = FinanceService(db)
    if current_user.role.name == "STUDENT":
        student = UserService(db).get_student_by_user(current_user.id)
        if not student:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Student profile not found")
        student_id = student.id
    return service.list_payments(student_id, status, skip, limit)


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> PaymentResponse:
    service = FinanceService(db)
    return service.create_payment(payload.model_dump())


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> PaymentResponse:
    service = FinanceService(db)
    return service.get_payment(payment_id)


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payload: PaymentUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> PaymentResponse:
    service = FinanceService(db)
    return service.update_payment(payment_id, payload.model_dump(exclude_unset=True))
