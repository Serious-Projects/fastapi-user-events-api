from typing import Optional, Union

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.models.event import EventModel
from app.api.models.relations import event_sponsor_association
from app.api.models.sponsor import SponsorModel
from app.api.schema.sponsor import SponsorCreate
from app.database.connection import get_db
from app.utils.exceptions import EntityNotFoundException


class SponsorRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self._db = db

    def get(self, id: Union[int, str]) -> Optional[SponsorModel]:
        return self._db.query(SponsorModel).get(id)

    def add_sponsorship(
        self,
        sponsor: SponsorCreate,
        event: EventModel,
    ) -> SponsorModel:
        new_sponsor = SponsorModel(
            name=sponsor.name, logo=sponsor.logo, contact=sponsor.contact
        )
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
        event = self._db.query(SponsorModel).get(id)
        return event is not None
