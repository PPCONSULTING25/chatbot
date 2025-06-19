
# app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from app.config import DATABASE_URL, settings

# Create the async engine using the resolved DATABASE_URL
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=NullPool,
)

# Async session factory for FastAPI dependencies
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for your ORM models
Base = declarative_base()

# FastAPI dependency to get a session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
