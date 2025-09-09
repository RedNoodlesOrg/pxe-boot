from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.db import get_session
from app.models.host import HostORM
from app.repositories.profile_fs import read_profile_ignition
from sqlalchemy import select

router = APIRouter(tags=["boot"])

@router.get("/ignition")
async def get_ignition(
    profile_id: int | None = Query(default=None),
    profile: str | None = Query(default=None, deprecated=True),
):
    if profile_id is None and profile is not None:
        return Response(
            content=_read_ign_by_name(profile),
            media_type="application/json",
        )
    if profile_id is None:
        raise HTTPException(400, "Provide profile_id")
    return Response(content=read_profile_ignition(profile_id), media_type="application/json")

def _read_ign_by_name(name: str) -> str:
    from app.repositories.profile_fs import _iter_profiles, read_profile_ignition
    candidates = [pid for (pid, n, _) in _iter_profiles() if n == name]
    if not candidates:
        raise HTTPException(404, "Profile not found")
    return read_profile_ignition(max(candidates))

@router.get("/ignition/{host_id:int}")
async def get_ignition_by_host(host_id: int, session: AsyncSession = Depends(get_session)):
    host = await session.get(HostORM, host_id)
    if not host:
        raise HTTPException(404, "Host not found")
    return Response(content=read_profile_ignition(host.profile_id), media_type="application/json")

@router.get("/ipxe")
async def get_ipxe(host_id: int | None = None):
    ign_url = (
        f"{settings.ignition_base_url}/ignition/{host_id}"
        if host_id is not None
        else f"{settings.ignition_base_url}/ignition?profile_id=${{hostname}}"
    )
    script = f"""#!ipxe
set version {settings.fcos_version}
set base {settings.pxe_base_url}/${{version}}

kernel ${{base}}/fedora-coreos-${{version}}-live-kernel-x86_64 \
    coreos.live.rootfs_url=${{base}}/fedora-coreos-${{version}}-live-rootfs.x86_64.img \
    ignition.firstboot ignition.platform.id=metal \
    rd.neednet=1 ip=dhcp \
    ignition.config.url={ign_url}
initrd ${{base}}/fedora-coreos-${{version}}-live-initramfs.x86_64.img
boot
"""
    return Response(content=script, media_type="text/plain")
