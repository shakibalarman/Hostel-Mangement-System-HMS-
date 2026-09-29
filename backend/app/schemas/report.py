from __future__ import annotations

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_students: int
    total_staff: int
    total_hostels: int
    total_rooms: int
    total_beds: int
    occupied_beds: int
    available_beds: int
    pending_applications: int
    pending_payments: int
    active_complaints: int
    pending_maintenance: int
    monthly_revenue: int
    monthly_expenses: int


class OccupancyReport(BaseModel):
    hostel_id: int
    hostel_name: str
    total_rooms: int
    total_beds: int
    occupied_beds: int
    available_beds: int
    occupancy_rate: float


class StudentReport(BaseModel):
    id: int
    student_number: str
    full_name: str
    department: str | None
    room_number: str | None
    bed_number: str | None
    status: str


class PaymentReport(BaseModel):
    id: int
    student_name: str
    fee_type: str
    amount: int
    status: str
    payment_date: str | None


class OutstandingFeeReport(BaseModel):
    student_id: int
    student_name: str
    student_number: str
    total_fees: int
    total_paid: int
    outstanding: int
