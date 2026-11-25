import os
import shutil
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from starlette.middleware.sessions import SessionMiddleware

from fastapwebapp.config import config
from fastapwebapp.data.database import engine
# Keep all structural model types anchored so SQLModel.metadata.create_all creates every table
from fastapwebapp.data.model import (
    AudioChapter,
    Chapter,
    ChatSession,
    ImageMetadata,
    Sentence,
    SentenceHistory,
    Story,
    Word,
    WordHistory,
)
from fastapwebapp.routers.api_routes import api_router
from fastapwebapp.routers.view_routes import view_router

# ==========================================================================
# 1. ENVIRONMENT CONFIGURATION & PATH ANCHORS
# ==========================================================================
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Configure FFmpeg environment paths
if os.name == "nt":
    ffmpeg_path = r"C:\ffmpeg\bin"
    if ffmpeg_path not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]
    try:
        import pydub
        pydub.AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
        pydub.AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
    except ImportError:
        pass
else:
    try:
        import pydub
        pydub.AudioSegment.converter = shutil.which("ffmpeg") or "ffmpeg"
        pydub.AudioSegment.ffprobe = shutil.which("ffprobe") or "ffprobe"
    except ImportError:
        pass


# ==========================================================================
# 2. D: DRIVE STORAGE CONTEXT REGISTRATION
# ==========================================================================
GENERATED_DIR = os.path.normpath(os.path.join(config.STORAGE_ROOT, "generated"))
IMAGE_TEXT_DIR = os.path.normpath(os.path.join(config.STORAGE_ROOT, "imageuploads"))
CHAT_AUDIO_DIR = os.path.normpath(os.path.join(config.STORAGE_ROOT, "chat_audio"))

os.makedirs(IMAGE_TEXT_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(CHAT_AUDIO_DIR, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================================
# 3. LIFECYCLE MANAGEMENT (LIFESPAN PROVISIONS)
# ==========================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    admin_url = (
        f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
        f"@{config.DB_HOST}:{config.DB_PORT}/postgres"
    )
    temp_engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")

    async with temp_engine.connect() as conn:
        query = text(f"SELECT 1 FROM pg_database WHERE datname='{config.DB_NAME}'")
        result = await conn.execute(query)
        if not result.scalar():
            await conn.execute(text(f"CREATE DATABASE {config.DB_NAME}"))
            print(f"Database '{config.DB_NAME}' verified and initialized successfully.")

    await temp_engine.dispose()

    print("Verifying structural tables exist inside PostgreSQL...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Tables sync complete.")

    yield

    print("Shutting down application... disposing connections.")
    await engine.dispose()


# ==========================================================================
# 4. APPLICATION INITIALIZATION & ROUTING MAPS
# ==========================================================================
app = FastAPI(title="Modern Studio Backend", lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=config.SECRET_KEY,
)

# Mount external storage folders onto URL path aliases
app.mount("/project/generated", StaticFiles(directory=GENERATED_DIR), name="d-drive-media")
app.mount("/imageuploads", StaticFiles(directory=IMAGE_TEXT_DIR), name="d-drive-imagetext")

# Mount package static folder (src/fastapwebapp/static)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Core Router Blocks
app.include_router(view_router)
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapwebapp.main:app", host="127.0.0.1", port=8000, reload=True)
