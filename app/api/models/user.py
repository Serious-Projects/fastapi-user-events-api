from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.api.models.relations import user_event_association
from app.database.connection import Base


class UserModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(15), nullable=False)
    email = Column(String(15), nullable=False, unique=True)
    password = Column(String(15), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship with self created events
    events = relationship("EventModel", backref="creator", cascade="all, delete-orphan")

    # Relationship with enrolled events
    enrolled_events = relationship(
        "EventModel", secondary=user_event_association, back_populates="participants"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


from app.api.models.event import EventModel
