from typing import Union

from ..models.sponsor import SponsorModel
from ..repositories.sponsor_repository import SponsorRepository
from ..schema.sponsor import SponsorCreate
from .event_service import EventService
from ...utils.exceptions import EntityNotFoundException


class SponsorService:
    def __init__(
        self,
        sponsor_repository: SponsorRepository,
        event_service: EventService,
    ):
        self._repository = sponsor_repository
        self._event_service = event_service

    def get_by_id(self, id: Union[int, str]) -> SponsorModel:
        sponsor = self._repository.get_by_id(id)
        if sponsor is None:
            raise EntityNotFoundException("sponsor does not exist")
        return sponsor

    def add(self, event_id: Union[int, str], sponsor: SponsorCreate):
        event = self._event_service.get_by_id(event_id)
        return self._repository.add_sponsorship(sponsor, event)

    def remove(self, event_id: Union[int, str], sponsor_id: Union[int, str]):
        event = self._event_service.get_by_id(event_id)
        self._repository.remove_sponsorship(sponsor_id, event_id, event)
