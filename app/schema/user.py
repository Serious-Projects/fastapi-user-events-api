from typing import List

from pydantic import BaseModel, EmailStr, Field


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


class UserCreate(BaseSchema):
    name: str = Field(..., title="Username", max_length=25)
    email: EmailStr = Field(..., title="User email")
    password: str = Field(..., title="User password", min_length=8)


class UserOut(BaseSchema):
    id: int
    name: str
    email: EmailStr
    enrolled_events: List["EventOut"]


class UpdateUser(BaseSchema):
    name: str | None = Field(None, min_length=6)
    email: EmailStr | None = Field(None)


from ..schema.event import EventOut

UserOut.update_forward_refs()
