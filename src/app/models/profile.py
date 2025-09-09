from pydantic import BaseModel, Field

class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    content: str | None = None
    path: str | None = None

class ProfileUpdate(BaseModel):
    new_name: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None

class ProfileOut(BaseModel):
    name: str
    path: str
