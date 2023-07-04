from passlib.context import CryptContext

from ..config import config

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = config.hash_secret_key


def hash_password(password: str) -> str:
    return pass_context.hash(password)


def verify_password(password: str, hash_pass: str) -> bool:
    return pass_context.verify(password, hash_pass)
