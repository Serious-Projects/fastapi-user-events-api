from fastapi import APIRouter, HTTPException, status

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
