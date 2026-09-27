import secrets
import string
from datetime import datetime, timezone

from hex.storage import StorageManager
from hex.user import UserManager


class InvalidLoginException(Exception):
    """Wrong username/password combo."""


class SessionManager:
    """Manages login sessions."""

    def __init__(
        self, storage_manager: StorageManager, user_manager: UserManager
    ) -> None:
        self._storage_manager = storage_manager
        self._user_manager = user_manager

    def create_session(self, username: str, password: str) -> str:
        """Create a login session if creds are valid."""
        if self._user_manager.authenticate(username, password):
            session_id = self.generate_session_id()
            self._storage_manager.save(
                "sessions",
                {
                    "id": session_id,
                    "username": username,
                    "created_at": self.get_current_timestamp(),
                },
            )
            return session_id
        else:
            raise InvalidLoginException()

    def generate_session_id(self) -> str:
        return "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(8)
        )

    def get_current_timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()
