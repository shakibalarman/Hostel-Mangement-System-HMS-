from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.meal import MealCreate, MealResponse, MealUpdate
from app.services.misc import MiscService

router = APIRouter(prefix="/meals", tags=["meals"])


@router.get("", response_model=list[MealResponse])
def list_meals(
    hostel_id: int | None = None,
    meal_type: str | None = None,
    meal_date: date | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF", "STUDENT")),
) -> list[MealResponse]:
    service = MiscService(db)
    return service.list_meals(hostel_id, meal_type, meal_date, skip, limit)


@router.post("", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
def create_meal(
    payload: MealCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> MealResponse:
    service = MiscService(db)
    return service.create_meal(payload.model_dump())


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF", "STUDENT")),
) -> MealResponse:
    service = MiscService(db)
    return service.get_meal(meal_id)


@router.put("/{meal_id}", response_model=MealResponse)
def update_meal(
    meal_id: int,
    payload: MealUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> MealResponse:
    service = MiscService(db)
    return service.update_meal(meal_id, payload.model_dump(exclude_unset=True))


@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = MiscService(db)
    service.delete_meal(meal_id)
