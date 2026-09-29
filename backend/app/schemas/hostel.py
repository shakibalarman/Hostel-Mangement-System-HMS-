from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class HostelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    code: str = Field(min_length=1, max_length=20)
    address: str | None = Field(default=None, max_length=500)
    contact_number: str | None = Field(default=None, max_length=20)
    description: str | None = None


class HostelUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    address: str | None = Field(default=None, max_length=500)
    contact_number: str | None = Field(default=None, max_length=20)
    description: str | None = None
    status: str | None = Field(default=None, max_length=20)


class HostelResponse(BaseModel):
    id: int
    name: str
    code: str
    address: str | None
    contact_number: str | None
    description: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
