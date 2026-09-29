from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    floor_id: int
    room_number: str = Field(min_length=1, max_length=20)
    room_type: str = Field(default="SINGLE", max_length=20)
    capacity: int = Field(default=1, ge=1, le=10)
    rent: int | None = Field(default=None, ge=0)
    description: str | None = None


class RoomUpdate(BaseModel):
    room_number: str | None = Field(default=None, max_length=20)
    room_type: str | None = Field(default=None, max_length=20)
    capacity: int | None = Field(default=None, ge=1, le=10)
    rent: int | None = Field(default=None, ge=0)
    description: str | None = None
    status: str | None = Field(default=None, max_length=20)


class RoomResponse(BaseModel):
    id: int
    floor_id: int
    room_number: str
    room_type: str
    capacity: int
    status: str
    rent: int | None
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
