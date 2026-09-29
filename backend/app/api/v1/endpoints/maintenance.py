from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.complaint import MaintenanceCreate, MaintenanceResponse, MaintenanceUpdate
from app.services.operations import OperationsService
from app.services.user import UserService

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.get("", response_model=list[MaintenanceResponse])
def list_maintenance(
    student_id: int | None = None,
    status: str | None = None,
    room_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[MaintenanceResponse]:
    service = OperationsService(db)
    if current_user.role.name == "STUDENT":
        student = UserService(db).get_student_by_user(current_user.id)
        if not student:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Student profile not found")
        student_id = student.id
    return service.list_maintenance(student_id, status, room_id, skip, limit)


@router.post("", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(
    payload: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MaintenanceResponse:
    student = UserService(db).get_student_by_user(current_user.id)
    if not student:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Student profile not found")
    service = OperationsService(db)
    return service.create_maintenance({**payload.model_dump(), "student_id": student.id})


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> MaintenanceResponse:
    service = OperationsService(db)
    return service.get_maintenance(maintenance_id)


@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance(
    maintenance_id: int,
    payload: MaintenanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MaintenanceResponse:
    service = OperationsService(db)
    return service.update_maintenance(
        maintenance_id,
        status=payload.status,
        resolution_notes=payload.resolution_notes,
        handled_by=current_user.id,
    )
