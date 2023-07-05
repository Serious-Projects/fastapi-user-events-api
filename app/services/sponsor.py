from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import EventModel, SponsorModel, event_sponsor_association
from ..schema.sponsor import SponsorCreate


def get_sponsor_by(id: int, db: Session) -> SponsorModel:
    sponsor = db.query(SponsorModel).get(id)
    if sponsor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no such sponsor is sponsoring this event",
        )
    return sponsor


def add_sponsorship(
    db: Session, sponsor: SponsorCreate, event: EventModel
) -> SponsorModel:
    new_sponsor = SponsorModel(
        name=sponsor.name, logo=sponsor.logo, contact=sponsor.contact
    )
    event.sponsors.append(new_sponsor)
    db.add(new_sponsor)
    db.commit()
    db.refresh(new_sponsor)
    return new_sponsor


def withdraw_sponsorship(
    db: Session, sponsor_id: int, event_id: int, event: EventModel
) -> None:
    sponsor = (
        db.query(SponsorModel)
        .join(event_sponsor_association)
        .filter(
            SponsorModel.id == sponsor_id,
            event_sponsor_association.c.event_id == event_id,
        )
        .first()
    )
    if sponsor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no such sponsor to this event",
        )
    # remove the association from the events table
    event.sponsors.remove(sponsor)
    # delete the actual sponsor from the database too, because `remove()` only removes the association
    # and does not delete's the original entity!
    db.delete(sponsor)
    db.commit()


def check_event_exists(db: Session, id: int) -> bool:
    event = db.query(SponsorModel).get(id)
    return event is not None
