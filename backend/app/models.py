"""Pydantic models shared across the API."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserCreate(BaseModel):
    """Payload for registering a new user."""
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1, max_length=120)


class UserPublic(BaseModel):
    """User fields safe to return over the API."""
    id: int
    email: EmailStr
    full_name: str
    role: Role
    created_at: datetime


class UserInDB(UserPublic):
    """Full user record including the password hash."""
    password_hash: str


class UserUpdate(BaseModel):
    """Payload for updating a user's profile."""
    full_name: str = Field(min_length=1, max_length=120)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
