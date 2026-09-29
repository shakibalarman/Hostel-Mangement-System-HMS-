from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.bed import BedCreate, BedResponse, BedUpdate
from app.services.hostel import HostelService

router = APIRouter(prefix="/beds", tags=["beds"])


@router.get("", response_model=list[BedResponse])
def list_beds(
    room_id: int | None = None,
    status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[BedResponse]:
    service = HostelService(db)
    return service.list_beds(room_id, status, skip, limit)


@router.post("", response_model=BedResponse, status_code=status.HTTP_201_CREATED)
def create_bed(
    payload: BedCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> BedResponse:
    service = HostelService(db)
    return service.create_bed(payload.model_dump())


@router.get("/{bed_id}", response_model=BedResponse)
def get_bed(
    bed_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> BedResponse:
    service = HostelService(db)
    return service.get_bed(bed_id)


@router.put("/{bed_id}", response_model=BedResponse)
def update_bed(
    bed_id: int,
    payload: BedUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> BedResponse:
    service = HostelService(db)
    return service.update_bed(bed_id, payload.model_dump(exclude_unset=True))


@router.delete("/{bed_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bed(
    bed_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = HostelService(db)
    service.delete_bed(bed_id)
