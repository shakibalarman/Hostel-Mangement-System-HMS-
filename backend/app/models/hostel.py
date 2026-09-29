from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import BedStatus, HostelStatus, RoomStatus, RoomType

if TYPE_CHECKING:
    from app.models.application import RoomAllocation
    from app.models.complaint import MaintenanceRequest
    from app.models.finance import Expense, FeeStructure
    from app.models.inventory import Inventory
    from app.models.meal import Meal


class Hostel(Base):
    __tablename__ = "hostels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    address: Mapped[str | None] = mapped_column(String(500))
    contact_number: Mapped[str | None] = mapped_column(String(20))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default=HostelStatus.ACTIVE.value, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    buildings: Mapped[List["Building"]] = relationship(back_populates="hostel")
    fee_structures: Mapped[List["FeeStructure"]] = relationship(back_populates="hostel")
    expenses: Mapped[List["Expense"]] = relationship(back_populates="hostel")
    meals: Mapped[List["Meal"]] = relationship(back_populates="hostel")
    inventory_items: Mapped[List["Inventory"]] = relationship(back_populates="hostel")


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostel_id: Mapped[int] = mapped_column(ForeignKey("hostels.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default=HostelStatus.ACTIVE.value, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    hostel: Mapped["Hostel"] = relationship(back_populates="buildings")
    floors: Mapped[List["Floor"]] = relationship(back_populates="building")


class Floor(Base):
    __tablename__ = "floors"

    id: Mapped[int] = mapped_column(primary_key=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    floor_number: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default=HostelStatus.ACTIVE.value, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    building: Mapped["Building"] = relationship(back_populates="floors")
    rooms: Mapped[List["Room"]] = relationship(back_populates="floor")


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    floor_id: Mapped[int] = mapped_column(ForeignKey("floors.id"), nullable=False)
    room_number: Mapped[str] = mapped_column(String(20), nullable=False)
    room_type: Mapped[str] = mapped_column(String(20), default=RoomType.SINGLE.value, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=RoomStatus.AVAILABLE.value, nullable=False)
    rent: Mapped[int | None] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    floor: Mapped["Floor"] = relationship(back_populates="rooms")
    beds: Mapped[List["Bed"]] = relationship(back_populates="room")
    allocations: Mapped[List["RoomAllocation"]] = relationship(back_populates="room")
    maintenance_requests: Mapped[List["MaintenanceRequest"]] = relationship(back_populates="room")


class Bed(Base):
    __tablename__ = "beds"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    bed_number: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=BedStatus.AVAILABLE.value, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    room: Mapped["Room"] = relationship(back_populates="beds")
    allocations: Mapped[List["RoomAllocation"]] = relationship(back_populates="bed")
