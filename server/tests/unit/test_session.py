from datetime import datetime
from unittest.mock import MagicMock

import pytest
from hex.session import InvalidLoginException, SessionManager


def test_create_with_invalid_login():
    # Arrange.
    storage_manager = MagicMock()
    user_manager = MagicMock()
    user_manager.authenticate.return_value = False
    session_manager = SessionManager(storage_manager, user_manager)

    # Act, Assert.
    with pytest.raises(InvalidLoginException):
        session_manager.create_session("non-existant-username", "password")


def test_create_session_with_valid_login():
    # Arrange.
    storage_manager = MagicMock()
    user_manager = MagicMock()
    user_manager.authenticate.return_value = True
    session_manager = SessionManager(storage_manager, user_manager)
    session_manager.get_current_timestamp = MagicMock()
    session_manager.get_current_timestamp.return_value = "test-timestamp"

    # Act.
    session_id = session_manager.create_session("valid-username", "password")

    # Assert.
    storage_manager.save.assert_called_with(
        "sessions",
        {
            "id": session_id,
            "username": "valid-username",
            "created_at": "test-timestamp",
        },
    )


def test_generate_session_id():
    # Arrange.
    session_manager = SessionManager(MagicMock(), MagicMock())

    # Act.
    session_id = session_manager.generate_session_id()

    # Assert.
    assert len(session_id) == 8


def test_get_current_timestamp():
    # Arrange.
    session_manager = SessionManager(MagicMock(), MagicMock())

    # Act.
    timestamp = session_manager.get_current_timestamp()

    # Assert.
    assert datetime.fromisoformat(timestamp)
