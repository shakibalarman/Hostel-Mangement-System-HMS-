from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class FloorCreate(BaseModel):
    building_id: int
    name: str = Field(min_length=1, max_length=50)
    floor_number: int
    description: str | None = None


class FloorUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=50)
    floor_number: int | None = None
    description: str | None = None
    status: str | None = Field(default=None, max_length=20)


class FloorResponse(BaseModel):
    id: int
    building_id: int
    name: str
    floor_number: int
    description: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
