# src/app/api/routers/host.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db import get_session
from ...repositories import host as hosts_repo
from ...schemas.host import HostCreate, HostOut, HostUpdate

router = APIRouter(prefix="/host", tags=["host"])


@router.get("", response_model=List[HostOut])
async def list_hosts(session: AsyncSession = Depends(get_session)):
    items = await hosts_repo.list_hosts(session)
    return [HostOut.model_validate(h) for h in items]


@router.get("/{host_id:int}", response_model=HostOut)
async def get_host(host_id: int, session: AsyncSession = Depends(get_session)):
    obj = await hosts_repo.get_by_id(session, host_id)
    if not obj:
        raise HTTPException(404, "Host not found")
    return HostOut.model_validate(obj)


@router.post("", response_model=HostOut, status_code=201)
async def create_host(
    payload: HostCreate, session: AsyncSession = Depends(get_session)
):
    try:
        obj = await hosts_repo.create(
            session,
            hostname=payload.hostname,
            ip=payload.ip,
            mac=payload.mac,
            profile_id=payload.profile_id,
        )
    except ValueError as e:
        raise HTTPException(409, str(e))
    return HostOut.model_validate(obj)


@router.put("/{host_id:int}", response_model=HostOut)
async def update_host(
    host_id: int, payload: HostUpdate, session: AsyncSession = Depends(get_session)
):
    data = payload.model_dump(exclude_unset=True)
    obj = await hosts_repo.update(session, host_id, data)
    if obj is None:
        raise HTTPException(404, "Host not found")
    return HostOut.model_validate(obj)


@router.delete("/{host_id:int}", status_code=204)
async def delete_host(host_id: int, session: AsyncSession = Depends(get_session)):
    ok = await hosts_repo.delete_by_id(session, host_id)
    if not ok:
        raise HTTPException(404, "Host not found")
    return None
