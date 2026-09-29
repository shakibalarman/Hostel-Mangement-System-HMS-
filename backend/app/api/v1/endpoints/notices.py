from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.user import User
from app.schemas.notice import NoticeCreate, NoticeResponse, NoticeUpdate
from app.services.misc import MiscService

router = APIRouter(prefix="/notices", tags=["notices"])


@router.get("", response_model=list[NoticeResponse])
def list_notices(
    audience: str | None = None,
    is_active: bool | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[NoticeResponse]:
    service = MiscService(db)
    if current_user.role.name == "STUDENT":
        audience = "STUDENT"
        is_active = True
    return service.list_notices(audience, is_active, skip, limit)


@router.post("", response_model=NoticeResponse, status_code=status.HTTP_201_CREATED)
def create_notice(
    payload: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NoticeResponse:
    service = MiscService(db)
    return service.create_notice({**payload.model_dump(), "created_by": current_user.id})


@router.get("/{notice_id}", response_model=NoticeResponse)
def get_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN", "STAFF")),
) -> NoticeResponse:
    service = MiscService(db)
    return service.get_notice(notice_id)


@router.put("/{notice_id}", response_model=NoticeResponse)
def update_notice(
    notice_id: int,
    payload: NoticeUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> NoticeResponse:
    service = MiscService(db)
    return service.update_notice(notice_id, payload.model_dump(exclude_unset=True))


@router.delete("/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notice(
    notice_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("ADMIN")),
) -> None:
    service = MiscService(db)
    service.delete_notice(notice_id)
