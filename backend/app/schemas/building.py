from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class BuildingCreate(BaseModel):
    hostel_id: int
    name: str = Field(min_length=1, max_length=100)
    code: str = Field(min_length=1, max_length=20)
    description: str | None = None


class BuildingUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    description: str | None = None
    status: str | None = Field(default=None, max_length=20)


class BuildingResponse(BaseModel):
    id: int
    hostel_id: int
    name: str
    code: str
    description: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
