from fastapi import APIRouter, HTTPException, status

from ..database.connection import Session
from ..models.event import EventModel
from ..schema.event import EventIn, EventOut, UpdateEvent
from ..security import CurrentLoggedInUser

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=list[EventOut], status_code=status.HTTP_200_OK)
def get_events_all(db: Session):
    events = db.query(EventModel).order_by(EventModel.created_at).all()
    return events


@router.get("/{event_id}", response_model=EventOut, status_code=status.HTTP_200_OK)
def get_event(event_id: int, db: Session):
    event = db.query(EventModel).get(event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event does not exist!"
        )
    return event


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EventOut)
def create_event(curr_user: CurrentLoggedInUser, event: EventIn, db: Session):
    print(curr_user)
    # Event object
    event = EventModel(
        title=event.title,
        description=event.description,
        date=event.date,
        location=event.location,
        creator_id=curr_user.id,
    )

    # Add a new event to the database
    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.patch("/{event_id}", status_code=status.HTTP_200_OK, response_model=EventOut)
def update_event(event_id: int, event_data: UpdateEvent, db: Session):
    event = db.query(EventModel).get(event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There was no such event found.",
        )

    # Update the user
    update_data = event_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        # update the field with user provided data
        setattr(event, key, value)

    # commit the updates to the database
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session):
    event = db.query(EventModel).get(event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="We could not find such event!",
        )

    # Delete the user from the database
    db.delete(event)
    db.commit()
