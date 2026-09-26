from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import APP_NAME, APP_VERSION
from .db import init_db
from .routes.pages import router as pages_router
from .routes.api import router as api_router


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="PocketSmart AI - Smart Party Planning Assistant",
)
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="pocketsmart-ai-secret-key",
)


# Initialize database
@app.on_event("startup")
async def startup_event():
    init_db()


# Routes
app.include_router(pages_router)
app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": APP_NAME,
        "version": APP_VERSION,
    }