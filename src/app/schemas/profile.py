from pydantic import BaseModel, Field, field_validator

def _ensure_no_plus(v: str) -> str:
    if "+" in v:
        raise ValueError("Profile name must not contain '+'")
    return v

class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)

    _no_plus = field_validator("name")(_ensure_no_plus)

class ProfileUpdate(BaseModel):
    new_name: str | None = Field(default=None, min_length=1, max_length=255)

    @field_validator("new_name")
    @classmethod
    def _no_plus(cls, v: str | None):
        return _ensure_no_plus(v) if v else v

class ProfileOut(BaseModel):
    id: int
    name: str
    bu_path: str
    ign_path: str | None = None
