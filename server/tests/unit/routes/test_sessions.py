from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from hex.routes.sessions import create_router


def create_test_client():
    session_manager = MagicMock()
    storage_manager = MagicMock()
    user_manager = MagicMock()

    app = FastAPI()
    app.include_router(
        create_router(
            session_manager,
            storage_manager,
            user_manager,
        )
    )

    return (
        TestClient(app),
        session_manager,
        storage_manager,
        user_manager,
    )


def test_home():
    client, _, _, _ = create_test_client()

    response = client.get("/api/sessions")

    assert response.status_code == 200
    assert response.json() == "Hello from sessions"


def test_seed_creates_admin():
    client, _, storage_manager, user_manager = create_test_client()
    storage_manager.load.return_value = None

    response = client.post("/api/sessions/seed")

    assert response.status_code == 200
    assert response.json() == "Created admin user"
    storage_manager.load.assert_called_once_with("users", "admin")
    user_manager.create.assert_called_once_with("admin", "admin123456")


def test_seed_when_admin_exists():
    client, _, storage_manager, user_manager = create_test_client()
    storage_manager.load.return_value = {"id": "admin"}

    response = client.post("/api/sessions/seed")

    assert response.status_code == 200
    assert response.json() == "Admin user exists already"
    user_manager.create.assert_not_called()


def test_create_session():
    client, session_manager, _, _ = create_test_client()
    session_manager.create_session.return_value = "abc123"

    response = client.post(
        "/api/sessions",
        json={
            "username": "steve",
            "password": "password",
        },
    )

    assert response.status_code == 201
    assert response.json() == {"message": "Session created"}
    assert response.cookies["session_id"] == "abc123"
    session_manager.create_session.assert_called_once_with(
        "steve",
        "password",
    )


def test_create_session_invalid_login():
    from hex.session import InvalidLoginException

    client, session_manager, _, _ = create_test_client()
    session_manager.create_session.side_effect = InvalidLoginException()

    response = client.post(
        "/api/sessions",
        json={
            "username": "steve",
            "password": "wrong",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"message": "Invalid username or password"}


def test_check_session_not_authenticated():
    client, _, _, _ = create_test_client()

    response = client.get("/api/sessions/check")

    assert response.status_code == 200
    assert response.json() == {"authenticated": False}


def test_check_session_invalid():
    client, session_manager, _, _ = create_test_client()
    session_manager.get_session_username.return_value = None
    client.cookies.set("session_id", "invalid")

    response = client.get("/api/sessions/check")

    assert response.status_code == 200
    assert response.json() == {"authenticated": False}
    session_manager.get_session_username.assert_called_once_with("invalid")


def test_check_session_authenticated():
    client, session_manager, _, _ = create_test_client()
    session_manager.get_session_username.return_value = "steve"
    client.cookies.set("session_id", "abc123")

    response = client.get("/api/sessions/check")

    assert response.status_code == 200
    assert response.json() == {
        "authenticated": True,
        "username": "steve",
    }
    session_manager.get_session_username.assert_called_once_with("abc123")


def test_delete_session():
    client, _, _, _ = create_test_client()

    response = client.delete("/api/sessions")

    assert response.status_code == 200
    assert response.json() == {"message": "Session deleted"}

    cookie = response.headers["set-cookie"]
    assert "session_id=" in cookie
    assert "HttpOnly" in cookie
