# wow, what terrible practice!
# at least it's all in one place.

from pathlib import Path

from hex.session import SessionManager
from hex.storage import StorageManager
from hex.user import UserManager


storage_manager = StorageManager(
    Path("hexstorage")
)  # TODO figure out how to choose path
user_manager = UserManager(storage_manager)
session_manager = SessionManager(storage_manager, user_manager)
