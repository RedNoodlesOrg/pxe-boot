from pydantic import BaseModel, Field

class HostCreate(BaseModel):
    hostname: str = Field(min_length=1, max_length=255)
    ip: str
    mac: str
    profile_id: int

class HostUpdate(BaseModel):
    hostname: str | None = None
    ip: str | None = None
    mac: str | None = None
    profile_id: int | None = None

class HostOut(BaseModel):
    id: int
    hostname: str
    ip: str
    mac: str
    profile_id: int

    class Config:
        from_attributes = True
