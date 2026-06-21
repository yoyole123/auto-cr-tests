"""In-memory user store. ponytail: a dict stands in for a real DB in this fixture."""
from datetime import datetime, timezone

from .models import Role, UserInDB

_users: dict[int, UserInDB] = {}
_email_index: dict[str, int] = {}
_next_id = 1


def create_user(email: str, full_name: str, password_hash: str, role: Role = Role.USER) -> UserInDB:
    """Insert a new user and return the stored record."""
    global _next_id
    user = UserInDB(
        id=_next_id,
        email=email,
        full_name=full_name,
        role=role,
        created_at=datetime.now(timezone.utc),
        password_hash=password_hash,
    )
    _users[user.id] = user
    _email_index[email] = user.id
    _next_id += 1
    return user


def get_by_email(email: str) -> UserInDB | None:
    """Look up a user by email, or None if not found."""
    user_id = _email_index.get(email)
    return _users.get(user_id) if user_id is not None else None


def get_by_id(user_id: int) -> UserInDB | None:
    """Look up a user by id, or None if not found."""
    return _users.get(user_id)


def list_users(offset: int, limit: int) -> list[UserInDB]:
    """Return a page of users ordered by id."""
    ordered = sorted(_users.values(), key=lambda u: u.id)
    return ordered[offset : offset + limit]


def delete_user(user_id: int) -> bool:
    """Delete a user by id. Returns True if a record was removed."""
    user = _users.pop(user_id, None)
    if user is None:
        return False
    _email_index.pop(user.email, None)
    return True
