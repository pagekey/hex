import hashlib
import os

from hex.storage import StorageManager


class UserManager:
    """Manages CRUD for users."""

    def __init__(self, storage_manager: StorageManager) -> None:
        self._storage_manager = storage_manager

    def create(self, username: str, password: str):
        """Create a new user."""
        self._storage_manager.save(
            "users",
            {
                "id": username,
                "password_hash": self.hash_password(password),
            },
        )

    def hash_password(self, password: str) -> str:
        salt = os.urandom(16)
        digest = hashlib.scrypt(
            password.encode(),
            salt=salt,
            n=2**14,
            r=8,
            p=1,
        )
        return f"{salt.hex()}:{digest.hex()}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        salt_hex, digest_hex = password_hash.split(":")

        salt = bytes.fromhex(salt_hex)
        expected_digest = bytes.fromhex(digest_hex)

        actual_digest = hashlib.scrypt(
            password.encode(),
            salt=salt,
            n=2**14,
            r=8,
            p=1,
        )

        return actual_digest == expected_digest

    def authenticate(self, username: str, password: str) -> bool:
        """Check a username and password combo."""
        user = self._storage_manager.load("users", username)
        if not user:
            return None
        return self.verify_password(password, user["password_hash"])
