from typing import Union

from fastapi import APIRouter, Depends, status

from ...utils.jwt import CurrentUser
from ..schema.event import EventIn, EventOut, UpdateEvent
from ..services import EventService, get_event_service

event_router = APIRouter(tags=["Event Routes"])


@event_router.get(
    "/events", response_model=list[EventOut], status_code=status.HTTP_200_OK
)
def get_all_events(event_service: EventService = Depends(get_event_service)):
    return event_service.get_all()


@event_router.get(
    "/events/{event_id}", response_model=EventOut, status_code=status.HTTP_200_OK
)
def get_event(
    event_id: Union[int, str],
    event_service: EventService = Depends(get_event_service),
):
    return event_service.get_by_id(event_id)


@event_router.post(
    "/event", status_code=status.HTTP_201_CREATED, response_model=EventOut
)
def create_event(
    event: EventIn,
    curr_user: CurrentUser,
    event_service: EventService = Depends(get_event_service),
):
    return event_service.create(event, curr_user)


@event_router.patch(
    "/event/{event_id}", status_code=status.HTTP_200_OK, response_model=EventOut
)
def update_event(
    event_id: Union[int, str],
    event_data: UpdateEvent,
    event_service: EventService = Depends(get_event_service),
):
    return event_service.update(event_id, event_data)


@event_router.delete("/event/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: Union[int, str],
    event_service: EventService = Depends(get_event_service),
):
    return event_service.delete(event_id)
