from datetime import datetime
from typing import ForwardRef, List

from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    class Config:
        orm_mode = True


class EventIn(BaseEvent):
    title: str | None = Field(None, title="Event Title")
    description: str | None = Field(None, title="Event description")
    date: datetime = Field(datetime.now(), title="Event occurring date")
    creator_id: int = Field(0, title="Event creator's id")


class EventOut(BaseEvent):
    id: int
    title: str
    description: str
    date: datetime


class UpdateEvent(BaseEvent):
    title: str | None = Field(None, min_length=5)
    description: str | None = Field(None, min_length=5)
    date: datetime | None = Field(None)


from ..schema.user import UserOut

EventOut.update_forward_refs()
