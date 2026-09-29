from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import Application, RoomAllocation
from app.models.enums import AllocationStatus, ApplicationStatus


class ApplicationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, application_id: int) -> Application | None:
        return self.db.get(Application, application_id)

    def list_applications(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Application]:
        stmt = select(Application)
        if student_id:
            stmt = stmt.where(Application.student_id == student_id)
        if status:
            stmt = stmt.where(Application.status == status)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_application(self, **kwargs) -> Application:
        application = Application(**kwargs)
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def update_application(self, application: Application, **kwargs) -> Application:
        for key, value in kwargs.items():
            if value is not None:
                setattr(application, key, value)
        self.db.commit()
        self.db.refresh(application)
        return application


class AllocationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, allocation_id: int) -> RoomAllocation | None:
        return self.db.get(RoomAllocation, allocation_id)

    def list_allocations(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RoomAllocation]:
        stmt = select(RoomAllocation)
        if student_id:
            stmt = stmt.where(RoomAllocation.student_id == student_id)
        if status:
            stmt = stmt.where(RoomAllocation.status == status)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def get_active_by_student(self, student_id: int) -> RoomAllocation | None:
        return self.db.execute(
            select(RoomAllocation).where(
                RoomAllocation.student_id == student_id,
                RoomAllocation.status == AllocationStatus.ACTIVE.value,
            )
        ).scalar_one_or_none()

    def get_active_by_bed(self, bed_id: int) -> RoomAllocation | None:
        return self.db.execute(
            select(RoomAllocation).where(
                RoomAllocation.bed_id == bed_id,
                RoomAllocation.status == AllocationStatus.ACTIVE.value,
            )
        ).scalar_one_or_none()

    def create_allocation(self, **kwargs) -> RoomAllocation:
        allocation = RoomAllocation(**kwargs)
        self.db.add(allocation)
        self.db.commit()
        self.db.refresh(allocation)
        return allocation

    def update_allocation(self, allocation: RoomAllocation, **kwargs) -> RoomAllocation:
        for key, value in kwargs.items():
            if value is not None:
                setattr(allocation, key, value)
        self.db.commit()
        self.db.refresh(allocation)
        return allocation
