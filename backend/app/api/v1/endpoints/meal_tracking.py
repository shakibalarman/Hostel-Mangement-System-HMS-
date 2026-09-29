from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.exceptions import NotFoundError
from app.models.user import User
from app.schemas.meal_tracking import (
    MealBalanceResponse,
    MealStatsResponse,
    MealTrackingCreate,
    MealTrackingResponse,
    MealTrackingUpdate,
)
from app.services.meal_tracking import MealTrackingService

router = APIRouter(prefix="/meal-tracking", tags=["meal-tracking"])


def _get_student_id(user: User) -> int:
    if not user.student:
        raise NotFoundError("Student profile not found")
    return user.student.id


@router.get("/stats", response_model=MealStatsResponse)
def get_meal_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MealStatsResponse:
    service = MealTrackingService(db)
    return service.get_meal_stats(_get_student_id(current_user))


@router.get("/balance", response_model=MealBalanceResponse)
def get_meal_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MealBalanceResponse:
    service = MealTrackingService(db)
    return service.get_balance(_get_student_id(current_user))


@router.get("/meals", response_model=list[MealTrackingResponse])
def list_my_meals(
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=2000, le=2100),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[MealTrackingResponse]:
    service = MealTrackingService(db)
    return service.get_student_meals(_get_student_id(current_user), month, year, skip, limit)


@router.post("/meals", response_model=MealTrackingResponse, status_code=status.HTTP_201_CREATED)
def record_meal(
    payload: MealTrackingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MealTrackingResponse:
    service = MealTrackingService(db)
    return service.record_meal(_get_student_id(current_user), payload.model_dump())


@router.put("/meals/{meal_id}", response_model=MealTrackingResponse)
def update_meal(
    meal_id: int,
    payload: MealTrackingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MealTrackingResponse:
    service = MealTrackingService(db)
    return service.update_meal(meal_id, _get_student_id(current_user), payload.model_dump(exclude_unset=True))


@router.delete("/meals/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    service = MealTrackingService(db)
    service.delete_meal(meal_id, _get_student_id(current_user))


@router.post("/purchase", response_model=MealBalanceResponse)
def purchase_meals(
    quantity: int = Query(..., ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MealBalanceResponse:
    service = MealTrackingService(db)
    return service.purchase_meals(_get_student_id(current_user), quantity)
