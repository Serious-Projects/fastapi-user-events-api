from pydantic import BaseModel, Field


class TokenBody(BaseModel):
    access_token: str
    type: str


class UserCredentials(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class CurrentUser(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
