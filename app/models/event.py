from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from ..database.connection import Base
from .relations import event_sponsor_association, user_event_association


class EventModel(Base):
    __tablename__ = "event_table"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(30), nullable=False)
    description = Column(Text)
    date = Column(DateTime, nullable=False)
    location = Column(String(30), nullable=False)
    creator_id = Column(Integer, ForeignKey("user_table.id"))

    # Relationship with its sponsors
    sponsors = relationship(
        "SponsorModel", secondary=event_sponsor_association, back_populates="events"
    )

    # Relationship with the participants
    participants = relationship(
        "UserModel", secondary=user_event_association, back_populates="enrolled_events"
    )

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Event(id={self.id}, title={self.title}, date_time={self.date})>"


from .user import UserModel
