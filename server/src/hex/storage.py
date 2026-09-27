import json
from pathlib import Path


class StorageManager:
    """Manages storage."""

    def __init__(self, base_path: Path):
        self._base_path = base_path

    def save(self, asset_type: str, asset_dict: dict) -> None:
        """Save an asset."""
        asset_id = asset_dict["id"]
        target_path = self._base_path / asset_type / f"{asset_id}.json"
        target_path.parent.mkdir(exist_ok=True, parents=True)
        target_path.write_text(json.dumps(asset_dict))

    def load(self, asset_type: str, asset_id: str) -> dict | None:
        """Load an asset."""
        target_path = self._base_path / asset_type / f"{asset_id}.json"
        if target_path.exists():
            return json.loads(target_path.read_text())
        else:
            return None
