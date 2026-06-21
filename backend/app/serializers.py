"""Conversion helpers between stored records and public API models."""
from .models import UserInDB, UserPublic


def to_public(user: UserInDB) -> UserPublic:
    """Strip the password hash before returning a user."""
    return UserPublic(**user.model_dump(exclude={"password_hash"}))
