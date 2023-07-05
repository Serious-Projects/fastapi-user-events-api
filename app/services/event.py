from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models import EventModel
from ..schema.event import EventIn, UpdateEvent
from ..security.auth_tokens import CurrentLoggedInUser


def get_event_by(id: int, db: Session) -> EventModel:
    event = db.query(EventModel).get(id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="event not found"
        )
    return event


def create_event(
    db: Session, event: EventIn, curr_user: CurrentLoggedInUser
) -> EventModel:
    event = EventModel(**event, creator_id=curr_user.id)
    # Add a new event to the database
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def check_event_exists(db: Session, id: int) -> bool:
    event = db.query(EventModel).get(id)
    return event is not None


def update_event(db: Session, id: int, patch_data: UpdateEvent) -> EventModel:
    event = get_event_by(id, db)
    # Update the user
    event_dict = patch_data.dict(exclude_unset=True)
    for key, value in event_dict.items():
        # update the event object's field with user provided data
        setattr(event, key, value)
    # push the changes to the database
    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, id: int) -> EventModel:
    event = get_event_by(id, db)
    db.delete(event)
    db.commit()
    return event
