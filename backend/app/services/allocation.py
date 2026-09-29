from __future__ import annotations

from datetime import date

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, UnprocessableEntityError
from app.models.application import Application, RoomAllocation
from app.models.enums import AllocationStatus, ApplicationStatus, BedStatus
from app.models.hostel import Bed, Hostel, Room
from app.repositories.application import AllocationRepository, ApplicationRepository
from app.repositories.hostel import BedRepository, HostelRepository, RoomRepository


class AllocationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.applications = ApplicationRepository(db)
        self.allocations = AllocationRepository(db)
        self.beds = BedRepository(db)
        self.rooms = RoomRepository(db)
        self.hostels = HostelRepository(db)

    def create_application(self, student_id: int, data: dict) -> Application:
        existing = self.applications.list_applications(student_id=student_id)
        for app in existing:
            if app.status == ApplicationStatus.PENDING.value:
                raise ConflictError("Student already has a pending application")
        data["student_id"] = student_id
        return self.applications.create_application(**data)

    def get_application(self, application_id: int) -> Application:
        application = self.applications.get_by_id(application_id)
        if not application:
            raise NotFoundError("Application not found")
        return application

    def list_applications(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Application]:
        return self.applications.list_applications(student_id, status, skip, limit)

    def review_application(
        self,
        application_id: int,
        reviewer_id: int,
        status: str,
        remarks: str | None = None,
    ) -> Application:
        application = self.get_application(application_id)
        if application.status != ApplicationStatus.PENDING.value:
            raise ConflictError("Only pending applications can be reviewed")
        if status not in (ApplicationStatus.APPROVED.value, ApplicationStatus.REJECTED.value):
            raise UnprocessableEntityError("Status must be APPROVED or REJECTED")
        return self.applications.update_application(
            application,
            status=status,
            remarks=remarks,
            reviewed_by=reviewer_id,
            reviewed_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
        )

    def allocate_bed(self, data: dict) -> RoomAllocation:
        student_id = data["student_id"]
        bed_id = data["bed_id"]
        room_id = data["room_id"]
        hostel_id = data["hostel_id"]

        active = self.allocations.get_active_by_student(student_id)
        if active:
            raise ConflictError("Student already has an active room allocation")

        bed = self.beds.get_bed(bed_id)
        if not bed:
            raise NotFoundError("Bed not found")
        if bed.status != BedStatus.AVAILABLE.value:
            raise ConflictError("Bed is not available for allocation")
        if bed.room_id != room_id:
            raise ConflictError("Bed does not belong to the specified room")

        room = self.rooms.get_room(room_id)
        if not room:
            raise NotFoundError("Room not found")
        if room.status == "MAINTENANCE":
            raise ConflictError("Room is under maintenance")

        hostel = self.hostels.get_hostel(hostel_id)
        if not hostel:
            raise NotFoundError("Hostel not found")

        if data.get("application_id"):
            application = self.applications.get_by_id(data["application_id"])
            if not application or application.status != ApplicationStatus.APPROVED.value:
                raise ConflictError("Application must be approved before allocation")
            if application.student_id != student_id:
                raise ConflictError("Application does not belong to this student")

        allocation = self.allocations.create_allocation(**data)
        self.beds.update_bed(bed, status=BedStatus.OCCUPIED.value)

        occupied_count = len([
            b for b in self.beds.list_beds(room_id=room_id)
            if b.status == BedStatus.OCCUPIED.value
        ])
        if occupied_count >= room.capacity:
            self.rooms.update_room(room, status="FULL")

        return allocation

    def get_allocation(self, allocation_id: int) -> RoomAllocation:
        allocation = self.allocations.get_by_id(allocation_id)
        if not allocation:
            raise NotFoundError("Allocation not found")
        return allocation

    def list_allocations(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RoomAllocation]:
        return self.allocations.list_allocations(student_id, status, skip, limit)

    def checkout(self, allocation_id: int, check_out_date: date) -> RoomAllocation:
        allocation = self.get_allocation(allocation_id)
        if allocation.status != AllocationStatus.ACTIVE.value:
            raise ConflictError("Only active allocations can be checked out")
        if check_out_date < allocation.allocation_date:
            raise UnprocessableEntityError("Check-out date cannot be before allocation date")

        allocation = self.allocations.update_allocation(
            allocation,
            status=AllocationStatus.CHECKED_OUT.value,
            check_out_date=check_out_date,
        )

        bed = self.beds.get_bed(allocation.bed_id)
        if bed:
            self.beds.update_bed(bed, status=BedStatus.AVAILABLE.value)

        room = self.rooms.get_room(allocation.room_id)
        if room and room.status == "FULL":
            self.rooms.update_room(room, status="AVAILABLE")

        return allocation

    def transfer(
        self,
        allocation_id: int,
        new_room_id: int,
        new_bed_id: int,
        transfer_date: date,
        notes: str | None = None,
    ) -> RoomAllocation:
        old_allocation = self.get_allocation(allocation_id)
        if old_allocation.status != AllocationStatus.ACTIVE.value:
            raise ConflictError("Only active allocations can be transferred")

        new_bed = self.beds.get_bed(new_bed_id)
        if not new_bed:
            raise NotFoundError("New bed not found")
        if new_bed.status != BedStatus.AVAILABLE.value:
            raise ConflictError("New bed is not available")
        if new_bed.room_id != new_room_id:
            raise ConflictError("New bed does not belong to the specified room")

        old_bed = self.beds.get_bed(old_allocation.bed_id)
        if old_bed:
            self.beds.update_bed(old_bed, status=BedStatus.AVAILABLE.value)

        old_room = self.rooms.get_room(old_allocation.room_id)
        if old_room and old_room.status == "FULL":
            self.rooms.update_room(old_room, status="AVAILABLE")

        self.allocations.update_allocation(
            old_allocation,
            status=AllocationStatus.TRANSFERRED.value,
            check_out_date=transfer_date,
        )

        new_allocation = self.allocations.create_allocation(
            student_id=old_allocation.student_id,
            hostel_id=old_allocation.hostel_id,
            room_id=new_room_id,
            bed_id=new_bed_id,
            application_id=old_allocation.application_id,
            allocation_date=transfer_date,
            check_in_date=transfer_date,
            status=AllocationStatus.ACTIVE.value,
            notes=notes,
        )

        self.beds.update_bed(new_bed, status=BedStatus.OCCUPIED.value)

        new_room = self.rooms.get_room(new_room_id)
        if new_room:
            occupied = len([
                b for b in self.beds.list_beds(room_id=new_room_id)
                if b.status == BedStatus.OCCUPIED.value
            ])
            if occupied >= new_room.capacity:
                self.rooms.update_room(new_room, status="FULL")

        return new_allocation
