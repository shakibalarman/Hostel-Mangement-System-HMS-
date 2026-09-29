from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class AttendanceCreate(BaseModel):
    student_id: int
    attendance_date: date
    status: str = Field(min_length=1, max_length=20)
    remarks: str | None = Field(default=None, max_length=255)


class AttendanceUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=20)
    remarks: str | None = Field(default=None, max_length=255)


class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    attendance_date: date
    status: str
    remarks: str | None
    marked_by: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
