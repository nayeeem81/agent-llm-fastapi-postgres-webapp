from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapwebapp.config import config
from fastapwebapp.data.database import get_db
from fastapwebapp.main import app


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect STORAGE_ROOT to a clean temporary folder for every test."""
    monkeypatch.setattr(config, "STORAGE_ROOT", tmp_path)
    (tmp_path / "generated").mkdir(parents=True, exist_ok=True)
    (tmp_path / "imageuploads").mkdir(parents=True, exist_ok=True)
    (tmp_path / "chat_audio").mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional SQLModel AsyncSession that rolls back after each test."""
    test_engine = create_async_engine(config.DATABASE_URL, echo=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with test_engine.connect() as conn:
        transaction = await conn.begin()
        session = AsyncSession(
            bind=conn,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()

    await test_engine.dispose()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP test client wired to override get_db."""
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session
        await db_session.commit()

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()