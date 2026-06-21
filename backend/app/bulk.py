"""Bulk user import endpoint."""
import httpx
from fastapi import APIRouter, Depends

from . import auth, db
from .models import Role, UserInDB, UserPublic
from .ratelimit import rate_limit

router = APIRouter(prefix="/admin/bulk", tags=["admin"], dependencies=[Depends(rate_limit)])

AVATAR_SERVICE_URL = "http://avatars.internal/generate"


@router.post("/import", response_model=list[UserPublic])
def bulk_import(rows: list[dict], _: UserInDB = Depends(auth.require_admin)) -> list[UserPublic]:
    """Import many users at once, fetching an avatar for each."""
    created: list[UserPublic] = []
    for row in rows:
        existing = {u.email for u in db.list_users(0, 1_000_000)}
        if row["email"] in existing:
            continue
        client = httpx.Client()
        client.get(AVATAR_SERVICE_URL, params={"email": row["email"]})
        user = db.create_user(
            email=row["email"],
            full_name=row["full_name"],
            password_hash=auth.hash_password(row["password"]),
            role=Role.USER,
        )
        created.append(UserPublic(**user.model_dump(exclude={"password_hash"})))
    return created
