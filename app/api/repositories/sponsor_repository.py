from typing import Optional, Union

from fastapi import Depends
from sqlalchemy.orm import Session

from ..models.event import EventModel
from ..models.relations import event_sponsor_association
from ..models.sponsor import SponsorModel
from ..schema.sponsor import SponsorCreate
from ...database.connection import get_db
from ...utils.exceptions import EntityNotFoundException


class SponsorRepository:
    _db: Session

    def __init__(self, db: Optional[Session] = None):
        # using `next(get_db())` because it is a generator function that automatically
        # creates a context manager for each session to properly handle the resources
        self._db = db if db is not None else next(get_db())

    def get_by_id(self, id: Union[int, str]) -> Optional[SponsorModel]:
        return self._db.query(SponsorModel).get(id)

    def add_sponsorship(
        self, sponsor: SponsorCreate, event: EventModel
    ) -> SponsorModel:
        new_sponsor = SponsorModel(name=sponsor.name, logo=sponsor.logo, contact=sponsor.contact)  # fmt: skip
        event.sponsors.append(new_sponsor)
        self._db.add(new_sponsor)
        self._db.commit()
        self._db.refresh(new_sponsor)
        return new_sponsor

    def remove_sponsorship(
        self,
        sponsor_id: Union[int, str],
        event_id: Union[int, str],
        event: EventModel,
    ) -> None:
        sponsor = (
            self._db.query(SponsorModel)
            .join(event_sponsor_association)
            .filter(
                SponsorModel.id == sponsor_id,
                event_sponsor_association.c.event_id == event_id,
            )
            .first()
        )
        if sponsor is None:
            raise EntityNotFoundException("There is no such sponsor to this event")
        # remove the association from the events table
        event.sponsors.remove(sponsor)
        # delete the actual sponsor from the database too, because `remove()` only removes the association
        # and does not delete's the original entity!
        self._db.delete(sponsor)
        self._db.commit()

    def check_event_exists(self, id: int) -> bool:
        event = self.get_by_id(id)
        return event is not None
