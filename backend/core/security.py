from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends
from jose import JWTError, jwt
from backend.core.config import settings
from backend.core.database import get_db


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRES_MINUTES
REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRES_MINUTES
ACCESS_TOKEN_TYPE = settings.ACCESS_TOKEN_TYPE_FIELD
REFRESH_TOKEN_TYPE = settings.REFRESH_TOKEN_TYPE_FIELD
TOKEN_TYPE_FIELD = "type"


oauth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(pwd: str) -> str:
    return pwd_context.hash(pwd)

def verify_password(pwd: str, hash_pwd: str) -> bool:
    return pwd_context.verify(secret=pwd, hash=hash_password)


def encode_jwt(
        payload: dict,
        private_key: str = SECRET_KEY, 
        algorithm: str = ALGORITHM,
        expire_minutes: int, 
        expire_days: timedelta | None = None
) -> str:
    to_encode = payload.copy()

    now = datetime.utcnow()
    if expire_days:
        expire = datetime.utcnow + expire_days
    else:
        expire = datetime.utcnow + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode







