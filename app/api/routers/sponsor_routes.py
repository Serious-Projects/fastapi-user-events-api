from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api.schema.sponsor import Sponsor, SponsorCreate
from app.api.services import get_event_service, get_sponsor_service
from app.api.services.event_service import EventService
from app.api.services.sponsor_service import SponsorService

sponsor_router = APIRouter()


@sponsor_router.post(
    "/event/{event_id}/sponsor-it",
    status_code=status.HTTP_200_OK,
    response_model=Sponsor,
)
def sponsor_the_event(
    event_id: Union[int, str],
    sponsor: SponsorCreate,
    sponsor_service: SponsorService = Depends(get_sponsor_service),
):
    sponsor_service.add(event_id, sponsor)
    return {"message": "sponsorship added successfully"}


@sponsor_router.get(
    "/event/{event_id}/withdraw-sponsorship/{sponsor_id}",
    status_code=status.HTTP_200_OK,
)
def withdraw_sponsorship(
    event_id: Union[int, str],
    sponsor_id: Union[int, str],
    sponsor_service: SponsorService = Depends(get_sponsor_service),
):
    sponsor_service.remove(sponsor_id, event_id)
    return {"message": "Sponsorship withdrawn successfully"}
