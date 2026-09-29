from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ComplaintCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)


class ComplaintUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=20)
    resolution_notes: str | None = None


class ComplaintResponse(BaseModel):
    id: int
    student_id: int
    title: str
    description: str
    status: str
    resolved_by: int | None
    resolved_at: datetime | None
    resolution_notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class MaintenanceCreate(BaseModel):
    room_id: int
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)


class MaintenanceUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=20)
    resolution_notes: str | None = None


class MaintenanceResponse(BaseModel):
    id: int
    student_id: int
    room_id: int
    title: str
    description: str
    status: str
    handled_by: int | None
    handled_at: datetime | None
    resolution_notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
