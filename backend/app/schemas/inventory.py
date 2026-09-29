from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class InventoryCreate(BaseModel):
    hostel_id: int
    item_name: str = Field(min_length=1, max_length=200)
    quantity: int = Field(default=0, ge=0)
    unit: str | None = Field(default=None, max_length=30)
    description: str | None = None


class InventoryUpdate(BaseModel):
    item_name: str | None = Field(default=None, max_length=200)
    quantity: int | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, max_length=30)
    description: str | None = None
    status: str | None = Field(default=None, max_length=20)


class InventoryResponse(BaseModel):
    id: int
    hostel_id: int
    item_name: str
    quantity: int
    unit: str | None
    description: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
