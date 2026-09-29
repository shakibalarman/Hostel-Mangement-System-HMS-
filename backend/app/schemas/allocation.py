from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field, model_validator


class AllocationCreate(BaseModel):
    student_id: int
    hostel_id: int
    room_id: int
    bed_id: int
    application_id: int | None = None
    allocation_date: date
    check_in_date: date | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_in_date and self.check_in_date < self.allocation_date:
            raise ValueError("Check-in date cannot be before allocation date")
        return self


class AllocationUpdate(BaseModel):
    notes: str | None = None
    status: str | None = Field(default=None, max_length=20)


class AllocationCheckout(BaseModel):
    check_out_date: date


class AllocationTransfer(BaseModel):
    new_room_id: int
    new_bed_id: int
    transfer_date: date
    notes: str | None = None


class AllocationResponse(BaseModel):
    id: int
    student_id: int
    hostel_id: int
    room_id: int
    bed_id: int
    application_id: int | None
    allocation_date: date
    check_in_date: date | None
    check_out_date: date | None
    status: str
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
