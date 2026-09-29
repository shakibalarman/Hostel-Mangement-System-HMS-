from __future__ import annotations

from datetime import datetime, timezone

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, UnprocessableEntityError
from app.models.attendance import Attendance
from app.models.complaint import Complaint, MaintenanceRequest
from app.models.enums import ComplaintStatus, LeaveStatus, MaintenanceStatus
from app.models.leave import LeaveRequest
from app.repositories.operations import (
    AttendanceRepository,
    ComplaintRepository,
    LeaveRepository,
    MaintenanceRepository,
)


class OperationsService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.attendance = AttendanceRepository(db)
        self.leaves = LeaveRepository(db)
        self.complaints = ComplaintRepository(db)
        self.maintenance = MaintenanceRepository(db)

    def mark_attendance(self, data: dict, marked_by: int) -> Attendance:
        existing = self.attendance.get_by_student_and_date(
            data["student_id"], data["attendance_date"]
        )
        if existing:
            raise ConflictError("Attendance already marked for this student on this date")
        data["marked_by"] = marked_by
        return self.attendance.create_attendance(**data)

    def update_attendance(self, attendance_id: int, data: dict) -> Attendance:
        record = self.attendance.get_by_id(attendance_id)
        if not record:
            raise NotFoundError("Attendance record not found")
        return self.attendance.update_attendance(record, **data)

    def list_attendance(
        self,
        student_id: int | None = None,
        attendance_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Attendance]:
        return self.attendance.list_attendance(student_id, attendance_date, skip, limit)

    def create_leave(self, data: dict) -> LeaveRequest:
        return self.leaves.create_leave(**data)

    def get_leave(self, leave_id: int) -> LeaveRequest:
        leave = self.leaves.get_by_id(leave_id)
        if not leave:
            raise NotFoundError("Leave request not found")
        return leave

    def list_leaves(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[LeaveRequest]:
        return self.leaves.list_leaves(student_id, status, skip, limit)

    def review_leave(
        self,
        leave_id: int,
        reviewer_id: int,
        status: str,
        remarks: str | None = None,
    ) -> LeaveRequest:
        leave = self.get_leave(leave_id)
        if leave.status != LeaveStatus.PENDING.value:
            raise ConflictError("Only pending leave requests can be reviewed")
        if status not in (LeaveStatus.APPROVED.value, LeaveStatus.REJECTED.value):
            raise UnprocessableEntityError("Status must be APPROVED or REJECTED")
        return self.leaves.update_leave(
            leave,
            status=status,
            remarks=remarks,
            reviewed_by=reviewer_id,
            reviewed_at=datetime.now(timezone.utc),
        )

    def create_complaint(self, data: dict) -> Complaint:
        return self.complaints.create_complaint(**data)

    def get_complaint(self, complaint_id: int) -> Complaint:
        complaint = self.complaints.get_by_id(complaint_id)
        if not complaint:
            raise NotFoundError("Complaint not found")
        return complaint

    def list_complaints(
        self,
        student_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Complaint]:
        return self.complaints.list_complaints(student_id, status, skip, limit)

    def update_complaint(
        self,
        complaint_id: int,
        status: str | None = None,
        resolution_notes: str | None = None,
        resolved_by: int | None = None,
    ) -> Complaint:
        complaint = self.get_complaint(complaint_id)
        if status == ComplaintStatus.RESOLVED.value:
            return self.complaints.update_complaint(
                complaint,
                status=status,
                resolution_notes=resolution_notes,
                resolved_by=resolved_by,
                resolved_at=datetime.now(timezone.utc),
            )
        return self.complaints.update_complaint(
            complaint, status=status, resolution_notes=resolution_notes
        )

    def create_maintenance(self, data: dict) -> MaintenanceRequest:
        return self.maintenance.create_maintenance(**data)

    def get_maintenance(self, maintenance_id: int) -> MaintenanceRequest:
        request = self.maintenance.get_by_id(maintenance_id)
        if not request:
            raise NotFoundError("Maintenance request not found")
        return request

    def list_maintenance(
        self,
        student_id: int | None = None,
        status: str | None = None,
        room_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[MaintenanceRequest]:
        return self.maintenance.list_maintenance(student_id, status, room_id, skip, limit)

    def update_maintenance(
        self,
        maintenance_id: int,
        status: str | None = None,
        resolution_notes: str | None = None,
        handled_by: int | None = None,
    ) -> MaintenanceRequest:
        request = self.get_maintenance(maintenance_id)
        if status == MaintenanceStatus.COMPLETED.value:
            return self.maintenance.update_maintenance(
                request,
                status=status,
                resolution_notes=resolution_notes,
                handled_by=handled_by,
                handled_at=datetime.now(timezone.utc),
            )
        return self.maintenance.update_maintenance(
            request, status=status, resolution_notes=resolution_notes
        )
