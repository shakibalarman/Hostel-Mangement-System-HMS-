from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.building import BuildingCreate, BuildingResponse, BuildingUpdate
from app.services.hostel import HostelService

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("", response_model=list[BuildingResponse])
def list_buildings(
    hostel_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[BuildingResponse]:
    service = HostelService(db)
    return service.list_buildings(hostel_id, skip, limit)


@router.post("", response_model=BuildingResponse, status_code=status.HTTP_201_CREATED)
def create_building(
    payload: BuildingCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> BuildingResponse:
    service = HostelService(db)
    return service.create_building(payload.model_dump())


@router.get("/{building_id}", response_model=BuildingResponse)
def get_building(
    building_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> BuildingResponse:
    service = HostelService(db)
    return service.get_building(building_id)


@router.put("/{building_id}", response_model=BuildingResponse)
def update_building(
    building_id: int,
    payload: BuildingUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> BuildingResponse:
    service = HostelService(db)
    return service.update_building(building_id, payload.model_dump(exclude_unset=True))


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_building(
    building_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = HostelService(db)
    service.delete_building(building_id)
