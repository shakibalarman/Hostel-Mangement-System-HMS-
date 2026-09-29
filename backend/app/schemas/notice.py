from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class NoticeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    audience: str = Field(default="ALL", max_length=20)
    is_active: bool = True


class NoticeUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    content: str | None = None
    audience: str | None = Field(default=None, max_length=20)
    is_active: bool | None = None


class NoticeResponse(BaseModel):
    id: int
    title: str
    content: str
    audience: str
    is_active: bool
    created_by: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
