from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db import get_session
from ...repositories.host import get_by_id, get_by_mac
from ...repositories.profile_fs import read_profile_ignition

router = APIRouter(prefix="/boot", tags=["boot"])


@router.get("/ignition")
async def get_ignition(
    profile_id: int | None = Query(default=None),
    mac: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    if profile_id:
        return Response(
            content=read_profile_ignition(profile_id), media_type="application/json"
        )
    if mac:
        obj = await get_by_mac(session, mac)
        if not obj:
            # TODO Return default ignition instead
            raise HTTPException(404, "Host not found")
        return Response(
            content=read_profile_ignition(obj.profile_id), media_type="application/json"
        )
    raise HTTPException(400, "Provide profile_id or host_mac")


@router.get("/ignition/{host_id:int}")
async def get_ignition_by_host(
    host_id: int, session: AsyncSession = Depends(get_session)
):
    host = await get_by_id(session, host_id)
    if not host:
        raise HTTPException(404, "Host not found")
    return Response(
        content=read_profile_ignition(host.profile_id), media_type="application/json"
    )


@router.get("/kernel")
async def get_kernel():
    pass


@router.get("/rootfs")
async def get_rootfs():
    pass


@router.get("/initramfs")
async def get_initramfs():
    pass
