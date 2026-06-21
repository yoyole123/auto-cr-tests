"""Authentication: password hashing, JWT issuance, and the current-user dependency."""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from . import db
from .config import ACCESS_TOKEN_TTL_SECONDS, JWT_ALGORITHM, JWT_SECRET
from .models import Role, UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    """Hash a plaintext password for storage."""
    # bcrypt caps input at 72 bytes; encode and let it hash the rest.
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Check a plaintext password against a stored hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_access_token(user: UserInDB) -> str:
    """Issue a signed JWT for the given user."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role.value,
        "iat": now,
        "exp": now + timedelta(seconds=ACCESS_TOKEN_TTL_SECONDS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def authenticate(email: str, password: str) -> UserInDB | None:
    """Return the user if the email/password pair is valid, else None."""
    user = db.get_by_email(email)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """FastAPI dependency that resolves the authenticated user from a bearer token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise credentials_error

    user = db.get_by_id(user_id)
    if user is None:
        raise credentials_error
    return user


def require_admin(user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """Dependency that allows only admin users through."""
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user
