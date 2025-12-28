from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends
from jose import JWTError
import jwt
from backend.core.config import settings
from backend.core.database import get_db
from backend.modules.users import schemas as userschemas


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE = settings.ACCESS_TOKEN_EXPIRES_MINUTES
REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRES_DAYS
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
        expire_minutes: int = ACCESS_TOKEN_EXPIRE, 
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
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm
    )
    return encoded

def create_jwt(
        type: str, 
        payload:dict,
        expire_minutes: int = ACCESS_TOKEN_EXPIRE,
        expire_days: timedelta | None = None
):
    jwt_payload = {TOKEN_TYPE_FIELD: type}
    jwt_payload.update(payload)

    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_days=expire_days
    )

def create_access_jwt(user: userschemas.UserBase):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email
    }
    return create_jwt(
        type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload,
        expire_minutes=ACCESS_TOKEN_EXPIRE,
        expire_days= None
    )

def create_refresh_jwt(user: userschemas.UserBase):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email
    }
    return create_jwt(
        type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        expire_days= timedelta(days=REFRESH_TOKEN_EXPIRE)
    )












