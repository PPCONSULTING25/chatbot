from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import get_db, engine, Base
from app.routers import clients, leads, flights, chat

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include v1 routers
app.include_router(clients.router)
app.include_router(leads.router)
app.include_router(flights.router)
app.include_router(chat.router)

@app.on_event("startup")
async def startup():
    # ensure tables exist
    import app.database  # this triggers sync create_all
    # async tables already created in database.py sync step
    pass
