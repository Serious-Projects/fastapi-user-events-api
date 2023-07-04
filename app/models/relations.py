from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, func

from ..database.connection import Base

user_event_association = Table(
    "enrollments_table",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user_table.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("event_table.id"), primary_key=True),
    Column("enrolled_at", DateTime, default=func.now()),
)

event_sponsor_association = Table(
    "event_sponsor_association",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("event_table.id")),
    Column("sponsor_id", Integer, ForeignKey("sponsor_table.id")),
)
