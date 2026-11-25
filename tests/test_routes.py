from pathlib import Path
from httpx import AsyncClient
from fastapwebapp.config import config


def test_storage_directories_created(isolated_storage: Path) -> None:
    assert (isolated_storage / "generated").is_dir()
    assert (isolated_storage / "imageuploads").is_dir()
    assert (isolated_storage / "chat_audio").is_dir()
    assert config.STORAGE_ROOT == isolated_storage


async def test_openapi_schema_loads(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Modern Studio Backend"


async def test_home_view_route(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code in {200, 302, 307}