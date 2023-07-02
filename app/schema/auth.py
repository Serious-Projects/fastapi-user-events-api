from pydantic import BaseModel


class TokenBody(BaseModel):
    access_token: str
    type: str
