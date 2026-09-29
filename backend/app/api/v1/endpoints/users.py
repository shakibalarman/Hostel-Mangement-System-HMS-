from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def list_users(
    role: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> list[UserResponse]:
    service = UserService(db)
    return service.list_users(role, skip, limit)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> UserResponse:
    service = UserService(db)
    return service.create_user(payload.model_dump())


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> UserResponse:
    service = UserService(db)
    return service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> UserResponse:
    service = UserService(db)
    return service.update_user(user_id, payload.model_dump(exclude_unset=True))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = UserService(db)
    service.delete_user(user_id)
