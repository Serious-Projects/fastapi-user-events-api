from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from .database import Base, EntityNotFound, engine, get_event
from .database.connection import SessionLocal
from .views import auth_router, events_router, sponsor_router, users_router

# FastAPI instance
app = FastAPI(title="Event Management API", version="1.0")

# Create all the necessary tables in the database (SQLite database)
Base.metadata.create_all(bind=engine)


# `Unique Constraint Validation` exception handler
@app.exception_handler(HTTPException)
def handle_unique_constraint_violation(req: Request, e: HTTPException):
    return JSONResponse(
        status_code=e.status_code or status.HTTP_400_BAD_REQUEST,
        content={"message": e.detail or "Something went wrong"},
    )


# Handle pydantic validation errors
@app.exception_handler(RequestValidationError)
def handle_value_error(req: Request, e: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "creation of duplicate data"},
    )


# Health-check route
@app.get("/health-check", status_code=status.HTTP_200_OK)
async def check_health():
    return {"message": "Api is working perfectly fine!"}


# register all the business route handlers
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(users_router)
app.include_router(sponsor_router)


# dummy method just to dump some data in the dev db
def test_runner():
    try:
        session = SessionLocal()
        event = get_event(2, session)
        print(event)
    except EntityNotFound:
        print("User not found!")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
