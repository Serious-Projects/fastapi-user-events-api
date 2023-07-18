from typing import List, Union

from sqlalchemy import BooleanClauseList

from app.api.models.event import EventModel
from app.api.repositories.event_repository import EventRepository
from app.api.schema.event import EventIn, UpdateEvent
from app.utils.exceptions import EntityNotFoundException
from app.utils.jwt import CurrentLoggedInUser


class EventService:
    def __init__(self, event_repository: EventRepository):
        self._repository = event_repository

    def get_by_id(self, id: Union[int, str]) -> EventModel:
        user = self._repository.get_by_id(id)
        if user is None:
            raise EntityNotFoundException("user not found")
        return user

    def get_all(self) -> List[EventModel]:
        return self._repository.get_all()

    def get_by_filter(self, filter: BooleanClauseList) -> EventModel:
        user = self._repository.get_by_filter(filter)
        if user is None:
            raise EntityNotFoundException("user not found")
        return user

    def get_all_by_filter(self, filter: BooleanClauseList) -> List[EventModel]:
        return self._repository.get_all_by_filter(filter)

    def create(self, event: EventIn, current_user: CurrentLoggedInUser) -> EventModel:
        return self._repository.create(event, current_user)

    def update(self, id: Union[int, str], event: UpdateEvent) -> EventModel:
        return self._repository.update(id, event)

    def delete(self, id: Union[int, str]) -> EventModel:
        return self._repository.delete(id)
