from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.inventory import InventoryCreate, InventoryResponse, InventoryUpdate
from app.services.misc import MiscService

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("", response_model=list[InventoryResponse])
def list_inventory(
    hostel_id: int | None = None,
    status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> list[InventoryResponse]:
    service = MiscService(db)
    return service.list_inventory(hostel_id, status, skip, limit)


@router.post("", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    payload: InventoryCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> InventoryResponse:
    service = MiscService(db)
    return service.create_inventory_item(payload.model_dump())


@router.get("/{item_id}", response_model=InventoryResponse)
def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> InventoryResponse:
    service = MiscService(db)
    return service.get_inventory_item(item_id)


@router.put("/{item_id}", response_model=InventoryResponse)
def update_inventory_item(
    item_id: int,
    payload: InventoryUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> InventoryResponse:
    service = MiscService(db)
    return service.update_inventory_item(item_id, payload.model_dump(exclude_unset=True))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = MiscService(db)
    service.delete_inventory_item(item_id)
