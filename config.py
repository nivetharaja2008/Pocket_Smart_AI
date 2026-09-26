import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


APP_NAME = os.getenv(
    "APP_NAME",
    "PocketSmart AI"
)
APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-secret-change-me"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)

MAX_UPLOAD_MB = int(
    os.getenv(
        "MAX_UPLOAD_MB",
        "5"
    )
)

DB_PATH = BASE_DIR / "data" / "pocketsmart.db"

UPLOAD_DIR = BASE_DIR / "uploads"