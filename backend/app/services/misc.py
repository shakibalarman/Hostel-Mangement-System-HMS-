from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.inventory import Inventory
from app.models.meal import Meal
from app.models.notice import Notice
from app.models.notification import Notification
from app.repositories.hostel import HostelRepository
from app.repositories.misc import (
    InventoryRepository,
    MealRepository,
    NoticeRepository,
    NotificationRepository,
)


class MiscService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.meals = MealRepository(db)
        self.inventory = InventoryRepository(db)
        self.notices = NoticeRepository(db)
        self.notifications = NotificationRepository(db)
        self.hostels = HostelRepository(db)

    def create_meal(self, data: dict) -> Meal:
        hostel = self.hostels.get_hostel(data["hostel_id"])
        if not hostel:
            raise NotFoundError("Hostel not found")
        return self.meals.create_meal(**data)

    def get_meal(self, meal_id: int) -> Meal:
        meal = self.meals.get_by_id(meal_id)
        if not meal:
            raise NotFoundError("Meal not found")
        return meal

    def list_meals(
        self,
        hostel_id: int | None = None,
        meal_type: str | None = None,
        meal_date=None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Meal]:
        return self.meals.list_meals(hostel_id, meal_type, meal_date, skip, limit)

    def update_meal(self, meal_id: int, data: dict) -> Meal:
        meal = self.get_meal(meal_id)
        return self.meals.update_meal(meal, **data)

    def delete_meal(self, meal_id: int) -> None:
        meal = self.get_meal(meal_id)
        self.meals.delete_meal(meal)

    def create_inventory_item(self, data: dict) -> Inventory:
        hostel = self.hostels.get_hostel(data["hostel_id"])
        if not hostel:
            raise NotFoundError("Hostel not found")
        return self.inventory.create_item(**data)

    def get_inventory_item(self, item_id: int) -> Inventory:
        item = self.inventory.get_by_id(item_id)
        if not item:
            raise NotFoundError("Inventory item not found")
        return item

    def list_inventory(
        self,
        hostel_id: int | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Inventory]:
        return self.inventory.list_inventory(hostel_id, status, skip, limit)

    def update_inventory_item(self, item_id: int, data: dict) -> Inventory:
        item = self.get_inventory_item(item_id)
        return self.inventory.update_item(item, **data)

    def delete_inventory_item(self, item_id: int) -> None:
        item = self.get_inventory_item(item_id)
        self.inventory.delete_item(item)

    def create_notice(self, data: dict) -> Notice:
        return self.notices.create_notice(**data)

    def get_notice(self, notice_id: int) -> Notice:
        notice = self.notices.get_by_id(notice_id)
        if not notice:
            raise NotFoundError("Notice not found")
        return notice

    def list_notices(
        self,
        audience: str | None = None,
        is_active: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Notice]:
        return self.notices.list_notices(audience, is_active, skip, limit)

    def update_notice(self, notice_id: int, data: dict) -> Notice:
        notice = self.get_notice(notice_id)
        return self.notices.update_notice(notice, **data)

    def delete_notice(self, notice_id: int) -> None:
        notice = self.get_notice(notice_id)
        self.notices.delete_notice(notice)

    def list_notifications(
        self,
        user_id: int,
        is_read: bool | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Notification]:
        return self.notifications.list_for_user(user_id, is_read, skip, limit)

    def mark_notification_read(self, notification_id: int) -> Notification:
        notification = self.notifications.get_by_id(notification_id)
        if not notification:
            raise NotFoundError("Notification not found")
        return self.notifications.mark_as_read(notification)

    def mark_all_notifications_read(self, user_id: int) -> int:
        return self.notifications.mark_all_as_read(user_id)
