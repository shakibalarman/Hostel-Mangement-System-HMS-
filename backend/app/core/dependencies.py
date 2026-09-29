from __future__ import annotations

from typing import Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import TokenError, decode_access_token
from app.models.user import User
from app.services.auth import AuthService

_bearer = HTTPBearer(auto_error=False)


def get_token_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    """Decode the incoming Bearer token into claims (no database access)."""
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return decode_access_token(credentials.credentials)
    except TokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def require_roles(*roles: str) -> Callable:
    """Factory: dependency that allows only the listed application roles."""

    allowed = {role.upper() for role in roles}

    def dependency(payload: dict = Depends(get_token_payload)) -> dict:
        role = str(payload.get("role", "")).upper()
        if role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return payload

    return dependency


def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the authenticated user from the database."""
    service = AuthService(db)
    return service.get_current_user(int(payload["sub"]))


def get_pagination_params(
    page: int = 1,
    size: int = 20,
) -> dict:
    """Standard pagination query parameters (1-indexed)."""
    return {"page": max(page, 1), "size": min(max(size, 1), 100)}


def db_session(db: Session = Depends(get_db)) -> Session:
    return db


def request_client(request: Request) -> Request:
    return request
