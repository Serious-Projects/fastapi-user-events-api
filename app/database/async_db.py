from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ..config import get_settings

config = get_settings()

engine = create_async_engine(config.SQLITE_DB_URL_ASYNC, pool_pre_ping=True, echo=False)

AsyncSessionLocal = async_sessionmaker(bind=engine, autoflush=False, future=True)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        print("Error getting session for the database!")


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()

    def __repr__(self) -> str:
        columns = ", ".join(
            [
                f"{k}={repr(v)}"
                for k, v in self.__dict__.items()
                if not k.startswith("_")
            ]
        )
        return f"<{self.__class__.__name__}({columns})>"
