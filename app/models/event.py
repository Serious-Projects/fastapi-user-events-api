from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from ..database.connection import Base
from .enrollment import Enrollment


class Event(Base):
    __tablename__ = "event_table"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(15), nullable=False)
    description = Column(Text)
    date = Column(DateTime, nullable=False)

    # Relationship with the event creator
    creator_id = Column(Integer, ForeignKey("user_table.id"))

    # Relationship with the enrolled users
    attendees = relationship(
        "User", secondary=Enrollment, back_populates="enrolled_events"
    )

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


from .user import User
