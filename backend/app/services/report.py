from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.application import Application, RoomAllocation
from app.models.enums import ApplicationStatus, BedStatus, PaymentStatus
from app.models.finance import FeeStructure, Payment
from app.models.hostel import Bed, Building, Floor, Hostel, Room
from app.models.user import Staff, Student, User


class ReportService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_dashboard_stats(self) -> dict:
        total_students = self.db.scalar(select(func.count(Student.id))) or 0
        total_staff = self.db.scalar(select(func.count(Staff.id))) or 0
        total_hostels = self.db.scalar(select(func.count(Hostel.id))) or 0
        total_rooms = self.db.scalar(select(func.count(Room.id))) or 0
        total_beds = self.db.scalar(select(func.count(Bed.id))) or 0
        occupied_beds = self.db.scalar(
            select(func.count(Bed.id)).where(Bed.status == BedStatus.OCCUPIED.value)
        ) or 0
        available_beds = self.db.scalar(
            select(func.count(Bed.id)).where(Bed.status == BedStatus.AVAILABLE.value)
        ) or 0
        pending_applications = self.db.scalar(
            select(func.count(Application.id)).where(
                Application.status == ApplicationStatus.PENDING.value
            )
        ) or 0
        pending_payments = self.db.scalar(
            select(func.count(Payment.id)).where(Payment.status == PaymentStatus.PENDING.value)
        ) or 0
        from app.models.complaint import Complaint
        from app.models.enums import ComplaintStatus
        active_complaints = self.db.scalar(
            select(func.count(Complaint.id)).where(
                Complaint.status.in_([ComplaintStatus.PENDING.value, ComplaintStatus.IN_PROGRESS.value])
            )
        ) or 0
        from app.models.complaint import MaintenanceRequest
        from app.models.enums import MaintenanceStatus
        pending_maintenance = self.db.scalar(
            select(func.count(MaintenanceRequest.id)).where(
                MaintenanceRequest.status.in_([MaintenanceStatus.PENDING.value, MaintenanceStatus.IN_PROGRESS.value])
            )
        ) or 0
        from app.models.finance import Expense
        from datetime import date
        now = date.today()
        month_start = now.replace(day=1)
        monthly_revenue = self.db.scalar(
            select(func.coalesce(func.sum(Payment.amount), 0)).where(
                Payment.status == PaymentStatus.PAID.value,
                Payment.payment_date >= month_start,
            )
        ) or 0
        monthly_expenses = self.db.scalar(
            select(func.coalesce(func.sum(Expense.amount), 0)).where(
                Expense.expense_date >= month_start,
            )
        ) or 0
        return {
            "total_students": total_students,
            "total_staff": total_staff,
            "total_hostels": total_hostels,
            "total_rooms": total_rooms,
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "available_beds": available_beds,
            "pending_applications": pending_applications,
            "pending_payments": pending_payments,
            "active_complaints": active_complaints,
            "pending_maintenance": pending_maintenance,
            "monthly_revenue": monthly_revenue,
            "monthly_expenses": monthly_expenses,
        }

    def get_occupancy_report(self) -> list[dict]:
        hostels = self.db.execute(select(Hostel)).scalars()
        report = []
        for hostel in hostels:
            rooms = self.db.scalar(
                select(func.count(Room.id)).join(Room.floor).join(Floor.building).where(
                    Floor.building.has(hostel_id=hostel.id)
                )
            ) or 0
            beds = self.db.scalar(
                select(func.count(Bed.id)).join(Bed.room).join(Room.floor).join(Floor.building).where(
                    Floor.building.has(hostel_id=hostel.id)
                )
            ) or 0
            occupied = self.db.scalar(
                select(func.count(Bed.id)).join(Bed.room).join(Room.floor).join(Floor.building).where(
                    Floor.building.has(hostel_id=hostel.id),
                    Bed.status == BedStatus.OCCUPIED.value,
                )
            ) or 0
            report.append({
                "hostel_id": hostel.id,
                "hostel_name": hostel.name,
                "total_rooms": rooms,
                "total_beds": beds,
                "occupied_beds": occupied,
                "available_beds": beds - occupied,
                "occupancy_rate": round(occupied / beds * 100, 2) if beds > 0 else 0,
            })
        return report

    def get_student_report(self) -> list[dict]:
        students = self.db.execute(select(Student)).scalars()
        report = []
        for student in students:
            user = self.db.get(User, student.user_id)
            allocation = self.db.execute(
                select(RoomAllocation).where(
                    RoomAllocation.student_id == student.id,
                    RoomAllocation.status == "ACTIVE",
                )
            ).scalar_one_or_none()
            room_number = None
            bed_number = None
            if allocation:
                room = self.db.get(Room, allocation.room_id)
                bed = self.db.get(Bed, allocation.bed_id)
                room_number = room.room_number if room else None
                bed_number = bed.bed_number if bed else None
            report.append({
                "id": student.id,
                "student_number": student.student_number,
                "full_name": user.full_name if user else "",
                "department": student.department,
                "room_number": room_number,
                "bed_number": bed_number,
                "status": "Allocated" if allocation else "Unallocated",
            })
        return report

    def get_payment_report(self) -> list[dict]:
        payments = self.db.execute(select(Payment)).scalars()
        report = []
        for payment in payments:
            student = self.db.get(Student, payment.student_id)
            user = self.db.get(User, student.user_id) if student else None
            fee = self.db.get(FeeStructure, payment.fee_structure_id)
            report.append({
                "id": payment.id,
                "student_name": user.full_name if user else "",
                "fee_type": fee.fee_type if fee else "",
                "amount": payment.amount,
                "status": payment.status,
                "payment_date": str(payment.payment_date) if payment.payment_date else None,
            })
        return report

    def get_outstanding_fees_report(self) -> list[dict]:
        students = self.db.execute(select(Student)).scalars()
        report = []
        for student in students:
            user = self.db.get(User, student.user_id)
            total_fees = self.db.scalar(
                select(func.coalesce(func.sum(FeeStructure.amount), 0)).where(
                    FeeStructure.is_active == True
                )
            ) or 0
            total_paid = self.db.scalar(
                select(func.coalesce(func.sum(Payment.amount), 0)).where(
                    Payment.student_id == student.id,
                    Payment.status == PaymentStatus.PAID.value,
                )
            ) or 0
            report.append({
                "student_id": student.id,
                "student_name": user.full_name if user else "",
                "student_number": student.student_number,
                "total_fees": total_fees,
                "total_paid": total_paid,
                "outstanding": total_fees - total_paid,
            })
        return report
