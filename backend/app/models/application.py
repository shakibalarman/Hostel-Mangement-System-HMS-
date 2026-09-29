from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import AllocationStatus, ApplicationStatus

if TYPE_CHECKING:
    from app.models.hostel import Bed, Hostel, Room
    from app.models.user import Student


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    preferred_hostel_id: Mapped[int | None] = mapped_column(ForeignKey("hostels.id"))
    preferred_room_type: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(
        String(20), default=ApplicationStatus.PENDING.value, nullable=False
    )
    remarks: Mapped[str | None] = mapped_column(Text)
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    student: Mapped["Student"] = relationship(back_populates="applications")
    preferred_hostel: Mapped["Hostel | None"] = relationship()


class RoomAllocation(Base):
    __tablename__ = "room_allocations"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    hostel_id: Mapped[int] = mapped_column(ForeignKey("hostels.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    bed_id: Mapped[int] = mapped_column(ForeignKey("beds.id"), nullable=False)
    application_id: Mapped[int | None] = mapped_column(ForeignKey("applications.id"))
    allocation_date: Mapped[date] = mapped_column(Date, nullable=False)
    check_in_date: Mapped[date | None] = mapped_column(Date)
    check_out_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(
        String(20), default=AllocationStatus.ACTIVE.value, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    student: Mapped["Student"] = relationship(back_populates="allocations")
    hostel: Mapped["Hostel"] = relationship()
    room: Mapped["Room"] = relationship(back_populates="allocations")
    bed: Mapped["Bed"] = relationship(back_populates="allocations")
    application: Mapped["Application | None"] = relationship()
