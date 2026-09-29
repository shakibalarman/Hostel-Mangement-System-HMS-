from __future__ import annotations

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.hostel import Bed, Building, Floor, Hostel, Room
from app.repositories.hostel import BedRepository, BuildingRepository, FloorRepository, HostelRepository, RoomRepository


class HostelService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.hostels = HostelRepository(db)
        self.buildings = BuildingRepository(db)
        self.floors = FloorRepository(db)
        self.rooms = RoomRepository(db)
        self.beds = BedRepository(db)

    def create_hostel(self, data: dict) -> Hostel:
        if self.hostels.get_hostel_by_code(data["code"]):
            raise ConflictError("Hostel code already exists")
        return self.hostels.create_hostel(**data)

    def get_hostel(self, hostel_id: int) -> Hostel:
        hostel = self.hostels.get_hostel(hostel_id)
        if not hostel:
            raise NotFoundError("Hostel not found")
        return hostel

    def list_hostels(self, skip: int = 0, limit: int = 100) -> list[Hostel]:
        return self.hostels.list_hostels(skip, limit)

    def update_hostel(self, hostel_id: int, data: dict) -> Hostel:
        hostel = self.get_hostel(hostel_id)
        return self.hostels.update_hostel(hostel, **data)

    def delete_hostel(self, hostel_id: int) -> None:
        hostel = self.get_hostel(hostel_id)
        self.hostels.delete_hostel(hostel)

    def create_building(self, data: dict) -> Building:
        self.get_hostel(data["hostel_id"])
        return self.buildings.create_building(**data)

    def get_building(self, building_id: int) -> Building:
        building = self.buildings.get_building(building_id)
        if not building:
            raise NotFoundError("Building not found")
        return building

    def list_buildings(self, hostel_id: int | None = None, skip: int = 0, limit: int = 100) -> list[Building]:
        return self.buildings.list_buildings(hostel_id, skip, limit)

    def update_building(self, building_id: int, data: dict) -> Building:
        building = self.get_building(building_id)
        return self.buildings.update_building(building, **data)

    def delete_building(self, building_id: int) -> None:
        building = self.get_building(building_id)
        self.buildings.delete_building(building)

    def create_floor(self, data: dict) -> Floor:
        self.get_building(data["building_id"])
        return self.floors.create_floor(**data)

    def get_floor(self, floor_id: int) -> Floor:
        floor = self.floors.get_floor(floor_id)
        if not floor:
            raise NotFoundError("Floor not found")
        return floor

    def list_floors(self, building_id: int | None = None, skip: int = 0, limit: int = 100) -> list[Floor]:
        return self.floors.list_floors(building_id, skip, limit)

    def update_floor(self, floor_id: int, data: dict) -> Floor:
        floor = self.get_floor(floor_id)
        return self.floors.update_floor(floor, **data)

    def delete_floor(self, floor_id: int) -> None:
        floor = self.get_floor(floor_id)
        self.floors.delete_floor(floor)

    def create_room(self, data: dict) -> Room:
        self.get_floor(data["floor_id"])
        return self.rooms.create_room(**data)

    def get_room(self, room_id: int) -> Room:
        room = self.rooms.get_room(room_id)
        if not room:
            raise NotFoundError("Room not found")
        return room

    def list_rooms(self, floor_id: int | None = None, status: str | None = None, skip: int = 0, limit: int = 100) -> list[Room]:
        return self.rooms.list_rooms(floor_id, status, skip, limit)

    def update_room(self, room_id: int, data: dict) -> Room:
        room = self.get_room(room_id)
        return self.rooms.update_room(room, **data)

    def delete_room(self, room_id: int) -> None:
        room = self.get_room(room_id)
        self.rooms.delete_room(room)

    def create_bed(self, data: dict) -> Bed:
        self.get_room(data["room_id"])
        return self.beds.create_bed(**data)

    def get_bed(self, bed_id: int) -> Bed:
        bed = self.beds.get_bed(bed_id)
        if not bed:
            raise NotFoundError("Bed not found")
        return bed

    def list_beds(self, room_id: int | None = None, status: str | None = None, skip: int = 0, limit: int = 100) -> list[Bed]:
        return self.beds.list_beds(room_id, status, skip, limit)

    def update_bed(self, bed_id: int, data: dict) -> Bed:
        bed = self.get_bed(bed_id)
        return self.beds.update_bed(bed, **data)

    def delete_bed(self, bed_id: int) -> None:
        bed = self.get_bed(bed_id)
        self.beds.delete_bed(bed)
