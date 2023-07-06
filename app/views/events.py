from fastapi import APIRouter, Depends, status

from ..database.connection import Session
from ..models.event import EventModel
from ..schema.event import EventIn, EventOut, UpdateEvent
from ..security import CurrentLoggedInUser, authenticate_user_from
from ..services import event as event_service

router = APIRouter(
    prefix="/events",
    tags=["Events", "Authenticated"],
    dependencies=[Depends(authenticate_user_from)],
)


@router.get("", response_model=list[EventOut], status_code=status.HTTP_200_OK)
def get_events_all(db: Session):
    events = db.query(EventModel).order_by(EventModel.created_at).all()
    return events


@router.get("/{event_id}", response_model=EventOut, status_code=status.HTTP_200_OK)
def get_event(event_id: int, db: Session):
    event = event_service.get_event_by(event_id, db)
    return event


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EventOut)
def create_event(curr_user: CurrentLoggedInUser, event: EventIn, db: Session):
    event = event_service.create_event(db, event, curr_user)
    return event


@router.patch("/{event_id}", status_code=status.HTTP_200_OK, response_model=EventOut)
def update_event(event_id: int, event_data: UpdateEvent, db: Session):
    event = event_service.update_event(db, event_id, event_data)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session):
    event_service.delete_event(db, event_id)
