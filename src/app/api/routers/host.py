from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.core.db import get_session
from app.models.host import HostORM
from app.schemas.host import HostCreate, HostUpdate, HostOut
from app.repositories.profile_fs import get_profile

router = APIRouter(prefix="/host", tags=["host"])

@router.get("", response_model=List[HostOut])
async def list_hosts(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(HostORM))
    return [HostOut.model_validate(h) for h in res.scalars().all()]

@router.get("/{host_id:int}", response_model=HostOut)
async def get_host(host_id: int, session: AsyncSession = Depends(get_session)):
    obj = await session.get(HostORM, host_id)
    if not obj:
        raise HTTPException(404, "Host not found")
    return HostOut.model_validate(obj)

@router.post("", response_model=HostOut, status_code=201)
async def create_host(payload: HostCreate, session: AsyncSession = Depends(get_session)):
    get_profile(payload.profile_id)
    obj = HostORM(hostname=payload.hostname, ip=payload.ip, mac=payload.mac, profile_id=payload.profile_id)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return HostOut.model_validate(obj)

@router.put("/{host_id:int}", response_model=HostOut)
async def update_host(host_id: int, payload: HostUpdate, session: AsyncSession = Depends(get_session)):
    obj = await session.get(HostORM, host_id)
    if not obj:
        raise HTTPException(404, "Host not found")
    data = payload.model_dump(exclude_unset=True)
    if "profile_id" in data:
        get_profile(int(data["profile_id"]))
    for k, v in data.items():
        setattr(obj, k, v)
    await session.commit()
    await session.refresh(obj)
    return HostOut.model_validate(obj)

@router.delete("/{host_id:int}", status_code=204)
async def delete_host(host_id: int, session: AsyncSession = Depends(get_session)):
    res = await session.execute(delete(HostORM).where(HostORM.id == host_id))
    if res.rowcount == 0:
        raise HTTPException(404, "Host not found")
    await session.commit()
    return None
