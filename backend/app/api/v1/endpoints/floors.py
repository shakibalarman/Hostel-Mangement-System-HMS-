from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.floor import FloorCreate, FloorResponse, FloorUpdate
from app.services.hostel import HostelService

router = APIRouter(prefix="/floors", tags=["floors"])


@router.get("", response_model=list[FloorResponse])
def list_floors(
    building_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[FloorResponse]:
    service = HostelService(db)
    return service.list_floors(building_id, skip, limit)


@router.post("", response_model=FloorResponse, status_code=status.HTTP_201_CREATED)
def create_floor(
    payload: FloorCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> FloorResponse:
    service = HostelService(db)
    return service.create_floor(payload.model_dump())


@router.get("/{floor_id}", response_model=FloorResponse)
def get_floor(
    floor_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> FloorResponse:
    service = HostelService(db)
    return service.get_floor(floor_id)


@router.put("/{floor_id}", response_model=FloorResponse)
def update_floor(
    floor_id: int,
    payload: FloorUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> FloorResponse:
    service = HostelService(db)
    return service.update_floor(floor_id, payload.model_dump(exclude_unset=True))


@router.delete("/{floor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_floor(
    floor_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = HostelService(db)
    service.delete_floor(floor_id)
