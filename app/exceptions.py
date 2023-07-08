from typing import Optional

from fastapi import HTTPException, status


class EntityNotFoundException(HTTPException):
    """Exception raised when trying to query non existing entity"""

    def __init__(self, detail: Optional[str] = "Entity not found exception"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateEntityException(HTTPException):
    """Exception raised when trying to add a duplicate entity"""

    def __init__(self, detail: Optional[str] = "Duplicate entity exception"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InternalServerException(HTTPException):
    """Exception raised when server does not respond"""

    def __init__(self, detail: Optional[str] = "Internal Server Error exception"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
