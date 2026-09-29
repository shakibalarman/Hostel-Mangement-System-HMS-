from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class BedCreate(BaseModel):
    room_id: int
    bed_number: str = Field(min_length=1, max_length=20)
    description: str | None = None


class BedUpdate(BaseModel):
    bed_number: str | None = Field(default=None, max_length=20)
    description: str | None = None
    status: str | None = Field(default=None, max_length=20)


class BedResponse(BaseModel):
    id: int
    room_id: int
    bed_number: str
    status: str
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
