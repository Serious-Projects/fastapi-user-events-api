from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routers import auth_router, event_router, sponsor_router, user_router
from app.database.connection import Base, engine

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


# # Handle pydantic validation errors
@app.exception_handler(RequestValidationError)
def handle_value_error(req: Request, e: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(e)},
    )


# Health-check route
@app.get("/health-check", status_code=status.HTTP_200_OK)
async def check_health():
    return {"message": "Api is working perfectly fine!"}


# register all the business route handlers
app.include_router(auth_router)
app.include_router(event_router)
app.include_router(user_router)
app.include_router(sponsor_router)
