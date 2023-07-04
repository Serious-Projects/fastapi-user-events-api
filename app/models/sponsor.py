from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from ..database import Base
from .relations import event_sponsor_association


class SponsorModel(Base):
    __tablename__ = "sponsor_table"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(30), nullable=False, unique=True)
    logo = Column(String(255), nullable=True)
    contact = Column(String(60), nullable=False)
    events = relationship(
        "EventModel", secondary=event_sponsor_association, back_populates="sponsors"
    )

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Sponsor(id={self.id}, name={self.name})>"
