from passlib.context import CryptContext

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = b"df4e600f7910a1cb98af41f381a2da8191a4780580461f36151f1e8f17f94b39"


def hash_password(password: str) -> str:
    return pass_context.hash(password)


def verify_password(password: str, hash_pass: str) -> bool:
    return pass_context.verify(password, hash_pass)
