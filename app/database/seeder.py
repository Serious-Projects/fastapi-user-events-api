from faker import Faker

from ..models.event import Event
from ..models.user import User
from .connection import Session

fake = Faker()


class EntityNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def seed_users(session: Session):
    for _ in range(10):
        user = User(name=fake.name(), email=fake.email(), password=fake.password())
        session.add(user)
        session.commit()

    print("User seeding complete...")


def seed_events(session: Session):
    for i in range(10):
        user = session.query(User).get(i + 1)
        if user is not None:
            event = Event(
                title=f"Event title {i+1}",
                description=f"Event description {i+1}",
                date=fake.date_time(),
                creator_id=i + 1,
            )

            event.attendees.append(user)
            session.add(event)
            session.commit()

    print("Event seeding complete...")


def get_user(user_id: int, session: Session) -> User | None:
    user = session.query(User).get(user_id)
    if user is None:
        raise EntityNotFound("User not found")
    return user


def get_event(event_id: int, session: Session) -> Event | None:
    event = session.query(Event).get(event_id)
    if event is None:
        raise EntityNotFound("Event not found!")
    return event
