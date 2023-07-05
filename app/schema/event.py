from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    class Config:
        orm_mode = True


class EventIn(BaseEvent):
    title: str = Field(..., title="Event Title")
    description: str = Field(..., title="Event description")
    location: str = Field(..., title="Event location")
    date: datetime = Field(datetime.now(), title="Event occurring date")


class EventOut(BaseEvent):
    id: int
    title: str
    description: str
    location: str
    date: datetime
    sponsors: List["Sponsor"]


class UpdateEvent(BaseEvent):
    title: str | None = Field(None, min_length=5)
    description: str | None = Field(None, min_length=5)
    location: str | None = Field(None, min_length=3)
    date: datetime | None = Field(None)


from .sponsor import Sponsor

EventOut.update_forward_refs()
