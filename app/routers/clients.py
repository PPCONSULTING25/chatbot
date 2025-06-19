# app/routers/clients.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.models import Client

router = APIRouter(tags=["clients"])

class ClientIn(BaseModel):
    name: str
    domain: str
    branding: dict

@router.post("", status_code=201)
async def create_client(
    data: ClientIn,
    db: AsyncSession = Depends(get_db)
):
    cid = uuid.uuid4().hex[:8]
    await db.execute(
        insert(Client).values(
            client_id=cid,
            name=data.name,
            domain=data.domain,
            branding=data.branding
        )
    )
    await db.commit()
    return {"client_id": cid}

@router.get("{cid}")
async def get_client(
    cid: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Client).where(Client.client_id == cid)
    )
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(404, "Client not found")
    return {
        "client_id": client.client_id,
        "branding": client.branding
    }
