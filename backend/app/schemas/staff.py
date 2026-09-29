from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class StaffCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=20)
    staff_number: str = Field(min_length=1, max_length=30)
    designation: str | None = Field(default=None, max_length=100)
    department: str | None = Field(default=None, max_length=100)
    hire_date: date | None = None


class StaffUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    designation: str | None = Field(default=None, max_length=100)
    department: str | None = Field(default=None, max_length=100)
    hire_date: date | None = None


class StaffResponse(BaseModel):
    id: int
    user_id: int
    staff_number: str
    designation: str | None
    department: str | None
    hire_date: date | None
    created_at: datetime

    model_config = {"from_attributes": True}


class StaffDetailResponse(StaffResponse):
    user: "UserNested | None" = None


class UserNested(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: str | None
    is_active: bool

    model_config = {"from_attributes": True}
