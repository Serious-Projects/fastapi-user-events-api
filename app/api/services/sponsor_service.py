from typing import Union

from app.api.repositories.sponsor_repository import SponsorRepository
from app.api.schema.sponsor import SponsorCreate
from app.api.services.event_service import EventService


class SponsorService:
    def __init__(
        self, sponsor_repository: SponsorRepository, event_service: EventService
    ):
        self._repository = sponsor_repository
        self._event_service = event_service

    def get(self, id: Union[int, str]):
        return self._repository.get(id)

    def add(self, event_id: Union[int, str], sponsor: SponsorCreate):
        event = self._event_service.get(event_id)
        return self._repository.add_sponsorship(sponsor, event)

    def remove(self, event_id: Union[int, str], sponsor_id: Union[int, str]):
        event = self._event_service.get(event_id)
        self._repository.remove_sponsorship(sponsor_id, event_id, event)
