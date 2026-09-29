from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import Role, Staff, Student, User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.db.execute(select(User).where(User.username == username)).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        return self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def list_users(self, role: str | None = None, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = select(User)
        if role:
            stmt = stmt.join(Role).where(Role.name == role)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_user(self, **kwargs) -> User:
        user = User(**kwargs)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()


class StudentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, student_id: int) -> Student | None:
        return self.db.get(Student, student_id)

    def get_by_user_id(self, user_id: int) -> Student | None:
        return self.db.execute(select(Student).where(Student.user_id == user_id)).scalar_one_or_none()

    def get_by_student_number(self, student_number: str) -> Student | None:
        return self.db.execute(select(Student).where(Student.student_number == student_number)).scalar_one_or_none()

    def list_students(self, skip: int = 0, limit: int = 100) -> list[Student]:
        return list(self.db.execute(select(Student).offset(skip).limit(limit)).scalars())

    def create_student(self, **kwargs) -> Student:
        student = Student(**kwargs)
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def update_student(self, student: Student, **kwargs) -> Student:
        for key, value in kwargs.items():
            if value is not None:
                setattr(student, key, value)
        self.db.commit()
        self.db.refresh(student)
        return student

    def delete_student(self, student: Student) -> None:
        self.db.delete(student)
        self.db.commit()


class StaffRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, staff_id: int) -> Staff | None:
        return self.db.get(Staff, staff_id)

    def get_by_user_id(self, user_id: int) -> Staff | None:
        return self.db.execute(select(Staff).where(Staff.user_id == user_id)).scalar_one_or_none()

    def get_by_staff_number(self, staff_number: str) -> Staff | None:
        return self.db.execute(select(Staff).where(Staff.staff_number == staff_number)).scalar_one_or_none()

    def list_staff(self, skip: int = 0, limit: int = 100) -> list[Staff]:
        return list(self.db.execute(select(Staff).offset(skip).limit(limit)).scalars())

    def create_staff(self, **kwargs) -> Staff:
        staff = Staff(**kwargs)
        self.db.add(staff)
        self.db.commit()
        self.db.refresh(staff)
        return staff

    def update_staff(self, staff: Staff, **kwargs) -> Staff:
        for key, value in kwargs.items():
            if value is not None:
                setattr(staff, key, value)
        self.db.commit()
        self.db.refresh(staff)
        return staff

    def delete_staff(self, staff: Staff) -> None:
        self.db.delete(staff)
        self.db.commit()
