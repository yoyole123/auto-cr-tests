"""User-facing routes: register, list, read, delete."""
from fastapi import APIRouter, Depends, HTTPException, Query, status

from . import auth, db
from .config import DEFAULT_PAGE_SIZE
from .models import Role, UserCreate, UserInDB, UserPublic
from .serializers import to_public as _to_public
from .utils import clamp_page_size, page_bounds

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate) -> UserPublic:
    """Register a new user with the default role."""
    if db.get_by_email(payload.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = db.create_user(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=auth.hash_password(payload.password),
        role=Role.USER,
    )
    return _to_public(user)


@router.get("", response_model=list[UserPublic])
def list_users(
    page: int = Query(1, ge=1),
    page_size: int | None = Query(DEFAULT_PAGE_SIZE),
    _: UserInDB = Depends(auth.get_current_user),
) -> list[UserPublic]:
    """List users, paginated. Requires authentication."""
    size = clamp_page_size(page_size)
    offset, limit = page_bounds(page, size)
    return [_to_public(u) for u in db.list_users(offset, limit)]


@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int, current: UserInDB = Depends(auth.get_current_user)) -> UserPublic:
    """Read a single user. Users may read themselves; admins may read anyone."""
    if current.id != user_id and current.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    user = db.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _to_public(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, _: UserInDB = Depends(auth.require_admin)) -> None:
    """Delete a user. Admin only."""
    if not db.delete_user(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
