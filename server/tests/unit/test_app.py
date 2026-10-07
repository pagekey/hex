from hex.app import create_app
from hex.session import SessionManager
from hex.storage import StorageManager
from hex.user import UserManager


def test_create_app(tmp_path):
    # Arrange, Act.
    app = create_app(tmp_path)

    # Assert.
    assert isinstance(app.storage, StorageManager)
    assert isinstance(app.users, UserManager)
    assert isinstance(app.sessions, SessionManager)
