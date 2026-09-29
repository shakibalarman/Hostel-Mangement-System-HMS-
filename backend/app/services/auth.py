from __future__ import annotations

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.repositories.auth import AuthRepository


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = AuthRepository(db)

    def authenticate(self, username: str, password: str) -> User:
        user = self.repo.get_by_username(username)
        if not user or not user.is_active:
            raise UnauthorizedError("Invalid username or password")
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid username or password")
        return user

    def login(self, username: str, password: str) -> tuple[User, str]:
        user = self.authenticate(username, password)
        self.repo.update_last_login(user)
        token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role.name, "username": user.username},
        )
        return user, token

    def get_current_user(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")
        return user
