from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class FeeStructureCreate(BaseModel):
    hostel_id: int
    name: str = Field(min_length=1, max_length=100)
    fee_type: str = Field(min_length=1, max_length=30)
    amount: int = Field(gt=0)
    description: str | None = None


class FeeStructureUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    amount: int | None = Field(default=None, gt=0)
    description: str | None = None
    is_active: bool | None = None


class FeeStructureResponse(BaseModel):
    id: int
    hostel_id: int
    name: str
    fee_type: str
    amount: int
    description: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class PaymentCreate(BaseModel):
    student_id: int
    fee_structure_id: int
    amount: int = Field(gt=0)
    payment_method: str | None = Field(default=None, max_length=30)
    payment_date: date | None = None
    due_date: date | None = None
    remarks: str | None = None


class PaymentUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=20)
    remarks: str | None = None


class PaymentResponse(BaseModel):
    id: int
    student_id: int
    fee_structure_id: int
    amount: int
    status: str
    payment_method: str | None
    transaction_id: str | None
    payment_date: date | None
    due_date: date | None
    remarks: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ExpenseCreate(BaseModel):
    hostel_id: int
    title: str = Field(min_length=1, max_length=200)
    category: str | None = Field(default=None, max_length=50)
    amount: int = Field(gt=0)
    expense_date: date
    description: str | None = None


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    category: str | None = Field(default=None, max_length=50)
    amount: int | None = Field(default=None, gt=0)
    expense_date: date | None = None
    description: str | None = None


class ExpenseResponse(BaseModel):
    id: int
    hostel_id: int
    title: str
    category: str | None
    amount: int
    expense_date: date
    description: str | None
    created_by: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
