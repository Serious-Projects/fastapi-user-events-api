from fastapi import APIRouter, status

from ...database.connection import Session
from ...security.auth_tokens import CurrentLoggedInUser
from ..models.event import EventModel
from ..schema.event import EventIn, EventOut, UpdateEvent

eventRouter = APIRouter()


@eventRouter.get("", response_model=list[EventOut], status_code=status.HTTP_200_OK)
def get_events_all(db: Session):
    events = db.query(EventModel).order_by(EventModel.created_at).all()
    return events


@eventRouter.get("/{event_id}", response_model=EventOut, status_code=status.HTTP_200_OK)
def get_event(event_id: int, db: Session):
    # event = event_service.get_event_by(event_id, db)
    return


@eventRouter.post("", status_code=status.HTTP_201_CREATED, response_model=EventOut)
def create_event(curr_user: CurrentLoggedInUser, event: EventIn, db: Session):
    # event = event_service.create_event(db, event, curr_user)
    return


@eventRouter.patch(
    "/{event_id}", status_code=status.HTTP_200_OK, response_model=EventOut
)
def update_event(event_id: int, event_data: UpdateEvent, db: Session):
    # event = event_service.update_event(db, event_id, event_data)
    return


@eventRouter.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session):
    # event_service.delete_event(db, event_id)
    return
