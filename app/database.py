
# app/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine as create_sync_engine

from app.config import DATABASE_URL, settings

# Base class for ORM models
Base = declarative_base()

# Import models so Base.metadata includes all table definitions
import app.models  # noqa: F401

# 1) Synchronous table creation at import-time (requires psycopg2-binary)
sync_url = DATABASE_URL.replace("+asyncpg", "")
sync_engine = create_sync_engine(sync_url, echo=False)
Base.metadata.create_all(bind=sync_engine)

# 2) Async engine for runtime
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=NullPool,
)

# Session factory for FastAPI dependencies
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
