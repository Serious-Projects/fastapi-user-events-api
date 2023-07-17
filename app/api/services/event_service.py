from typing import List, Union

from sqlalchemy import BooleanClauseList

from app.api.models.event import EventModel
from app.api.repositories.event_repository import EventRepository
from app.api.schema.event import EventIn, UpdateEvent
from app.utils.jwt import CurrentLoggedInUser


class EventService:
    def __init__(self, event_repository: EventRepository):
        self._repository = event_repository

    def get(self, id: Union[int, str]) -> EventModel:
        return self._repository.get(id)

    def get_all(self) -> List[EventModel]:
        return self._repository.get_all()

    def get_by_filter(self, filter: BooleanClauseList) -> EventModel:
        return self._repository.get_by_filter(filter)

    def get_all_by_filter(self, filter: BooleanClauseList) -> List[EventModel]:
        return self._repository.get_all_by_filter(filter)

    def create(self, event: EventIn, current_user: CurrentLoggedInUser) -> EventModel:
        return self._repository.create(event, current_user)

    def update(self, id: Union[int, str], event: UpdateEvent) -> EventModel:
        return self._repository.update(id, event)

    def delete(self, id: Union[int, str]) -> EventModel:
        return self._repository.delete(id)
