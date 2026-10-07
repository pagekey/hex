from fastapi import HTTPException
import pytest

from fastapi.testclient import TestClient

from hex.main import SPAStaticFiles, app, get_static_dir


def test_index():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "Hello from Hex server!"


def test_get_static_dir():
    static_dir = get_static_dir()

    assert static_dir.name == "static"
    assert static_dir.is_absolute()


@pytest.mark.anyio
async def test_static_files_falls_back_to_index(tmp_path):
    (tmp_path / "index.html").write_text("<html>Hello</html>")

    static_files = SPAStaticFiles(directory=tmp_path)

    response = await static_files.get_response(
        "some/react/route",
        {"type": "http", "method": "GET"},
    )

    assert response.status_code == 200


@pytest.mark.anyio
async def test_static_files_returns_404_without_index(tmp_path):
    static_files = SPAStaticFiles(directory=tmp_path)

    with pytest.raises(HTTPException) as exc:
        await static_files.get_response(
            "some/react/route",
            {"type": "http", "method": "GET"},
        )

    assert exc.value.status_code == 404


@pytest.mark.anyio
async def test_static_files_dot_serves_index(tmp_path):
    (tmp_path / "index.html").write_text("<html>Hello</html>")
    static_files = SPAStaticFiles(directory=tmp_path)

    response = await static_files.get_response(
        ".",
        {
            "type": "http",
            "method": "GET",
            "headers": [],
        },
    )

    assert response.status_code == 200
