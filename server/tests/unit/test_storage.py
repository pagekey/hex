from pathlib import Path

from hex.storage import StorageManager


def test_save_asset(tmp_path: Path):
    # Arrange.
    storage = StorageManager(tmp_path)
    asset = {
        "id": "abc123",
        "name": "Some Workflow",
    }

    # Act.
    storage.save("workflows", asset)

    # Assert.
    saved_file = tmp_path / "workflows" / "abc123.json"
    assert saved_file.exists()


def test_load_not_exist(tmp_path: Path):
    # Arrange.
    storage_manager = StorageManager(tmp_path)

    # Act.
    asset = storage_manager.load("users", "doesntexist")

    # Assert.
    assert asset is None
