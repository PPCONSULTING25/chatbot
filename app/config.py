# app/config.py

import os
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, EmailStr
from typing import List, Optional

class Settings(BaseSettings):
    # Core application settings
    APP_NAME: str = "Vacation Vista Chatbot"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["*"]

    # Optional service keys until you wire them up
    DUFFEL_API_KEY: Optional[str]      = None
    GEMINI_API_KEY: Optional[str]      = None

    SMTP_HOST:       Optional[str]     = None
    SMTP_PORT:       Optional[int]     = None
    SMTP_USER:       Optional[str]     = None
    SMTP_PASS:       Optional[str]     = None
    SENDER_EMAIL:    Optional[EmailStr]= None

    pinecone_api_key: Optional[str]    = None
    pinecone_environment: Optional[str]= None
    pinecone_index: Optional[str]      = None

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instantiate base settings
settings = Settings()

# Resolve DATABASE_URL (Postgres) or fall back to scratch SQLite
_db_url = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URI")
if _db_url:
    # Ensure asyncpg driver if using Postgres
    if _db_url.startswith("postgresql://") and "+asyncpg" not in _db_url:
        _db_url = _db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    print(f"🌐 Using DATABASE_URL: {_db_url}")
else:
    # Writable scratch space (ephemeral) for serverless
    _db_url = "sqlite+aiosqlite:////tmp/chatbot.db"
    print(f"⚠️ No DATABASE_URL found—falling back to: {_db_url}")

# Final DB connection string
DATABASE_URL = _db_url
