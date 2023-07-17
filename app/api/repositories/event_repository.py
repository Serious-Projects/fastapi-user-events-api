from typing import Optional, Union

from fastapi import Depends
from sqlalchemy import BooleanClauseList
from sqlalchemy.orm import Session

from app.api.models.event import EventModel
from app.api.schema.auth import CurrentUser
from app.api.schema.event import EventIn, UpdateEvent
from app.database.connection import get_db
from app.utils.exceptions import EntityNotFoundException
from app.utils.jwt import CurrentLoggedInUser


class EventRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self._db_session = db

    def get_all(self) -> list[EventModel]:
        events = self._db_session.query(EventModel).all()
        return events

    def get(self, id: Union[int, str]) -> EventModel:
        event = self._db_session.query(EventModel).get(id)
        if event is None:
            raise EntityNotFoundException(f"Event not found for event_id: {id}")
        return event

    def get_by_filter(self, filter: BooleanClauseList):
        return self._db_session.query(EventModel).filter(filter).first()

    def get_all_by_filter(self, filter: BooleanClauseList):
        return self._db_session.query(EventModel).filter(filter).all()

    def update(self, id: Union[int, str], event_data: UpdateEvent) -> EventModel:
        event = self.get(id)
        # Update the user
        event_dict = event_data.dict(exclude_unset=True)
        for key, value in event_dict.items():
            # update the event object's field with user provided data
            setattr(event, key, value)
        # push the changes to the database
        self._db_session.commit()
        self._db_session.refresh(event)
        return event

    def delete(self, id: Union[int, str]) -> EventModel:
        # check for the event existence
        event = self.get(id)
        # delete the event from the database
        self._db_session.delete(event)
        self._db_session.commit()
        return event

    def create(self, event: EventIn, logged_user: CurrentUser) -> EventModel:
        event = EventModel(**event.dict(), creator_id=logged_user.id)
        # Add a new event to the database
        self._db_session.add(event)
        self._db_session.commit()
        self._db_session.refresh(event)
        return event

    def get_event_or_none(self, id: Union[int, str]) -> Optional[EventModel]:
        event = self._db_session.query(EventModel).get(id)
        return event
