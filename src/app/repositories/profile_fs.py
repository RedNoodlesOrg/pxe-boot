from __future__ import annotations
from pathlib import Path
from typing import List, Tuple
from fastapi import HTTPException, status
from app.core.config import settings
from app.schemas.profile import ProfileOut
from .butane import transpile_butane_to_ignition, ButaneError
import re
import json

PROFILE_RE = re.compile(r"^(?P<id>\d+)\+(?P<name>[^/]+)\.bu$")

def _iter_profiles() -> list[Tuple[int, str, Path]]:
    items: list[Tuple[int, str, Path]] = []
    for p in settings.profiles_dir.glob("*.bu"):
        m = PROFILE_RE.match(p.name)
        if not m:
            continue
        pid = int(m.group("id"))
        name = m.group("name")
        items.append((pid, name, p.resolve()))
    return sorted(items, key=lambda x: x[0])

def _bu_path(pid: int, name: str) -> Path:
    return (settings.profiles_dir / f"{pid}+{name}.bu").resolve()

def _ign_path(pid: int, name: str) -> Path:
    return (settings.artifacts_dir / f"{pid}+{name}.ign").resolve()

def _next_profile_id() -> int:
    items = _iter_profiles()
    return (items[-1][0] + 1) if items else 1

def list_profiles() -> List[ProfileOut]:
    out: list[ProfileOut] = []
    for pid, name, bu in _iter_profiles():
        ign = _ign_path(pid, name)
        out.append(
            ProfileOut(
                id=pid,
                name=name,
                bu_path=str(bu),
                ign_path=str(ign) if ign.exists() else None,
            )
        )
    return out

def get_profile(pid: int) -> ProfileOut:
    items = {p[0]: p for p in _iter_profiles()}
    if pid not in items:
        raise HTTPException(status_code=404, detail="Profile not found")
    _, name, bu = items[pid]
    ign = _ign_path(pid, name)
    return ProfileOut(
        id=pid,
        name=name,
        bu_path=str(bu),
        ign_path=str(ign) if ign.exists() else None,
    )

def read_profile_butane(pid: int) -> str:
    items = {p[0]: p for p in _iter_profiles()}
    if pid not in items:
        raise HTTPException(404, "Profile not found")
    _, _, bu = items[pid]
    return bu.read_text(encoding="utf-8")

def ensure_ignition_fresh(pid: int) -> Path:
    items = {p[0]: p for p in _iter_profiles()}
    if pid not in items:
        raise HTTPException(404, "Profile not found")
    _, name, bu = items[pid]
    ign = _ign_path(pid, name)
    if (not ign.exists()) or (ign.stat().st_mtime < bu.stat().st_mtime):
        yaml_text = bu.read_text(encoding="utf-8")
        try:
            json_text = transpile_butane_to_ignition(yaml_text)
            json.loads(json_text)
        except ButaneError as e:
            raise HTTPException(status_code=400, detail=f"Butane transpile error: {e}")
        ign.parent.mkdir(parents=True, exist_ok=True)
        ign.write_text(json_text, encoding="utf-8")
    return ign

def read_profile_ignition(pid: int) -> str:
    ign = ensure_ignition_fresh(pid)
    return ign.read_text(encoding="utf-8")

def create_profile(name: str) -> ProfileOut:
    if "+" in name:
        raise HTTPException(status_code=400, detail="Profile name must not contain '+'")
    pid = _next_profile_id()
    bu = _bu_path(pid, name)
    if bu.exists():
        raise HTTPException(status_code=409, detail="Profile file already exists")
    bu.parent.mkdir(parents=True, exist_ok=True)
    bu.write_text("# Butane YAML goes here\n", encoding="utf-8")
    return ProfileOut(id=pid, name=name, bu_path=str(bu), ign_path=None)

def upsert_butane(pid: int, yaml_text: str) -> ProfileOut:
    items = {p[0]: p for p in _iter_profiles()}
    if pid not in items:
        raise HTTPException(404, "Profile not found")
    _, name, bu = items[pid]
    bu.write_text(yaml_text, encoding="utf-8")
    ensure_ignition_fresh(pid)
    ign = _ign_path(pid, name)
    return ProfileOut(id=pid, name=name, bu_path=str(bu), ign_path=str(ign))

def rename_profile(pid: int, new_name: str) -> ProfileOut:
    if "+" in new_name:
        raise HTTPException(status_code=400, detail="Profile name must not contain '+'")
    items = {p[0]: p for p in _iter_profiles()}
    if pid not in items:
        raise HTTPException(404, "Profile not found")
    _, old_name, bu_old = items[pid]
    bu_new = _bu_path(pid, new_name)
    if bu_new.exists():
        raise HTTPException(409, detail="Target profile filename exists")
    bu_old.replace(bu_new)
    ign_old = _ign_path(pid, old_name)
    if ign_old.exists():
        ign_old.replace(_ign_path(pid, new_name))
    return ProfileOut(id=pid, name=new_name, bu_path=str(bu_new), ign_path=str(_ign_path(pid, new_name)) if _ign_path(pid, new_name).exists() else None)

def delete_profile(pid: int) -> None:
    items = {p[0]: p for p in _iter_profiles()}
    if pid not in items:
        raise HTTPException(404, "Profile not found")
    _, name, bu = items[pid]
    bu.unlink()
    ign = _ign_path(pid, name)
    if ign.exists():
        ign.unlink()
