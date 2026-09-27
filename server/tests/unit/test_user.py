from unittest.mock import MagicMock

from hex.user import UserManager


def test_create_user():
    # Arrange.
    storage_manager = MagicMock()
    user_manager = UserManager(storage_manager)
    user_manager.hash_password = MagicMock()
    user_manager.hash_password.return_value = "hashed"

    # Act.
    user_manager.create("user1", "pass1")

    # Assert.
    storage_manager.save.assert_called_with(
        "users", {"id": "user1", "password_hash": "hashed"}
    )


def test_hash_password():
    # Arrange.
    user_manager = UserManager(MagicMock())
    password = "password123"

    # Act.
    hash = user_manager.hash_password(password)

    # Assert.
    assert hash != password


def test_verify_password():
    # Arrange.
    user_manager = UserManager(MagicMock())
    password = "password123"
    password_hash = user_manager.hash_password(password)

    # Act, Assert.
    assert user_manager.verify_password(password, password_hash)
