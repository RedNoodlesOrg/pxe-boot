from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from typing import List
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut
from app.repositories import profile_fs

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("", response_model=List[ProfileOut])
def list_profiles():
    return profile_fs.list_profiles()

@router.get("/{pid:int}", response_model=ProfileOut)
def get_profile(pid: int):
    return profile_fs.get_profile(pid)

@router.get("/{pid:int}/butane")
def download_butane(pid: int):
    prof = profile_fs.get_profile(pid)
    return Response(
        content=profile_fs.read_profile_butane(pid),
        media_type="text/yaml",
        headers={"Content-Disposition": f'attachment; filename="{prof.id}+{prof.name}.bu"'},
    )

@router.get("/{pid:int}/ignition")
def download_ignition(pid: int):
    prof = profile_fs.get_profile(pid)
    return Response(
        content=profile_fs.read_profile_ignition(pid),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{prof.id}+{prof.name}.ign"'},
    )

@router.post("", response_model=ProfileOut, status_code=201)
def create_profile(payload: ProfileCreate):
    return profile_fs.create_profile(payload.name)

@router.post("/{pid:int}/upload", response_model=ProfileOut)
async def upload_butane(pid: int, file: UploadFile = File(...)):
    filename = (file.filename or "").lower()
    if not (filename.endswith(".bu") or filename.endswith(".yaml") or filename.endswith(".yml")):
        raise HTTPException(status_code=400, detail="Upload a Butane YAML file (.bu/.yaml/.yml)")
    data = await file.read()
    return profile_fs.upsert_butane(pid, data.decode("utf-8"))

@router.put("/{pid:int}", response_model=ProfileOut)
def rename(pid: int, payload: ProfileUpdate):
    if not payload.new_name:
        raise HTTPException(status_code=400, detail="new_name is required to rename")
    return profile_fs.rename_profile(pid, payload.new_name)

@router.delete("/{pid:int}", status_code=204)
def delete_profile(pid: int):
    profile_fs.delete_profile(pid)
    return None
