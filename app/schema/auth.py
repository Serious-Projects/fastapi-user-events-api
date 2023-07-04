from pydantic import BaseModel, Field


class TokenBody(BaseModel):
    access_token: str
    type: str


class UserCredentials(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
