from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.complaint import Complaint, MaintenanceRequest
from app.models.leave import LeaveRequest


class AttendanceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, attendance_id: int) -> Attendance | None:
        return self.db.get(Attendance, attendance_id)

    def get_by_student_and_date(self, student_id: int, attendance_date) -> Attendance | None:
        return self.db.execute(
            select(Attendance).where(
                Attendance.student_id == student_id,
                Attendance.attendance_date == attendance_date,
            )
        ).scalar_one_or_none()

    def list_attendance(
        self,
        student_id: int | None = None,
        attendance_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Attendance]:
        stmt = select(Attendance)
        if student_id:
            stmt = stmt.where(Attendance.student_id == student_id)
        if attendance_date:
            stmt = stmt.where(Attendance.attendance_date == attendance_date)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_attendance(self, **kwargs) -> Attendance:
        record = Attendance(**kwargs)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_attendance(self, record: Attendance, **kwargs) -> Attendance:
        for key, value in kwargs.items():
            if value is not None:
                setattr(record, key, value)
        self.db.commit()
        self.db.refresh(record)
        return record


class LeaveRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, leave_id: int) -> LeaveRequest | None:
        return self.db.get(LeaveRequest, leave_id)

    def list_leaves(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[LeaveRequest]:
        stmt = select(LeaveRequest)
        if student_id:
            stmt = stmt.where(LeaveRequest.student_id == student_id)
        if status:
            stmt = stmt.where(LeaveRequest.status == status)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_leave(self, **kwargs) -> LeaveRequest:
        leave = LeaveRequest(**kwargs)
        self.db.add(leave)
        self.db.commit()
        self.db.refresh(leave)
        return leave

    def update_leave(self, leave: LeaveRequest, **kwargs) -> LeaveRequest:
        for key, value in kwargs.items():
            if value is not None:
                setattr(leave, key, value)
        self.db.commit()
        self.db.refresh(leave)
        return leave


class ComplaintRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, complaint_id: int) -> Complaint | None:
        return self.db.get(Complaint, complaint_id)

    def list_complaints(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Complaint]:
        stmt = select(Complaint)
        if student_id:
            stmt = stmt.where(Complaint.student_id == student_id)
        if status:
            stmt = stmt.where(Complaint.status == status)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_complaint(self, **kwargs) -> Complaint:
        complaint = Complaint(**kwargs)
        self.db.add(complaint)
        self.db.commit()
        self.db.refresh(complaint)
        return complaint

    def update_complaint(self, complaint: Complaint, **kwargs) -> Complaint:
        for key, value in kwargs.items():
            if value is not None:
                setattr(complaint, key, value)
        self.db.commit()
        self.db.refresh(complaint)
        return complaint


class MaintenanceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, maintenance_id: int) -> MaintenanceRequest | None:
        return self.db.get(MaintenanceRequest, maintenance_id)

    def list_maintenance(
        self,
        student_id: int | None = None,
        status: str | None = None,
        room_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[MaintenanceRequest]:
        stmt = select(MaintenanceRequest)
        if student_id:
            stmt = stmt.where(MaintenanceRequest.student_id == student_id)
        if status:
            stmt = stmt.where(MaintenanceRequest.status == status)
        if room_id:
            stmt = stmt.where(MaintenanceRequest.room_id == room_id)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_maintenance(self, **kwargs) -> MaintenanceRequest:
        request = MaintenanceRequest(**kwargs)
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request

    def update_maintenance(self, request: MaintenanceRequest, **kwargs) -> MaintenanceRequest:
        for key, value in kwargs.items():
            if value is not None:
                setattr(request, key, value)
        self.db.commit()
        self.db.refresh(request)
        return request
