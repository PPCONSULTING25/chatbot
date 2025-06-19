# api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from app.config import settings, DATABASE_URL
from app.database import engine, Base
from app.routers.clients import router as clients_router
from app.routers.chat    import router as chat_router
from app.routers.flights import router as flights_router
from app.routers.leads   import router as leads_router

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount all routers under /api/*
app.include_router(clients_router, prefix="/api/clients")
app.include_router(chat_router,    prefix="/api/chat")
app.include_router(flights_router, prefix="/api/flights")
app.include_router(leads_router,   prefix="/api/leads")

@app.on_event("startup")
async def startup_event():
    # 1) Synchronous table creation using psycopg2
    sync_url = DATABASE_URL.replace("+asyncpg", "")
    sync_engine = create_engine(sync_url, echo=False)
    Base.metadata.create_all(bind=sync_engine)

    # 2) Async ensure tables exist (no-op if already created)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
