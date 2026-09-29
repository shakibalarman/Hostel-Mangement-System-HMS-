from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.meal import Meal, MealAllocation
from app.models.notice import Notice
from app.models.notification import Notification


class MealRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, meal_id: int) -> Meal | None:
        return self.db.get(Meal, meal_id)

    def list_meals(
        self,
        hostel_id: int | None = None,
        meal_type: str | None = None,
        meal_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Meal]:
        stmt = select(Meal)
        if hostel_id:
            stmt = stmt.where(Meal.hostel_id == hostel_id)
        if meal_type:
            stmt = stmt.where(Meal.meal_type == meal_type)
        if meal_date:
            stmt = stmt.where(Meal.meal_date == meal_date)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_meal(self, **kwargs) -> Meal:
        meal = Meal(**kwargs)
        self.db.add(meal)
        self.db.commit()
        self.db.refresh(meal)
        return meal

    def update_meal(self, meal: Meal, **kwargs) -> Meal:
        for key, value in kwargs.items():
            if value is not None:
                setattr(meal, key, value)
        self.db.commit()
        self.db.refresh(meal)
        return meal

    def delete_meal(self, meal: Meal) -> None:
        self.db.delete(meal)
        self.db.commit()


class InventoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, item_id: int) -> Inventory | None:
        return self.db.get(Inventory, item_id)

    def list_inventory(
        self,
        hostel_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Inventory]:
        stmt = select(Inventory)
        if hostel_id:
            stmt = stmt.where(Inventory.hostel_id == hostel_id)
        if status:
            stmt = stmt.where(Inventory.status == status)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_item(self, **kwargs) -> Inventory:
        item = Inventory(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_item(self, item: Inventory, **kwargs) -> Inventory:
        for key, value in kwargs.items():
            if value is not None:
                setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_item(self, item: Inventory) -> None:
        self.db.delete(item)
        self.db.commit()


class NoticeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, notice_id: int) -> Notice | None:
        return self.db.get(Notice, notice_id)

    def list_notices(
        self,
        audience: str | None = None,
        is_active: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Notice]:
        stmt = select(Notice)
        if audience:
            stmt = stmt.where(Notice.audience == audience)
        if is_active is not None:
            stmt = stmt.where(Notice.is_active == is_active)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_notice(self, **kwargs) -> Notice:
        notice = Notice(**kwargs)
        self.db.add(notice)
        self.db.commit()
        self.db.refresh(notice)
        return notice

    def update_notice(self, notice: Notice, **kwargs) -> Notice:
        for key, value in kwargs.items():
            if value is not None:
                setattr(notice, key, value)
        self.db.commit()
        self.db.refresh(notice)
        return notice

    def delete_notice(self, notice: Notice) -> None:
        self.db.delete(notice)
        self.db.commit()


class NotificationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, notification_id: int) -> Notification | None:
        return self.db.get(Notification, notification_id)

    def list_for_user(
        self,
        user_id: int,
        is_read: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Notification]:
        stmt = select(Notification).where(Notification.user_id == user_id)
        if is_read is not None:
            stmt = stmt.where(Notification.is_read == is_read)
        return list(self.db.execute(stmt.offset(skip).limit(limit)).scalars())

    def create_notification(self, **kwargs) -> Notification:
        notification = Notification(**kwargs)
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_as_read(self, notification: Notification) -> Notification:
        notification.is_read = True
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_all_as_read(self, user_id: int) -> int:
        result = self.db.execute(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
        ).scalars()
        count = 0
        for n in result:
            n.is_read = True
            count += 1
        self.db.commit()
        return count
