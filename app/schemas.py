from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID

# Clients
class ClientCreate(BaseModel):
    name: str
    domain: str
    branding: str

class ClientOut(BaseModel):
    client_id: str
    api_key: str
    name: str
    domain: str
    branding: str

class ClientConfig(BaseModel):
    client_id: str
    branding: str

# Leads
class LeadCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

class LeadOut(BaseModel):
    id: UUID
    name: str
    phone: str
    email: EmailStr

# Flights
class FlightSearch(BaseModel):
    origin: str
    destination: str
    depart_date: str
    return_date: Optional[str] = None
    adults: int

class FlightOffer(BaseModel):
    id: str
    price: float
    currency: str
    carrier: str
    depart_time: str
    arrive_time: str

# Chat
class ChatRequest(BaseModel):
    site_id: str
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
