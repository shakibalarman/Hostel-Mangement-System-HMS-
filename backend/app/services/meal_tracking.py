from __future__ import annotations

from datetime import date, datetime
from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.meal_tracking import MealBalance, MealTracking
from app.models.user import Student


class MealTrackingService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _get_student(self, student_id: int) -> Student:
        student = self.db.get(Student, student_id)
        if not student:
            raise NotFoundError("Student not found")
        return student

    def _get_balance(self, student_id: int) -> MealBalance:
        balance = self.db.execute(
            select(MealBalance).where(MealBalance.student_id == student_id)
        ).scalar_one_or_none()
        if not balance:
            balance = MealBalance(student_id=student_id)
            self.db.add(balance)
            self.db.commit()
            self.db.refresh(balance)
        return balance

    def record_meal(self, student_id: int, data: dict) -> MealTracking:
        self._get_student(student_id)
        record = MealTracking(student_id=student_id, **data)
        self.db.add(record)

        balance = self._get_balance(student_id)
        balance.meals_consumed += data.get("quantity", 1)
        balance.balance = balance.total_meals_purchased - balance.meals_consumed

        self.db.commit()
        self.db.refresh(record)
        return record

    def get_student_meals(
        self,
        student_id: int,
        month: int | None = None,
        year: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[MealTracking]:
        self._get_student(student_id)
        stmt = select(MealTracking).where(MealTracking.student_id == student_id)
        if month and year:
            stmt = stmt.where(
                extract("month", MealTracking.meal_date) == month,
                extract("year", MealTracking.meal_date) == year,
            )
        stmt = stmt.order_by(MealTracking.meal_date.desc()).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars())

    def get_meal_stats(self, student_id: int) -> dict:
        self._get_student(student_id)
        balance = self._get_balance(student_id)

        now = datetime.now()
        current_month = now.month
        current_year = now.year
        last_month = current_month - 1 if current_month > 1 else 12
        last_month_year = current_year if current_month > 1 else current_year - 1

        current_month_meals = self.db.execute(
            select(func.coalesce(func.sum(MealTracking.quantity), 0)).where(
                MealTracking.student_id == student_id,
                extract("month", MealTracking.meal_date) == current_month,
                extract("year", MealTracking.meal_date) == current_year,
            )
        ).scalar()

        last_month_meals = self.db.execute(
            select(func.coalesce(func.sum(MealTracking.quantity), 0)).where(
                MealTracking.student_id == student_id,
                extract("month", MealTracking.meal_date) == last_month,
                extract("year", MealTracking.meal_date) == last_month_year,
            )
        ).scalar()

        total_spent = self.db.execute(
            select(func.coalesce(func.sum(MealTracking.cost_per_meal * MealTracking.quantity), 0)).where(
                MealTracking.student_id == student_id,
            )
        ).scalar()

        total_days = self.db.execute(
            select(func.count(func.distinct(MealTracking.meal_date))).where(
                MealTracking.student_id == student_id,
            )
        ).scalar()

        return {
            "current_month_meals": current_month_meals or 0,
            "last_month_meals": last_month_meals or 0,
            "total_meals": balance.meals_consumed,
            "balance": balance.balance,
            "total_spent": total_spent or 0,
            "daily_average": round(balance.meals_consumed / max(total_days, 1), 2),
        }

    def get_balance(self, student_id: int) -> MealBalance:
        self._get_student(student_id)
        return self._get_balance(student_id)

    def purchase_meals(self, student_id: int, quantity: int) -> MealBalance:
        self._get_student(student_id)
        balance = self._get_balance(student_id)
        balance.total_meals_purchased += quantity
        balance.balance = balance.total_meals_purchased - balance.meals_consumed
        self.db.commit()
        self.db.refresh(balance)
        return balance

    def update_meal(self, meal_id: int, student_id: int, data: dict) -> MealTracking:
        record = self.db.execute(
            select(MealTracking).where(
                MealTracking.id == meal_id,
                MealTracking.student_id == student_id,
            )
        ).scalar_one_or_none()
        if not record:
            raise NotFoundError("Meal record not found")

        old_quantity = record.quantity
        for key, value in data.items():
            if value is not None:
                setattr(record, key, value)

        if "quantity" in data:
            balance = self._get_balance(student_id)
            balance.meals_consumed += data["quantity"] - old_quantity
            balance.balance = balance.total_meals_purchased - balance.meals_consumed

        self.db.commit()
        self.db.refresh(record)
        return record

    def delete_meal(self, meal_id: int, student_id: int) -> None:
        record = self.db.execute(
            select(MealTracking).where(
                MealTracking.id == meal_id,
                MealTracking.student_id == student_id,
            )
        ).scalar_one_or_none()
        if not record:
            raise NotFoundError("Meal record not found")

        balance = self._get_balance(student_id)
        balance.meals_consumed -= record.quantity
        balance.balance = balance.total_meals_purchased - balance.meals_consumed

        self.db.delete(record)
        self.db.commit()
