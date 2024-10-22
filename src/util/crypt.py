from datetime import timedelta

import bcrypt
from dotenv import load_dotenv
import os

from fastapi_jwt import JwtAccessBearer

from src.model.user import User

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
ACCESS_EXPIRES_IN = int(os.getenv("ACCESS_EXPIRES_IN"))
access_security = JwtAccessBearer(secret_key=JWT_SECRET, auto_error=True)


def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password_hash(candidate: str, hash: str) -> bool:
    return bcrypt.checkpw(candidate.encode(), hash.encode())


def generate_jwt(user: User) -> str:
    payload = {"username": user.username}
    return access_security.create_access_token(payload, expires_delta=timedelta(seconds=ACCESS_EXPIRES_IN))
