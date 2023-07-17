from functools import lru_cache

from app.api.repositories.event_repository import EventRepository
from app.api.repositories.sponsor_repository import SponsorRepository
from app.api.repositories.user_repository import UserRepository
from app.api.services.auth_service import AuthenticationService
from app.api.services.event_service import EventService
from app.api.services.sponsor_service import SponsorService
from app.api.services.user_service import UserService


@lru_cache
def get_user_service():
    user_repository = UserRepository()
    return UserService(user_repository)


@lru_cache
def get_event_service():
    event_repository = EventRepository()
    return EventService(event_repository)


@lru_cache
def get_sponsor_service():
    sponsor_repository = SponsorRepository()
    event_service = get_event_service()
    return SponsorService(sponsor_repository, event_service)


@lru_cache
def get_auth_service():
    user_service = get_user_service()
    return AuthenticationService(user_service)
