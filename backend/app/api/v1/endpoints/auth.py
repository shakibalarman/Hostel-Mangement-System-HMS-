from __future__ import annotations

from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_token_payload
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    username: str = Form(min_length=1, max_length=50),
    password: str = Form(min_length=1, max_length=128),
    db: Session = Depends(get_db),
) -> TokenResponse:
    service = AuthService(db)
    _, token = service.login(username, password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> UserResponse:
    service = AuthService(db)
    user = service.get_current_user(int(payload["sub"]))
    return UserResponse.model_validate(user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout() -> None:
    return None
