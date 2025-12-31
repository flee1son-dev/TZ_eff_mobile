from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.core import exceptions
from backend.modules.users import models, schemas
from backend.core.security import hash_password
from typing import List


def update_profile(
        current_user: models.User,
        user_update_data: schemas.UserUpdate,
        db: Session,
) -> models.User:
    result = db.execute(select(models.User).where(models.User.id == current_user.id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise exceptions.UserNotFound()
    
    update_data = user_update_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password":
            if value:
                value = hash_password(value)
        setattr(db_user, key, value)
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user_from_director(
        worker_id: int,
        director_id: int,
        worker_update_data: schemas.UserUpdateFromDirector,
        db: Session
):
    result = db.execute(select(models.User).where(
        models.User.id == worker_id,
        models.User.director_id == director_id,
        models.User.is_active == True
    ))

    worker = result.scalar_one_or_none()
    update_data = worker_update_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password":
            if value:
                value = hash_password(value)
        setattr(worker, key, value)
        
    db.add(worker)
    db.commit()
    db.refresh(worker)

    return worker


def attach_worker_to_director(
        current_user: models.User,
        worker_id: int,
        db: Session
) -> models.User:
    
    if current_user.permissions != schemas.UserRoles.director:
        raise exceptions.UserForbidden()
    
    worker = db.get(models.User, worker_id)

    if not worker:
        raise exceptions.UserNotFound()
    
    if worker.is_active == False:
        raise exceptions.UserInactive()

    if worker.permissions != schemas.UserRoles.worker:
        raise exceptions.ValidationError(detail="Only workers can be attached")
    
    if worker.director_id is not None:
        raise exceptions.UserForbidden()
    
    worker.director_id = current_user.id
    
    db.commit()
    db.refresh(worker)

    return worker
    

def delete_user(
        user_id: int,
        user_delete_data: schemas.UserDelete,
        current_user: models.User,
        db: Session
) -> dict:
    result = db.execute(select(models.User).where(models.User.id == user_id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise exceptions.UserNotFound()
    
    if current_user.id != db_user.director_id or current_user.id != user_id:
        raise exceptions.UserForbidden
    
    delete_data = user_delete_data.model_dump(exclude_unset=True)
    for key, value in delete_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"detail": "User deleted"}

def get_worker(
        worker_id: int,
        current_user: models.User,
        db: Session
) -> models.User:
    result = db.execute(select(models.User).where(
        models.User.id == worker_id, 
        models.User.is_active == True
    ))

    worker = result.scalar_one_or_none()

    if not worker:
        raise exceptions.UserNotFound()
    
    if current_user.permissions == schemas.UserRoles.director:
        raise exceptions.UserForbidden
    
    if worker.director_id is None or worker.director_id == current_user.id:
        return worker
    
    raise exceptions.UserForbidden()

def get_profile(
        current_user: models.User,
        db: Session
):  
    return current_user


def get_all_workers(
        director_id,
        db: Session
) -> List[models.User]:
    result = db.execute(select(models.User.id).where(models.User.director_id == director_id, models.User.is_active == True))
    all_workers = result.scalars().all()

    return all_workers



