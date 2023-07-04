from typing import List

from pydantic import BaseModel, Field

from app.schema.event import EventOut


class SponsorCreate(BaseModel):
    name: str = Field(..., min_length=5, title="Name of the Sponsor")
    logo: str = Field(..., title="Logo/Brand of the Sponsor")
    contact: str = Field(..., min_length=10, title="Contact information of the Sponsor")


class Sponsor(BaseModel):
    id: int
    name: str
    logo: str
    contact: str

    class Config:
        orm_mode = True
