from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class MealCreate(BaseModel):
    hostel_id: int
    meal_type: str = Field(min_length=1, max_length=20)
    menu: str = Field(min_length=1)
    meal_date: date


class MealUpdate(BaseModel):
    menu: str | None = None
    is_active: bool | None = None


class MealResponse(BaseModel):
    id: int
    hostel_id: int
    meal_type: str
    menu: str
    meal_date: date
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
