"""
DEVELOPMENT ONLY seed script.
Creates sample data for local development and testing.
DO NOT run this in production.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.enums import (
    ApplicationStatus,
    BedStatus,
    HostelStatus,
    MealType,
    RoomType,
    UserRole,
)
from app.models.hostel import Bed, Building, Floor, Hostel, Room
from app.models.meal import Meal
from app.models.notice import Notice
from app.models.user import Role, Staff, Student, User
from app.models.finance import FeeStructure


def seed() -> None:
    db: Session = SessionLocal()
    try:
        # Create roles
        roles = {}
        for role_name in [UserRole.ADMIN.value, UserRole.STAFF.value, UserRole.STUDENT.value]:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name, description=f"{role_name} role")
                db.add(role)
                db.flush()
            roles[role_name] = role

        # Create admin user
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@hms.local",
                full_name="System Administrator",
                hashed_password=hash_password("Admin@123456"),
                role_id=roles[UserRole.ADMIN.value].id,
                is_active=True,
            )
            db.add(admin)
            db.flush()

        # Create staff user
        staff_user = db.query(User).filter(User.username == "staff").first()
        if not staff_user:
            staff_user = User(
                username="staff",
                email="staff@hms.local",
                full_name="Hostel Staff Member",
                hashed_password=hash_password("Staff@123456"),
                role_id=roles[UserRole.STAFF.value].id,
                is_active=True,
            )
            db.add(staff_user)
            db.flush()
            staff_profile = Staff(
                user_id=staff_user.id,
                staff_number="STF-001",
                designation="Hostel Warden",
                department="Hostel Management",
                hire_date=date.today() - timedelta(days=365),
            )
            db.add(staff_profile)

        # Create student user
        student_user = db.query(User).filter(User.username == "student").first()
        if not student_user:
            student_user = User(
                username="student",
                email="student@hms.local",
                full_name="Test Student",
                hashed_password=hash_password("Student@123456"),
                role_id=roles[UserRole.STUDENT.value].id,
                is_active=True,
            )
            db.add(student_user)
            db.flush()
            student_profile = Student(
                user_id=student_user.id,
                student_number="STU-2024-001",
                date_of_birth=date(2000, 1, 15),
                gender="Male",
                address="123 Campus Road",
                emergency_contact="01712345678",
                department="Computer Science",
                year_of_study="3rd Year",
            )
            db.add(student_profile)

        # Create hostel
        hostel = db.query(Hostel).filter(Hostel.code == "H1").first()
        if not hostel:
            hostel = Hostel(
                name="North Hostel",
                code="H1",
                address="North Campus",
                contact_number="01712345678",
                description="Main boys hostel",
                status=HostelStatus.ACTIVE.value,
            )
            db.add(hostel)
            db.flush()

        # Create building
        building = db.query(Building).filter(Building.code == "B1").first()
        if not building:
            building = Building(
                hostel_id=hostel.id,
                name="Block A",
                code="B1",
                description="Main academic block",
                status=HostelStatus.ACTIVE.value,
            )
            db.add(building)
            db.flush()

        # Create floors
        floor1 = db.query(Floor).filter(Floor.name == "Floor 1", Floor.building_id == building.id).first()
        if not floor1:
            floor1 = Floor(
                building_id=building.id,
                name="Floor 1",
                floor_number=1,
                status=HostelStatus.ACTIVE.value,
            )
            db.add(floor1)
            db.flush()

        floor2 = db.query(Floor).filter(Floor.name == "Floor 2", Floor.building_id == building.id).first()
        if not floor2:
            floor2 = Floor(
                building_id=building.id,
                name="Floor 2",
                floor_number=2,
                status=HostelStatus.ACTIVE.value,
            )
            db.add(floor2)
            db.flush()

        # Create rooms and beds
        room_data = [
            (floor1.id, "101", RoomType.SINGLE.value, 1, 5000),
            (floor1.id, "102", RoomType.DOUBLE.value, 2, 3500),
            (floor1.id, "103", RoomType.SHARED.value, 4, 2000),
            (floor2.id, "201", RoomType.SINGLE.value, 1, 5000),
            (floor2.id, "202", RoomType.DOUBLE.value, 2, 3500),
        ]
        for floor_id, room_num, room_type, capacity, rent in room_data:
            room = db.query(Room).filter(
                Room.room_number == room_num, Room.floor_id == floor_id
            ).first()
            if not room:
                room = Room(
                    floor_id=floor_id,
                    room_number=room_num,
                    room_type=room_type,
                    capacity=capacity,
                    rent=rent,
                    status="AVAILABLE",
                )
                db.add(room)
                db.flush()
                for i in range(1, capacity + 1):
                    bed = Bed(
                        room_id=room.id,
                        bed_number=f"{room_num}-B{i}",
                        status=BedStatus.AVAILABLE.value,
                    )
                    db.add(bed)

        # Create fee structures
        fee_types = [
            ("Hostel Fee", "HOSTEL_FEE", 5000),
            ("Meal Fee", "MEAL_FEE", 3000),
            ("Other Charges", "OTHER", 1000),
        ]
        for name, fee_type, amount in fee_types:
            fee = db.query(FeeStructure).filter(
                FeeStructure.fee_type == fee_type, FeeStructure.hostel_id == hostel.id
            ).first()
            if not fee:
                fee = FeeStructure(
                    hostel_id=hostel.id,
                    name=name,
                    fee_type=fee_type,
                    amount=amount,
                    is_active=True,
                )
                db.add(fee)

        # Create meals
        meal_types = [MealType.BREAKFAST.value, MealType.LUNCH.value, MealType.DINNER.value]
        menus = {
            MealType.BREAKFAST.value: "Egg, Bread, Tea, Banana",
            MealType.LUNCH.value: "Rice, Chicken, Salad, Water",
            MealType.DINNER.value: "Rice, Fish, Vegetables, Water",
        }
        for meal_type in meal_types:
            meal = db.query(Meal).filter(
                Meal.meal_type == meal_type,
                Meal.meal_date == date.today(),
                Meal.hostel_id == hostel.id,
            ).first()
            if not meal:
                meal = Meal(
                    hostel_id=hostel.id,
                    meal_type=meal_type,
                    menu=menus[meal_type],
                    meal_date=date.today(),
                    is_active=True,
                )
                db.add(meal)

        # Create notices
        notice = db.query(Notice).filter(Notice.title == "Welcome to HMS").first()
        if not notice:
            notice = Notice(
                title="Welcome to HMS",
                content="Welcome to the Hostel Management System. Please read all rules and regulations.",
                audience="ALL",
                is_active=True,
                created_by=admin.id,
            )
            db.add(notice)

        db.commit()
        print("Seed data created successfully!")
        print("\nDEVELOPMENT CREDENTIALS (DO NOT USE IN PRODUCTION):")
        print("  Admin:  username=admin,    password=Admin@123456")
        print("  Staff:  username=staff,    password=Staff@123456")
        print("  Student: username=student, password=Student@123456")
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
