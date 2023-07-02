from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from ..database.connection import Base
from .enrollment import Enrollment


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(15), nullable=False)
    email = Column(String(15), nullable=False, unique=True)
    password = Column(String(15), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship with self created events
    events = relationship("Event", backref="creator")

    # Relationship with enrolled events
    enrolled_events = relationship(
        "Event", secondary=Enrollment, back_populates="attendees"
    )


from .event import Event
