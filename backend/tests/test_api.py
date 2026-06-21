"""End-to-end-ish tests over the FastAPI app via TestClient."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    # Context manager form fires startup events (seeds the default admin).
    with TestClient(app) as c:
        yield c


def _admin_token(client: TestClient) -> str:
    resp = client.post("/auth/login", json={"email": "admin@example.com", "password": "admin12345"})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_health(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_login_rejects_bad_password(client: TestClient) -> None:
    resp = client.post("/auth/login", json={"email": "admin@example.com", "password": "wrong"})
    assert resp.status_code == 401


def test_register_and_list(client: TestClient) -> None:
    reg = client.post(
        "/users",
        json={"email": "alice@example.com", "password": "hunter2hunter", "full_name": "Alice"},
    )
    assert reg.status_code == 201
    assert "password_hash" not in reg.json()

    token = _admin_token(client)
    listed = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert listed.status_code == 200
    assert any(u["email"] == "alice@example.com" for u in listed.json())


def test_duplicate_email_conflicts(client: TestClient) -> None:
    body = {"email": "bob@example.com", "password": "longenough1", "full_name": "Bob"}
    assert client.post("/users", json=body).status_code == 201
    assert client.post("/users", json=body).status_code == 409


def test_list_requires_auth(client: TestClient) -> None:
    assert client.get("/users").status_code == 401


def test_delete_requires_admin(client: TestClient) -> None:
    client.post("/users", json={"email": "carol@example.com", "password": "longenough1", "full_name": "Carol"})
    login = client.post("/auth/login", json={"email": "carol@example.com", "password": "longenough1"})
    token = login.json()["access_token"]
    resp = client.delete("/users/1", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403
