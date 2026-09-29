from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.finance import Expense, FeeStructure, Payment


class FeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, fee_id: int) -> FeeStructure | None:
        return self.db.get(FeeStructure, fee_id)

    def list_fees(self, hostel_id: int | None = None, skip: int = 0, limit: int = 100) -> list[FeeStructure]:
        stmt = select(FeeStructure)
        if hostel_id:
            stmt = stmt.where(FeeStructure.hostel_id == hostel_id)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_fee(self, **kwargs) -> FeeStructure:
        fee = FeeStructure(**kwargs)
        self.db.add(fee)
        self.db.commit()
        self.db.refresh(fee)
        return fee

    def update_fee(self, fee: FeeStructure, **kwargs) -> FeeStructure:
        for key, value in kwargs.items():
            if value is not None:
                setattr(fee, key, value)
        self.db.commit()
        self.db.refresh(fee)
        return fee

    def delete_fee(self, fee: FeeStructure) -> None:
        self.db.delete(fee)
        self.db.commit()


class PaymentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, payment_id: int) -> Payment | None:
        return self.db.get(Payment, payment_id)

    def list_payments(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Payment]:
        stmt = select(Payment)
        if student_id:
            stmt = stmt.where(Payment.student_id == student_id)
        if status:
            stmt = stmt.where(Payment.status == status)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_payment(self, **kwargs) -> Payment:
        payment = Payment(**kwargs)
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def update_payment(self, payment: Payment, **kwargs) -> Payment:
        for key, value in kwargs.items():
            if value is not None:
                setattr(payment, key, value)
        self.db.commit()
        self.db.refresh(payment)
        return payment


class ExpenseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, expense_id: int) -> Expense | None:
        return self.db.get(Expense, expense_id)

    def list_expenses(
        self,
        hostel_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Expense]:
        stmt = select(Expense)
        if hostel_id:
            stmt = stmt.where(Expense.hostel_id == hostel_id)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_expense(self, **kwargs) -> Expense:
        expense = Expense(**kwargs)
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def update_expense(self, expense: Expense, **kwargs) -> Expense:
        for key, value in kwargs.items():
            if value is not None:
                setattr(expense, key, value)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete_expense(self, expense: Expense) -> None:
        self.db.delete(expense)
        self.db.commit()
