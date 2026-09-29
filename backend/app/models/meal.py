from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import MealType

if TYPE_CHECKING:
    from app.models.hostel import Hostel
    from app.models.user import Student


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostel_id: Mapped[int] = mapped_column(ForeignKey("hostels.id"), nullable=False)
    meal_type: Mapped[str] = mapped_column(String(20), nullable=False)
    menu: Mapped[str] = mapped_column(Text, nullable=False)
    meal_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    hostel: Mapped["Hostel"] = relationship(back_populates="meals")
    allocations: Mapped[List["MealAllocation"]] = relationship(back_populates="meal")


class MealAllocation(Base):
    __tablename__ = "meal_allocations"

    id: Mapped[int] = mapped_column(primary_key=True)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    allocated_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    meal: Mapped["Meal"] = relationship(back_populates="allocations")
    student: Mapped["Student"] = relationship(back_populates="meal_allocations")
