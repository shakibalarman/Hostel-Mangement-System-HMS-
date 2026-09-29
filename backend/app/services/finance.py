from __future__ import annotations

import uuid
from datetime import date

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.finance import Expense, FeeStructure, Payment
from app.models.enums import PaymentStatus
from app.repositories.finance import ExpenseRepository, FeeRepository, PaymentRepository
from app.repositories.hostel import HostelRepository


class FinanceService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.fees = FeeRepository(db)
        self.payments = PaymentRepository(db)
        self.expenses = ExpenseRepository(db)
        self.hostels = HostelRepository(db)

    def create_fee(self, data: dict) -> FeeStructure:
        hostel = self.hostels.get_hostel(data["hostel_id"])
        if not hostel:
            raise NotFoundError("Hostel not found")
        return self.fees.create_fee(**data)

    def get_fee(self, fee_id: int) -> FeeStructure:
        fee = self.fees.get_by_id(fee_id)
        if not fee:
            raise NotFoundError("Fee structure not found")
        return fee

    def list_fees(self, hostel_id: int | None = None, skip: int = 0, limit: int = 100) -> list[FeeStructure]:
        return self.fees.list_fees(hostel_id, skip, limit)

    def update_fee(self, fee_id: int, data: dict) -> FeeStructure:
        fee = self.get_fee(fee_id)
        return self.fees.update_fee(fee, **data)

    def delete_fee(self, fee_id: int) -> None:
        fee = self.get_fee(fee_id)
        self.fees.delete_fee(fee)

    def create_payment(self, data: dict) -> Payment:
        fee = self.fees.get_by_id(data["fee_structure_id"])
        if not fee:
            raise NotFoundError("Fee structure not found")
        data["transaction_id"] = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        if data.get("payment_date"):
            data["status"] = PaymentStatus.PAID.value
        return self.payments.create_payment(**data)

    def get_payment(self, payment_id: int) -> Payment:
        payment = self.payments.get_by_id(payment_id)
        if not payment:
            raise NotFoundError("Payment not found")
        return payment

    def list_payments(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Payment]:
        return self.payments.list_payments(student_id, status, skip, limit)

    def update_payment(self, payment_id: int, data: dict) -> Payment:
        payment = self.get_payment(payment_id)
        return self.payments.update_payment(payment, **data)

    def create_expense(self, data: dict) -> Expense:
        hostel = self.hostels.get_hostel(data["hostel_id"])
        if not hostel:
            raise NotFoundError("Hostel not found")
        return self.expenses.create_expense(**data)

    def get_expense(self, expense_id: int) -> Expense:
        expense = self.expenses.get_by_id(expense_id)
        if not expense:
            raise NotFoundError("Expense not found")
        return expense

    def list_expenses(
        self,
        hostel_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Expense]:
        return self.expenses.list_expenses(hostel_id, skip, limit)

    def update_expense(self, expense_id: int, data: dict) -> Expense:
        expense = self.get_expense(expense_id)
        return self.expenses.update_expense(expense, **data)

    def delete_expense(self, expense_id: int) -> None:
        expense = self.get_expense(expense_id)
        self.expenses.delete_expense(expense)
