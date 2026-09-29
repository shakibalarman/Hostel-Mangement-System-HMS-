from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=20)
    student_number: str = Field(min_length=1, max_length=30)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=10)
    address: str | None = Field(default=None, max_length=500)
    emergency_contact: str | None = Field(default=None, max_length=100)
    department: str | None = Field(default=None, max_length=100)
    year_of_study: str | None = Field(default=None, max_length=20)


class StudentUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=10)
    address: str | None = Field(default=None, max_length=500)
    emergency_contact: str | None = Field(default=None, max_length=100)
    department: str | None = Field(default=None, max_length=100)
    year_of_study: str | None = Field(default=None, max_length=20)


class StudentResponse(BaseModel):
    id: int
    user_id: int
    student_number: str
    date_of_birth: date | None
    gender: str | None
    address: str | None
    emergency_contact: str | None
    department: str | None
    year_of_study: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class StudentDetailResponse(StudentResponse):
    user: "UserNested | None" = None


class UserNested(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: str | None
    is_active: bool

    model_config = {"from_attributes": True}
