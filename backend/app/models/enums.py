from __future__ import annotations

import enum


class PyEnum(str, enum.Enum):
    def __str__(self) -> str:
        return self.value


class UserRole(PyEnum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    STUDENT = "STUDENT"


class HostelStatus(PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class RoomType(PyEnum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    SHARED = "SHARED"


class RoomStatus(PyEnum):
    AVAILABLE = "AVAILABLE"
    FULL = "FULL"
    MAINTENANCE = "MAINTENANCE"


class BedStatus(PyEnum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    MAINTENANCE = "MAINTENANCE"


class ApplicationStatus(PyEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AllocationStatus(PyEnum):
    ACTIVE = "ACTIVE"
    TRANSFERRED = "TRANSFERRED"
    CHECKED_OUT = "CHECKED_OUT"


class PaymentStatus(PyEnum):
    PAID = "PAID"
    PENDING = "PENDING"
    FAILED = "FAILED"


class PaymentMethod(PyEnum):
    CASH = "CASH"
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    ONLINE = "OTHER"


class AttendanceStatus(PyEnum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"


class LeaveStatus(PyEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ComplaintStatus(PyEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class MaintenanceStatus(PyEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class MealType(PyEnum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"


class InventoryStatus(PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class NoticeAudience(PyEnum):
    ALL = "ALL"
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    STUDENT = "STUDENT"
