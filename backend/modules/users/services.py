from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.core import exceptions
from backend.modules.users import models, schemas
from backend.core.security import hash_password
from typing import List


def update_user(
        user_id: int,
        user_update_data: schemas.UserUpdate,
        db: Session,
) -> models.User:
    result = db.execute(select(models.User).where(models.User.id == user_id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise exceptions.UserNotFound()
    
    update_data = user_update_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password":
            if value:
                value = hash_password(value)
        else:
            continue
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(
        user_id: int,
        user_delete_data: schemas.UserDelete,
        db: Session
) -> models.User:
    result = db.execute(select(models.User).where(models.User.id == user_id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise exceptions.UserNotFound()
    
    delete_data = user_delete_data.model_dump(exclude_unset=True)
    for key, value in delete_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def get_user(
        user_id: int,
        db: Session
) -> models.User:
    result = db.execute(select(models.User).where(models.User.id == user_id))

    user = result.scalar_one_or_none()

    if not user:
        raise exceptions.UserNotFound()
    
    return user


def get_all_users(
        db: Session
) -> List[models.User]:
    result = db.execute(select(models.User))

    all_users = result.scalars().all()

    return all_users
