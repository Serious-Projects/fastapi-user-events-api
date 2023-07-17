from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.async_db import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, primary_key=True, nullable=False
    )
    name: Mapped[str] = mapped_column("name", String(15), nullable=False)
    email: Mapped[EmailStr] = mapped_column("email", String(60), nullable=False)
    password: Mapped[str] = mapped_column("password", String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime, onupdate=func.now()
    )
    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="user",
        order_by="Event.created_at",
        cascade="save-update, merge, refresh-expire, expunge, delete, delete-orphan",
    )


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, primary_key=True, nullable=False
    )
    title: Mapped[str] = mapped_column("title", String, nullable=False)
    description: Mapped[str] = mapped_column("description", String)
    creator_id: Mapped[int] = mapped_column(
        "creator_id", ForeignKey("user.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime, onupdate=func.now()
    )
    user: Mapped[User] = relationship(User, back_populates="events")
