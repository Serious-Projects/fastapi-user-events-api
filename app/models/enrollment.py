from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, func

from ..database.connection import Base

Enrollment = Table(
    "enrollments_table",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user_table.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("event_table.id"), primary_key=True),
    Column("enrolled_at", DateTime, default=func.now()),
)
