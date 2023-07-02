from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SessionManager
from sqlalchemy.orm import declarative_base, sessionmaker
from typing_extensions import Annotated

SQLALCHEMY_DATABASE_URL = "sqlite:///./dev.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Session = Annotated[SessionManager, Depends(get_db)]
