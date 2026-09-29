from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth, health, hostels, buildings, floors, rooms, beds,
    users, students, staff, applications, allocations,
    fees, payments, expenses, attendance, leaves, complaints, maintenance,
    meals, inventory, notices, notifications, reports,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(health.router)
api_router.include_router(hostels.router)
api_router.include_router(buildings.router)
api_router.include_router(floors.router)
api_router.include_router(rooms.router)
api_router.include_router(beds.router)
api_router.include_router(users.router)
api_router.include_router(students.router)
api_router.include_router(staff.router)
api_router.include_router(applications.router)
api_router.include_router(allocations.router)
api_router.include_router(fees.router)
api_router.include_router(payments.router)
api_router.include_router(expenses.router)
api_router.include_router(attendance.router)
api_router.include_router(leaves.router)
api_router.include_router(complaints.router)
api_router.include_router(maintenance.router)
api_router.include_router(meals.router)
api_router.include_router(inventory.router)
api_router.include_router(notices.router)
api_router.include_router(notifications.router)
api_router.include_router(reports.router)
