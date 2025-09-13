import pytest
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_normalize_mac_variants():
    from app.repositories.host import _normalize_mac

    assert _normalize_mac("52:54:00:AA:BB:CC") == "52:54:00:aa:bb:cc"
    assert _normalize_mac("52-54-00-aa-bb-cc") == "52:54:00:aa:bb:cc"
    # Cisco-style with dots
    assert _normalize_mac("5254.00aa.bbcc") == "52:54:00:aa:bb:cc"
    # Trim + lowercase handling
    assert _normalize_mac("  52:54:00:AA:BB:CC  ") == "52:54:00:aa:bb:cc"


@pytest.mark.asyncio
async def test_create_and_get_by_mac_normalization():
    from app.core.db import SessionLocal, init_db
    from app.repositories import host as repo
    from app.repositories.profile_fs import create_profile

    await init_db()
    p = create_profile("repo-prof1")

    async with SessionLocal() as session:
        # Create with Cisco-style MAC; should be normalized on save
        obj = await repo.create(
            session,
            hostname="repo-node-1",
            ip="10.3.0.1",
            mac="5254.00aa.bb01",
            profile_id=p.id,
        )
        assert obj.mac == "52:54:00:aa:bb:01"

        # Lookup using hyphen style should match the same row
        got = await repo.get_by_mac(session, "52-54-00-aa-bb-01")
        assert got is not None and got.id == obj.id


@pytest.mark.asyncio
async def test_create_duplicate_constraints():
    from app.core.db import SessionLocal, init_db
    from app.repositories import host as repo
    from app.repositories.profile_fs import create_profile

    await init_db()
    p = create_profile("repo-prof2")

    async with SessionLocal() as session:
        a = await repo.create(
            session,
            hostname="repo-node-a",
            ip="10.3.0.2",
            mac="52:54:00:aa:bb:02",
            profile_id=p.id,
        )
        assert a.id is not None

        # Duplicate hostname
        with pytest.raises(ValueError):
            await repo.create(
                session,
                hostname="repo-node-a",
                ip="10.3.0.3",
                mac="52:54:00:aa:bb:03",
                profile_id=p.id,
            )

        # Duplicate MAC
        with pytest.raises(ValueError):
            await repo.create(
                session,
                hostname="repo-node-b",
                ip="10.3.0.4",
                mac="52:54:00:aa:bb:02",
                profile_id=p.id,
            )


@pytest.mark.asyncio
async def test_update_paths_and_conflicts():
    from app.core.db import SessionLocal, init_db
    from app.repositories import host as repo
    from app.repositories.profile_fs import create_profile

    await init_db()
    p = create_profile("repo-prof3")

    async with SessionLocal() as session:
        # Non-existent host returns None
        assert await repo.update(session, 999_999, {"hostname": "x"}) is None

        h1 = await repo.create(
            session,
            hostname="repo-node-u1",
            ip="10.3.0.5",
            mac="52:54:00:aa:bb:05",
            profile_id=p.id,
        )
        h2 = await repo.create(
            session,
            hostname="repo-node-u2",
            ip="10.3.0.6",
            mac="52:54:00:aa:bb:06",
            profile_id=p.id,
        )
        # Capture attributes eagerly to avoid lazy load on expired state
        h1_hostname = h1.hostname
        h1_mac = h1.mac
        h2_id = h2.id
        # Update succeeds with normalization
        updated = await repo.update(
            session, h2.id, {"mac": "5254.00aa.bb66", "ip": "10.3.0.66"}
        )
        assert updated is not None
        assert updated.mac == "52:54:00:aa:bb:66" and updated.ip == "10.3.0.66"

        # Conflicting hostname -> ValueError
        with pytest.raises(ValueError):
            await repo.update(session, h2_id, {"hostname": h1_hostname})

        # Conflicting MAC -> ValueError
        with pytest.raises(ValueError):
            await repo.update(session, h2_id, {"mac": h1_mac})


@pytest.mark.asyncio
async def test_update_profile_validation_error():
    from app.core.db import SessionLocal, init_db
    from app.repositories import host as repo
    from app.repositories.profile_fs import create_profile

    await init_db()
    p = create_profile("repo-prof4")

    async with SessionLocal() as session:
        h = await repo.create(
            session,
            hostname="repo-node-p1",
            ip="10.3.0.7",
            mac="52:54:00:aa:bb:07",
            profile_id=p.id,
        )

        # Setting a non-existent profile_id should bubble HTTPException
        with pytest.raises(HTTPException):
            await repo.update(session, h.id, {"profile_id": 9_999_999})


@pytest.mark.asyncio
async def test_delete_by_id_behaviour():
    from app.core.db import SessionLocal, init_db
    from app.repositories import host as repo
    from app.repositories.profile_fs import create_profile

    await init_db()
    p = create_profile("repo-prof5")

    async with SessionLocal() as session:
        h = await repo.create(
            session,
            hostname="repo-node-d1",
            ip="10.3.0.8",
            mac="52:54:00:aa:bb:08",
            profile_id=p.id,
        )
        assert await repo.delete_by_id(session, h.id) is True
        # Second attempt should be False
        assert await repo.delete_by_id(session, h.id) is False


@pytest.mark.asyncio
async def test_get_by_id_roundtrip():
    from app.core.db import SessionLocal, init_db
    from app.repositories import host as repo
    from app.repositories.profile_fs import create_profile

    await init_db()
    p = create_profile("repo-prof6")

    async with SessionLocal() as session:
        h = await repo.create(
            session,
            hostname="repo-node-g1",
            ip="10.3.0.9",
            mac="52:54:00:aa:bb:09",
            profile_id=p.id,
        )
        got = await repo.get_by_id(session, h.id)
        assert got is not None and got.id == h.id
        assert await repo.get_by_id(session, 123456789) is None
