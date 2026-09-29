from __future__ import annotations

from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.user import Role, Staff, Student, User
from app.repositories.user import StaffRepository, StudentRepository, UserRepository


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.students = StudentRepository(db)
        self.staff = StaffRepository(db)

    def _get_role(self, role_name: str) -> Role:
        role = self.db.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
        if not role:
            raise NotFoundError(f"Role '{role_name}' not found")
        return role

    def create_user(self, data: dict) -> User:
        if self.users.get_by_username(data["username"]):
            raise ConflictError("Username already exists")
        if self.users.get_by_email(data["email"]):
            raise ConflictError("Email already exists")
        role = self._get_role(data.pop("role"))
        data["hashed_password"] = hash_password(data.pop("password"))
        data["role_id"] = role.id
        return self.users.create_user(**data)

    def get_user(self, user_id: int) -> User:
        user = self.users.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    def list_users(self, role: str | None = None, skip: int = 0, limit: int = 100) -> list[User]:
        return self.users.list_users(role, skip, limit)

    def update_user(self, user_id: int, data: dict) -> User:
        user = self.get_user(user_id)
        if "email" in data and data["email"] != user.email:
            if self.users.get_by_email(data["email"]):
                raise ConflictError("Email already exists")
        return self.users.update_user(user, **data)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.users.delete_user(user)

    def create_student(self, data: dict) -> Student:
        if self.users.get_by_username(data["username"]):
            raise ConflictError("Username already exists")
        if self.users.get_by_email(data["email"]):
            raise ConflictError("Email already exists")
        if self.students.get_by_student_number(data["student_number"]):
            raise ConflictError("Student number already exists")
        role = self._get_role("STUDENT")
        user_data = {
            "username": data.pop("username"),
            "email": data.pop("email"),
            "full_name": data.pop("full_name"),
            "phone": data.pop("phone", None),
            "hashed_password": hash_password(data.pop("password")),
            "role_id": role.id,
        }
        user = self.users.create_user(**user_data)
        data["user_id"] = user.id
        return self.students.create_student(**data)

    def get_student(self, student_id: int) -> Student:
        student = self.students.get_by_id(student_id)
        if not student:
            raise NotFoundError("Student not found")
        return student

    def get_student_by_user(self, user_id: int) -> Student | None:
        return self.students.get_by_user_id(user_id)

    def list_students(self, skip: int = 0, limit: int = 100) -> list[Student]:
        return self.students.list_students(skip, limit)

    def update_student(self, student_id: int, data: dict) -> Student:
        student = self.get_student(student_id)
        return self.students.update_student(student, **data)

    def delete_student(self, student_id: int) -> None:
        student = self.get_student(student_id)
        self.students.delete_student(student)

    def create_staff(self, data: dict) -> Staff:
        if self.users.get_by_username(data["username"]):
            raise ConflictError("Username already exists")
        if self.users.get_by_email(data["email"]):
            raise ConflictError("Email already exists")
        if self.staff.get_by_staff_number(data["staff_number"]):
            raise ConflictError("Staff number already exists")
        role = self._get_role("STAFF")
        user_data = {
            "username": data.pop("username"),
            "email": data.pop("email"),
            "full_name": data.pop("full_name"),
            "phone": data.pop("phone", None),
            "hashed_password": hash_password(data.pop("password")),
            "role_id": role.id,
        }
        user = self.users.create_user(**user_data)
        data["user_id"] = user.id
        return self.staff.create_staff(**data)

    def get_staff(self, staff_id: int) -> Staff:
        staff_member = self.staff.get_by_id(staff_id)
        if not staff_member:
            raise NotFoundError("Staff not found")
        return staff_member

    def get_staff_by_user(self, user_id: int) -> Staff | None:
        return self.staff.get_by_user_id(user_id)

    def list_staff(self, skip: int = 0, limit: int = 100) -> list[Staff]:
        return self.staff.list_staff(skip, limit)

    def update_staff(self, staff_id: int, data: dict) -> Staff:
        staff_member = self.get_staff(staff_id)
        return self.staff.update_staff(staff_member, **data)

    def delete_staff(self, staff_id: int) -> None:
        staff_member = self.get_staff(staff_id)
        self.staff.delete_staff(staff_member)
