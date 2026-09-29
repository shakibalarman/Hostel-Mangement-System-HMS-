from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class MealTrackingCreate(BaseModel):
    meal_date: date
    meal_type: str = Field(min_length=1, max_length=20)
    quantity: int = Field(default=1, ge=1, le=10)
    cost_per_meal: int = Field(default=0, ge=0)
    notes: str | None = Field(default=None, max_length=255)


class MealTrackingUpdate(BaseModel):
    meal_type: str | None = Field(default=None, min_length=1, max_length=20)
    quantity: int | None = Field(default=None, ge=1, le=10)
    cost_per_meal: int | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=255)


class MealTrackingResponse(BaseModel):
    id: int
    student_id: int
    meal_date: date
    meal_type: str
    quantity: int
    cost_per_meal: int
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class MealBalanceResponse(BaseModel):
    id: int
    student_id: int
    total_meals_purchased: int
    meals_consumed: int
    balance: int
    last_updated: datetime

    model_config = {"from_attributes": True}


class MealStatsResponse(BaseModel):
    current_month_meals: int
    last_month_meals: int
    total_meals: int
    balance: int
    total_spent: int
    daily_average: float
