from pathlib import Path

from fastapi import FastAPI, status

from .database import Base, EntityNotFound, engine, get_event
from .database.connection import SessionLocal
from .views import auth_router, events_router, sponsor_router, users_router

# FastAPI instance
app = FastAPI(title="Event Management API", version="1.0")
BASE_DIR = Path(__file__).parent

# Create all the necessary tables in the database (SQLite database)
Base.metadata.create_all(bind=engine)


# Health-check route
@app.get("/health-check", status_code=status.HTTP_200_OK)
async def check_health():
    return {"message": "Api is working perfectly fine!"}


app.include_router(auth_router)
app.include_router(events_router)
app.include_router(users_router)
app.include_router(sponsor_router)


def test_runner():
    try:
        session = SessionLocal()
        event = get_event(2, session)
        print(event)
    except EntityNotFound:
        print("User not found!")


if __name__ == "__main__":
    test_runner()
