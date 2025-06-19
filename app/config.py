# app/config.py

import os
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, EmailStr, Field
from typing import List, Optional

class Settings(BaseSettings):
    # Core
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

    # Read the database URL from DATABASE_URL (won’t error if missing)
    SQLALCHEMY_DATABASE_URI: Optional[str] = Field(
        None,
        env="DATABASE_URL"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def GEMINI_MODEL_URL(self) -> str:
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set")
        return (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={self.GEMINI_API_KEY}"
        )

# Instantiate settings (no Pydantic ValidationError on import)
settings = Settings()

# Now enforce at runtime that the DB URL is present
if not settings.SQLALCHEMY_DATABASE_URI:
    raise RuntimeError(
        "Missing DATABASE_URL environment variable—"
        "please set your Postgres connection string as DATABASE_URL."
    )
