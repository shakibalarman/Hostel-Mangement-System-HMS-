from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hostel import Bed, Building, Floor, Hostel, Room


class HostelRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_hostel(self, hostel_id: int) -> Hostel | None:
        return self.db.get(Hostel, hostel_id)

    def get_hostel_by_code(self, code: str) -> Hostel | None:
        return self.db.execute(select(Hostel).where(Hostel.code == code)).scalar_one_or_none()

    def list_hostels(self, skip: int = 0, limit: int = 100) -> list[Hostel]:
        return list(self.db.execute(select(Hostel).offset(skip).limit(limit)).scalars())

    def create_hostel(self, **kwargs) -> Hostel:
        hostel = Hostel(**kwargs)
        self.db.add(hostel)
        self.db.commit()
        self.db.refresh(hostel)
        return hostel

    def update_hostel(self, hostel: Hostel, **kwargs) -> Hostel:
        for key, value in kwargs.items():
            if value is not None:
                setattr(hostel, key, value)
        self.db.commit()
        self.db.refresh(hostel)
        return hostel

    def delete_hostel(self, hostel: Hostel) -> None:
        self.db.delete(hostel)
        self.db.commit()


class BuildingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_building(self, building_id: int) -> Building | None:
        return self.db.get(Building, building_id)

    def list_buildings(self, hostel_id: int | None = None, skip: int = 0, limit: int = 100) -> list[Building]:
        stmt = select(Building)
        if hostel_id:
            stmt = stmt.where(Building.hostel_id == hostel_id)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_building(self, **kwargs) -> Building:
        building = Building(**kwargs)
        self.db.add(building)
        self.db.commit()
        self.db.refresh(building)
        return building

    def update_building(self, building: Building, **kwargs) -> Building:
        for key, value in kwargs.items():
            if value is not None:
                setattr(building, key, value)
        self.db.commit()
        self.db.refresh(building)
        return building

    def delete_building(self, building: Building) -> None:
        self.db.delete(building)
        self.db.commit()


class FloorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_floor(self, floor_id: int) -> Floor | None:
        return self.db.get(Floor, floor_id)

    def list_floors(self, building_id: int | None = None, skip: int = 0, limit: int = 100) -> list[Floor]:
        stmt = select(Floor)
        if building_id:
            stmt = stmt.where(Floor.building_id == building_id)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_floor(self, **kwargs) -> Floor:
        floor = Floor(**kwargs)
        self.db.add(floor)
        self.db.commit()
        self.db.refresh(floor)
        return floor

    def update_floor(self, floor: Floor, **kwargs) -> Floor:
        for key, value in kwargs.items():
            if value is not None:
                setattr(floor, key, value)
        self.db.commit()
        self.db.refresh(floor)
        return floor

    def delete_floor(self, floor: Floor) -> None:
        self.db.delete(floor)
        self.db.commit()


class RoomRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_room(self, room_id: int) -> Room | None:
        return self.db.get(Room, room_id)

    def list_rooms(self, floor_id: int | None = None, status: str | None = None, skip: int = 0, limit: int = 100) -> list[Room]:
        stmt = select(Room)
        if floor_id:
            stmt = stmt.where(Room.floor_id == floor_id)
        if status:
            stmt = stmt.where(Room.status == status)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_room(self, **kwargs) -> Room:
        room = Room(**kwargs)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    def update_room(self, room: Room, **kwargs) -> Room:
        for key, value in kwargs.items():
            if value is not None:
                setattr(room, key, value)
        self.db.commit()
        self.db.refresh(room)
        return room

    def delete_room(self, room: Room) -> None:
        self.db.delete(room)
        self.db.commit()


class BedRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_bed(self, bed_id: int) -> Bed | None:
        return self.db.get(Bed, bed_id)

    def list_beds(self, room_id: int | None = None, status: str | None = None, skip: int = 0, limit: int = 100) -> list[Bed]:
        stmt = select(Bed)
        if room_id:
            stmt = stmt.where(Bed.room_id == room_id)
        if status:
            stmt = stmt.where(Bed.status == status)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_bed(self, **kwargs) -> Bed:
        bed = Bed(**kwargs)
        self.db.add(bed)
        self.db.commit()
        self.db.refresh(bed)
        return bed

    def update_bed(self, bed: Bed, **kwargs) -> Bed:
        for key, value in kwargs.items():
            if value is not None:
                setattr(bed, key, value)
        self.db.commit()
        self.db.refresh(bed)
        return bed

    def delete_bed(self, bed: Bed) -> None:
        self.db.delete(bed)
        self.db.commit()
