from __future__ import annotations

from typing import Mapping, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.host import HostORM
from .profile_fs import get_profile


def _normalize_mac(s: str) -> str:
    s = s.strip().lower()
    if "." in s:  # cisco style 5254.00aa.bbcc
        s = s.replace(".", "")
        s = ":".join(s[i : i + 2] for i in range(0, 12, 2))
        return s
    return s.replace("-", ":")


async def list_hosts(session: AsyncSession) -> Sequence[HostORM]:
    res = await session.execute(select(HostORM))
    return res.scalars().all()


async def get_by_id(session: AsyncSession, host_id: int) -> HostORM | None:
    return await session.get(HostORM, host_id)


async def get_by_mac(session: AsyncSession, mac: str) -> HostORM | None:
    mac_n = _normalize_mac(mac)
    res = await session.execute(select(HostORM).where(HostORM.mac == mac_n))
    return res.scalar_one_or_none()


async def create(
    session: AsyncSession, *, hostname: str, ip: str, mac: str, profile_id: int
) -> HostORM:
    get_profile(profile_id)
    obj = HostORM(
        hostname=hostname,
        ip=ip,
        mac=_normalize_mac(mac),
        profile_id=profile_id,
    )
    session.add(obj)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        # surface a clean error; router can translate to HTTP 409
        raise ValueError("Host with same hostname or MAC already exists") from e
    await session.refresh(obj)
    return obj


async def update(
    session: AsyncSession, host_id: int, data: Mapping[str, int | str]
) -> HostORM | None:
    host = await get_by_id(session, host_id)
    if not host:
        return None
    if "profile_id" in data and data["profile_id"] is not None:
        get_profile(int(data["profile_id"]))
    if "mac" in data and data["mac"] is not None:
        data = dict(data)
        data["mac"] = _normalize_mac(str(data["mac"]))
    for k, v in data.items():
        setattr(host, k, v)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise ValueError("Host with same hostname or MAC already exists") from e
    await session.refresh(host)

    return host


async def delete_by_id(session: AsyncSession, host_id: int) -> bool:
    # Using ORM get to be explicit (and portable)
    obj = await session.get(HostORM, host_id)
    if not obj:
        return False
    await session.delete(obj)
    await session.commit()
    return True
