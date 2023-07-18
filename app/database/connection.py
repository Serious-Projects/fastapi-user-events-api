from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import get_settings

config = get_settings()
engine = create_engine(config.SQLITE_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# Dependency
def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    except Exception as e:
        print("Error:", str(type(e)))
    finally:
        db_session.close()
