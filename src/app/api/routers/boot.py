from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.config import settings
from ...core.db import get_session
from ...models.host import HostORM
from ...repositories.profile_fs import read_profile_ignition
from ...repositories.host import get_by_mac, get_by_id
from sqlalchemy import select

router = APIRouter(tags=["boot"])

@router.get("/ignition")
async def get_ignition(
    profile_id: int | None = Query(default=None),
    mac: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session)
):
    if profile_id:
        return Response(content=read_profile_ignition(profile_id), media_type="application/json")
    if mac:
        obj = await get_by_mac(session, mac)
        if not obj:
            raise HTTPException(404, "Host not found")
        return Response(content=read_profile_ignition(obj.profile_id), media_type="application/json")
    raise HTTPException(400, "Provide profile_id or host_mac")
    

@router.get("/ignition/{host_id:int}")
async def get_ignition_by_host(host_id: int, session: AsyncSession = Depends(get_session)):
    host = await get_by_id(session,host_id)
    if not host:
        raise HTTPException(404, "Host not found")
    return Response(content=read_profile_ignition(host.profile_id), media_type="application/json")
