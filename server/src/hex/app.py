from dataclasses import dataclass
from pathlib import Path

from hex.session import SessionManager
from hex.storage import StorageManager
from hex.user import UserManager


@dataclass
class HexApp:
    storage: StorageManager
    users: UserManager
    sessions: SessionManager


def create_app(storage_path: Path) -> HexApp:
    storage = StorageManager(storage_path)
    users = UserManager(storage)
    sessions = SessionManager(storage, users)

    return HexApp(
        storage=storage,
        users=users,
        sessions=sessions,
    )
