from pydantic import BaseModel
from typing import Optional, List, Dict
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from .database import Base
from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from .database import Base

# --- Pydantic Models ---

class ChatRequest(BaseModel):
    session_id: str
    site_id: str
    message: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    session_id: str
    reply: str

class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: Optional[str] = None
    adults: int

class FlightOffer(BaseModel):
    id: str
    total_amount: str
    currency: str
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str

# --- SQLAlchemy Model ---

class Lead(Base):
    __tablename__ = "leads"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True, nullable=False)
    name      = Column(String, nullable=False)
    domain    = Column(String, nullable=False)
    branding  = Column(JSON, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )