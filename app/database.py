# app/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine as create_sync_engine
from app.config import DATABASE_URL, settings

# Create the async engine for runtime
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=NullPool,
)

# Create a synchronous engine to auto-create tables on import (for serverless)
sync_url = DATABASE_URL.replace("+asyncpg", "")
sync_engine = create_sync_engine(
    sync_url,
    echo=False,
)

# Base class for your ORM models
Base = declarative_base()

# Ensure all tables exist (runs once at import/cold-start)
Base.metadata.create_all(sync_engine)

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
