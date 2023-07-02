from fastapi import APIRouter, HTTPException, status

from ..database.connection import Session
from ..models.event import Event
from ..models.user import User
from ..schema.event import EventIn, EventOut, UpdateEvent

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=list[EventOut], status_code=status.HTTP_200_OK)
def get_events_all(db: Session):
    events = db.query(Event).order_by(Event.created_at).all()
    return events


@router.get("/{event_id}", response_model=EventOut, status_code=status.HTTP_200_OK)
def get_event(event_id: int, db: Session):
    event = db.query(Event).get(event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event does not exist!"
        )
    return event


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EventOut)
def create_event(event: EventIn, db: Session):
    # Event object
    event = Event(
        title=event.title,
        description=event.description,
        date=event.date,
        creator_id=event.creator_id,
    )

    # Add a new event to the database
    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.patch("/{event_id}")
def update_event(event_id: int, event: UpdateEvent, db: Session):
    pass


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session):
    pass
