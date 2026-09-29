from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=20)
    role: str = Field(min_length=1, max_length=20)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: str | None
    role: str
    is_active: bool
    last_login: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        if hasattr(obj, 'role') and hasattr(obj.role, 'name'):
            data = {
                'id': obj.id,
                'username': obj.username,
                'email': obj.email,
                'full_name': obj.full_name,
                'phone': obj.phone,
                'role': obj.role.name,
                'is_active': obj.is_active,
                'last_login': obj.last_login,
                'created_at': obj.created_at,
            }
            return cls(**data)
        return super().model_validate(obj, *args, **kwargs)


class UserDetailResponse(UserResponse):
    student: "StudentNested | None" = None
    staff: "StaffNested | None" = None


class StudentNested(BaseModel):
    id: int
    student_number: str
    department: str | None
    year_of_study: str | None

    model_config = {"from_attributes": True}


class StaffNested(BaseModel):
    id: int
    staff_number: str
    designation: str | None
    department: str | None

    model_config = {"from_attributes": True}
