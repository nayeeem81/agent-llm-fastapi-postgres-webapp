# Modern Studio Backend (`fastapwebapp`)

A full-stack **FastAPI + PostgreSQL + AI/Audio Studio** web application supporting text-to-speech, audio segmentation, image-to-text processing, and interactive chatbot workflows.

---

## Key Features

* **Speech Synthesis & Audio DSP:** Real-time text-to-speech (`gTTS`), word-level segmentation (`pydub` + FFmpeg), pitch/frequency adjustments, and timeline JSONB persistence.
* **AI & Computer Vision Workflows:** Integrated Google GenAI (`google-genai`) chatbot and image-processing pipelines.
* **Async PostgreSQL Persistence:** Powered by `SQLModel`, `SQLAlchemy[asyncio]`, and `asyncpg` with automatic schema bootstrapping.
* **Full-Stack Web UI & REST API:** Server-rendered Jinja2 HTML templates paired with modular FastAPI endpoints and WaveSurfer.js audio controls.
* **Modern Python Tooling:** Standard `src/` layout managed via `pyproject.toml` and `uv`, with async `pytest` transaction-rollback tests and multi-container Docker Compose support.

---

## Project Structure

```text
agent-llm-fastapi-postgres-webapp/
├── pyproject.toml               # Package metadata, dependencies, and pytest config
├── uv.lock                      # Locked dependency versions
├── Dockerfile                   # Python 3.13 + FFmpeg container build
├── docker-compose.yml           # FastAPI backend + PostgreSQL 16 services
├── .env.example                 # Environment variable template
├── src/
│   └── fastapwebapp/
│       ├── main.py              # FastAPI app initialization, lifespan & static mounts
│       ├── config.py            # Environment settings & storage path configuration
│       ├── api/                 # Feature-specific API sub-routers
│       ├── data/                # Database engines & SQLModel ORM tables
│       ├── routers/             # REST API and HTML Jinja2 page routes
│       ├── utils/               # Shared helper modules (image & audio processing)
│       ├── templates/           # Jinja2 HTML templates
│       └── static/              # CSS, JavaScript, WaveSurfer, and media assets
└── tests/                       # Async pytest suite & conftest fixtures
```

---

## Quick Start & Usage

1. **Configure Environment:** Copy `.env.example` to `.env` and set your `GEMINI_API_KEY` and database credentials.
2. **Install Dependencies:** Run `uv sync` to install the editable package and lockfile dependencies.
3. **Run FastAPI Server:** Start the application locally via `uv run uvicorn fastapwebapp.main:app --reload` (Web UI at `http://127.0.0.1:8000`, Docs at `http://127.0.0`).
4. **Docker Compose:** Spin up containers using `docker compose up -d --build`.
5. **Run Tests:** Execute the test suite using `uv run pytest -v`.
