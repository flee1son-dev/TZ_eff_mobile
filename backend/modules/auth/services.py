from backend.core import security, exceptions
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import EmailStr
from backend.modules.users import models as usermodels
from backend.modules.auth import schemas



def authentificate_user(
        email: EmailStr,
        password: str,
        db: Session
):
    result = db.execute(select(usermodels.User).where(usermodels.User.email == email))

    user = result.scalar_one_or_none()

    if not user:
        raise exceptions.UserNotFound()
    
    if not security.verify_password(pwd=password, hash_pwd=user.password):
        raise exceptions.CredentialsException()
    
    return user


def register_user(
        user_data: schemas.UserRegister,
        db: Session
):
    result = db.execute(select(usermodels.User).where(usermodels.User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise exceptions.UserEmailAlreadyExists()
    
    hashed_pwd = security.hash_password(user_data.password)

    db_user = usermodels.User(
        email = user_data.email,
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        password = hashed_pwd,
        permissions = user_data.permissions,
        is_active = user_data.is_active
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(
        user_data: schemas.UserLogin,
        db: Session
) -> schemas.TokenResponse:
    db_user = authentificate_user(email=user_data.email, password=user_data.password, db=db)
    
    access_token = security.create_access_jwt(user=db_user)
    refresh_token = security.create_refresh_jwt(user=db_user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
