from pathlib import Path

from fastapi import FastAPI, status

from .database.connection import Base, SessionLocal, engine
from .database.seeder import EntityNotFound, get_event
from .views import auth, events, users

# FastAPI instance
app = FastAPI(title="Event Management API", version="1.0")
BASE_DIR = Path(__file__).parent
Base.metadata.create_all(bind=engine)


# Health-check route
@app.get("/health-check", status_code=status.HTTP_200_OK)
async def check_health():
    return {"message": "Api is working perfectly fine!"}


app.include_router(users.router)
app.include_router(events.router)
app.include_router(auth.router)

if __name__ == "__main__":
    try:
        session = SessionLocal()
        event = get_event(2, session)
    except EntityNotFound:
        print("User not found!")
