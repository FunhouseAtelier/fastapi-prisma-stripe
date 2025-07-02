# app/utils/envars.py

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")


def get_envar(key: str, default: str | None = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Missing required env var: {key}")
    return value


ENV_MODE = get_envar("ENV_MODE", "production")
DATABASE_URL = get_envar("DATABASE_URL", "")
SESSION_SECRET = get_envar("SESSION_SECRET", "")
