from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..database import Session
from ..schema.sponsor import Sponsor, SponsorCreate
from ..services import event as event_service
from ..services import sponsor as sponsor_service

router = APIRouter(prefix="/sponsor", tags=["Sponsors"])


@router.post("/to/{event_id}", status_code=status.HTTP_200_OK, response_model=Sponsor)
def sponsor_the_event(event_id: int, sponsor: SponsorCreate, db: Session):
    event = event_service.get_event_by(event_id, db)
    _ = sponsor_service.add_sponsorship(db, sponsor, event)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "sponsorship added successfully"},
    )


@router.get(
    "/{event_id}/withdraw-sponsorship/{sponsor_id}", status_code=status.HTTP_200_OK
)
def withdraw_sponsorship(event_id: int, sponsor_id: int, db: Session):
    # try to find the event with the given event_id
    event = event_service.get_event_by(event_id, db)
    _ = sponsor_service.withdraw_sponsorship(db, sponsor_id, event_id, event)
    return JSONResponse(
        status_code=200, content={"message": "Sponsorship withdrawn successfully"}
    )
