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


def test_load_existing_asset(tmp_path: Path):
    # Arrange.
    storage_manager = StorageManager(tmp_path)
    asset = {
        "id": "abc",
        "name": "some workflow",
    }
    storage_manager.save("workflows", asset)

    # Act.
    loaded_asset = storage_manager.load("workflows", "abc")

    # Assert.
    assert loaded_asset == asset


def test_load_many(tmp_path: Path):
    # Arrange.
    storage_manager = StorageManager(tmp_path)
    first = {"id": "1", "name": "first"}
    second = {"id": "2", "name": "second"}
    storage_manager.save("workflows", first)
    storage_manager.save("workflows", second)

    # Act.
    assets = storage_manager.load_many("workflows")

    # Assert.
    assert {a["id"] for a in assets} == {"1", "2"}


def test_load_many_pagination(tmp_path: Path):
    # Arrange.
    storage_manager = StorageManager(tmp_path)
    for i in range(5):
        storage_manager.save("workflows", {"id": str(i)})

    # Act.
    assets = storage_manager.load_many("workflows", limit=2, page=1)

    # Assert.
    assert {a["id"] for a in assets} == {"2", "3"}
