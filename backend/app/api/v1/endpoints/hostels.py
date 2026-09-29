from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.schemas.hostel import HostelCreate, HostelResponse, HostelUpdate
from app.services.hostel import HostelService

router = APIRouter(prefix="/hostels", tags=["hostels"])


@router.get("", response_model=list[HostelResponse])
def list_hostels(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> list[HostelResponse]:
    service = HostelService(db)
    return service.list_hostels(skip, limit)


@router.post("", response_model=HostelResponse, status_code=status.HTTP_201_CREATED)
def create_hostel(
    payload: HostelCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> HostelResponse:
    service = HostelService(db)
    return service.create_hostel(payload.model_dump())


@router.get("/{hostel_id}", response_model=HostelResponse)
def get_hostel(
    hostel_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> HostelResponse:
    service = HostelService(db)
    return service.get_hostel(hostel_id)


@router.put("/{hostel_id}", response_model=HostelResponse)
def update_hostel(
    hostel_id: int,
    payload: HostelUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> HostelResponse:
    service = HostelService(db)
    return service.update_hostel(hostel_id, payload.model_dump(exclude_unset=True))


@router.delete("/{hostel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hostel(
    hostel_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = HostelService(db)
    service.delete_hostel(hostel_id)
