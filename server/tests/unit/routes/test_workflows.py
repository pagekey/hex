from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from hex.routes.workflows import create_router


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

    client = TestClient(app)

    return client, session_manager, storage_manager, user_manager


def test_list_workflows_not_logged_in():
    # Arrange.
    client, session_manager, _, _ = create_test_client()

    # Act.
    response = client.get("/api/workflows")

    # Assert.
    assert response.status_code == 401
    assert response.json() == {"message": "Not logged in"}
    session_manager.get_session_username.assert_not_called()


def test_list_workflows_invalid_session():
    # Arrange.
    client, session_manager, _, _ = create_test_client()
    session_manager.get_session_username.return_value = None
    client.cookies.set("session_id", "invalid-session")

    # Act.
    response = client.get("/api/workflows")

    # Assert.
    assert response.status_code == 401
    assert response.json() == {"message": "Not logged in"}
    session_manager.get_session_username.assert_called_once_with("invalid-session")


def test_list_workflows():
    # Arrange.
    client, session_manager, storage_manager, _ = create_test_client()
    session_manager.get_session_username.return_value = "me"
    storage_manager.load_many.return_value = [
        {
            "id": "workflow1",
            "username": "me",
            "operations": [],
        }
    ]
    client.cookies.set("session_id", "valid-session")

    # Act.
    response = client.get("/api/workflows")

    # Assert.
    assert response.status_code == 200
    assert response.json() == storage_manager.load_many.return_value
    storage_manager.load_many.assert_called_once_with("workflows")


def test_create_workflow():
    # Arrange.
    client, session_manager, storage_manager, _ = create_test_client()
    session_manager.get_session_username.return_value = "me"
    client.cookies.set("session_id", "valid-session")
    workflow = {
        "id": "workflow1",
        "operations": [
            {
                "name": "hello",
                "command": "echo hello",
            }
        ],
    }

    # Act.
    response = client.post("/api/workflows", json=workflow)

    # Assert.
    assert response.status_code == 200
    assert response.json() == {"message": "Created workflow workflow1"}
    storage_manager.save.assert_called_once()


def test_create_workflow_not_logged_in():
    # Arrange.
    client, _, storage_manager, _ = create_test_client()

    # Act.
    response = client.post(
        "/api/workflows",
        json={
            "id": "workflow1",
            "operations": [],
        },
    )

    # Assert.
    assert response.status_code == 401
    assert response.json() == {"message": "Not logged in"}
    storage_manager.save.assert_not_called()


def test_run_workflow_not_found():
    # Arrange.
    client, session_manager, storage_manager, _ = create_test_client()
    session_manager.get_session_username.return_value = "me"
    storage_manager.load.return_value = None
    client.cookies.set("session_id", "valid-session")

    # Act.
    response = client.post("/api/workflows/run", json={"id": "does-not-exist"})

    # Assert.
    assert response.status_code == 404
    assert response.json() == {"message": "Workflow does-not-exist not found"}


def test_run_workflow():
    # Arrange.
    client, session_manager, storage_manager, _ = create_test_client()
    session_manager.get_session_username.return_value = "me"
    storage_manager.load.return_value = {
        "id": "workflow1",
        "username": "me",
        "operations": [],
    }
    client.cookies.set("session_id", "valid-session")
    execution = MagicMock()
    execution.model_dump.return_value = {
        "workflow_id": "workflow1",
    }

    # Act.
    with patch(
        "hex.routes.workflows.execute_workflow",
        return_value=execution,
    ) as execute:
        response = client.post("/api/workflows/run", json={"id": "workflow1"})

    # Assert.
    assert response.status_code == 200
    assert response.json() == {"execution": {"workflow_id": "workflow1"}}
    storage_manager.load.assert_called_once_with("workflows", "workflow1")
    execute.assert_called_once()


def test_run_workflow_not_logged_in():
    # Arrange.
    client, _, storage_manager, _ = create_test_client()

    # Act.
    response = client.post(
        "/api/workflows/run",
        json={"id": "workflow1"},
    )

    # Assert.
    assert response.status_code == 401
    assert response.json() == {"message": "Not logged in"}
    storage_manager.load.assert_not_called()
