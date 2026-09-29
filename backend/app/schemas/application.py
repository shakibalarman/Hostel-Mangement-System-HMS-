from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    preferred_hostel_id: int | None = None
    preferred_room_type: str | None = Field(default=None, max_length=20)


class ApplicationUpdate(BaseModel):
    preferred_hostel_id: int | None = None
    preferred_room_type: str | None = Field(default=None, max_length=20)


class ApplicationReview(BaseModel):
    status: str = Field(min_length=1, max_length=20)
    remarks: str | None = None


class ApplicationResponse(BaseModel):
    id: int
    student_id: int
    preferred_hostel_id: int | None
    preferred_room_type: str | None
    status: str
    remarks: str | None
    reviewed_by: int | None
    reviewed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
