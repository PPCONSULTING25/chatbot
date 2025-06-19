# app/config.py

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, EmailStr, Field
from typing import List, Optional

class Settings(BaseSettings):
    # Core
    APP_NAME: str = "Vacation Vista Chatbot"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["*"]

    # Service keys (made optional until you need each feature)
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

    # Database: required, sourced from DATABASE_URL
    SQLALCHEMY_DATABASE_URI: str = Field(..., env="DATABASE_URL")

    class Config:
        # load any `.env` in your repo root for local dev
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

# Instantiate, validating DATABASE_URL is present
settings = Settings()
