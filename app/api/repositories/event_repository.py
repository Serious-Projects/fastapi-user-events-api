from typing import Optional

from fastapi import Depends
from sqlalchemy import Cast
from sqlalchemy.orm import Session

from app.api.repositories.user_repository import UserRepository
from app.api.schema.event import EventIn, UpdateEvent
from app.utils.exceptions import EntityNotFoundException
from app.utils.jwt import CurrentLoggedInUser

from ...database.connection import get_db
from ..models.event import EventModel


class EventRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db_session = db

    def get_events(self) -> list[EventModel]:
        events = self.db_session.query(EventModel).all()
        return events

    def get_event(self, event_id: int) -> EventModel:
        event = self.db_session.query(EventModel).get(event_id)
        if event is None:
            raise EntityNotFoundException(f"Event not found for event_id: {event_id}")
        return event

    def update_event(self, event_id: int, event_data: UpdateEvent) -> EventModel:
        event = self.get_event(event_id)
        # Update the user
        event_dict = event_data.dict(exclude_unset=True)
        for key, value in event_dict.items():
            # update the event object's field with user provided data
            setattr(event, key, value)
        # push the changes to the database
        self.db_session.commit()
        self.db_session.refresh(event)
        return event

    def delete_event(self, event_id: int) -> EventModel:
        # check for the event existence
        event = self.get_event(event_id)
        # delete the event from the database
        self.db_session.delete(event)
        self.db_session.commit()
        return event

    def create_event(
        self, event: EventIn, logged_user: CurrentLoggedInUser
    ) -> EventModel:
        event = EventModel(**event.dict(), creator_id=logged_user.id)
        # Add a new event to the database
        self.db_session.add(event)
        self.db_session.commit()
        self.db_session.refresh(event)
        return event

    def get_event_or_none(self, id: int) -> Optional[EventModel]:
        event = self.db_session.query(EventModel).get(id)
        return event
