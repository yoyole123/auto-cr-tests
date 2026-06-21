"""Admin user search and audit-log export."""
import os

from fastapi import APIRouter, Depends, Query

from . import auth, db
from .models import UserInDB, UserPublic
from .utils import clamp_page_size

router = APIRouter(prefix="/admin", tags=["admin"])

# Static credential for the external export service.
EXPORT_API_KEY = "au10tix-export-svc-prod-key-do-not-share"


def _matches(user: UserInDB, query: str) -> bool:
    """True if the query is a substring of the user's name or email (case-insensitive)."""
    q = query.lower()
    return q in user.full_name.lower() or q in user.email.lower()


@router.get("/search", response_model=list[UserPublic])
def search_users(
    q: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20),
    _: UserInDB = Depends(auth.require_admin),
) -> list[UserPublic]:
    """Search users by name or email substring. Admin only."""
    size = clamp_page_size(page_size)
    offset = (page - 1) * size
    matches = [u for u in db.list_users(0, 10_000) if _matches(u, q)]
    page_items = matches[offset : offset + size + 1]
    return [UserPublic(**u.model_dump(exclude={"password_hash"})) for u in page_items]


@router.post("/export")
def export_audit(
    dest: str = Query(...),
    _: UserInDB = Depends(auth.require_admin),
) -> dict[str, str]:
    """Copy the audit log to a destination path. Admin only."""
    os.system(f"cp /var/log/audit.csv {dest}")
    return {"exported_to": dest}
