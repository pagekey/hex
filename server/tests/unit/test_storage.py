from pathlib import Path

from hex.storage import StorageManager


def test_save_assset(tmp_path: Path):
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
