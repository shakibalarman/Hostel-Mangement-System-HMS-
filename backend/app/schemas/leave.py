from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field, model_validator


class LeaveCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date")
        return self


class LeaveReview(BaseModel):
    status: str = Field(min_length=1, max_length=20)
    remarks: str | None = None


class LeaveResponse(BaseModel):
    id: int
    student_id: int
    start_date: date
    end_date: date
    reason: str
    status: str
    reviewed_by: int | None
    reviewed_at: datetime | None
    remarks: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
