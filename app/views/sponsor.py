from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..database import Session
from ..models import EventModel, SponsorModel
from ..schema.sponsor import Sponsor, SponsorCreate

router = APIRouter(prefix="/sponsor", tags=["Sponsors"])


@router.post("/to/{event_id}", status_code=status.HTTP_200_OK, response_model=Sponsor)
def sponsor_the_event(event_id: int, sponsor: SponsorCreate, db: Session):
    event = db.query(EventModel).get(event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no event created"
        )

    new_sponsor = SponsorModel(
        name=sponsor.name, logo=sponsor.logo, contact=sponsor.contact
    )
    # associate the sponsor with the event
    event.sponsors.append(new_sponsor)

    # save the new sponsor to the database
    db.add(new_sponsor)
    db.commit()
    db.refresh(new_sponsor)
    return new_sponsor


@router.get(
    "/{event_id}/withdraw-sponsorship/{sponsor_id}", status_code=status.HTTP_200_OK
)
def withdraw_sponsorship(event_id: int, sponsor_id: int, db: Session):
    # try to find the event with the given event_id
    event = db.query(EventModel).get(event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no such event created",
        )

    # try to find the sponsor associated with the event
    sponsor = (
        db.query(SponsorModel)
        .filter(SponsorModel.id == sponsor_id, EventModel.sponsors.any(id=event_id))
        .first()
    )
    if sponsor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no such sponsor to this event",
        )

    # remove the association from the events table
    event.sponsors.remove(sponsor)

    # Delete the actual sponsor from the database too, because `remove()` only removes the association
    # and does not delete's the original entity!
    db.delete(sponsor)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "Sponsorship withdrawn"})
