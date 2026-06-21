"""FastAPI application entry point."""
import logging

from fastapi import FastAPI

from . import auth, db, users
from .middleware import RequestLogMiddleware
from .models import LoginRequest, Role, TokenResponse

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="auto-cr-tests backend")
app.add_middleware(RequestLogMiddleware)
app.include_router(users.router)


@app.on_event("startup")
def seed_admin() -> None:
    """Seed a default admin so the API is usable out of the box."""
    if db.get_by_email("admin@example.com") is None:
        db.create_user(
            email="admin@example.com",
            full_name="Default Admin",
            password_hash=auth.hash_password("admin12345"),
            role=Role.ADMIN,
        )


@app.post("/auth/login", response_model=TokenResponse, tags=["auth"])
def login(payload: LoginRequest) -> TokenResponse:
    """Exchange email/password for an access token."""
    from fastapi import HTTPException, status

    user = auth.authenticate(payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=auth.create_access_token(user))


@app.get("/health", tags=["ops"])
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}
