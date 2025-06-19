# app/config.py

import os
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from pydantic_settings import BaseSettings
from pydantic import EmailStr
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "Vacation Vista Chatbot"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["*"]

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

# Resolve the raw URL from env
raw_url = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URI")
if not raw_url:
    raise RuntimeError(
        "Missing DATABASE_URL—set your Postgres connection string as DATABASE_URL"
    )

# Parse and strip sslmode, then ensure asyncpg scheme
parsed = urlparse(raw_url)
# Filter out sslmode query param
query_params = [(k, v) for k, v in parse_qsl(parsed.query) if k.lower() != 'sslmode']
new_query = urlencode(query_params)

# Rebuild URL with new query
scheme = parsed.scheme
if scheme.startswith('postgresql') and '+asyncpg' not in scheme:
    scheme = scheme.replace('postgresql', 'postgresql+asyncpg', 1)

clean_url = urlunparse((
    scheme,
    parsed.netloc,
    parsed.path,
    parsed.params,
    new_query,
    parsed.fragment
))

print(f"🌐 Using cleaned DATABASE_URL: {clean_url}")

# Final DB connection string
DATABASE_URL = clean_url

