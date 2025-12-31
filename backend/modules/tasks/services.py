from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.core import exceptions
from backend.modules.tasks import schemas, models
from backend.modules.users import models as usermodels, schemas as userschemas
from typing import List, Dict


def create_task(
        task_data: schemas.TaskCreate,
        db: Session
) -> models.Task:
    db_task = models.Task(
        title = task_data.title,
        description = task_data.description,
        completed = task_data.completed,
        worker_id = task_data.worker_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(
        task_id: int, 
        task_update_data: schemas.TaskUpdate,
        db: Session
) -> models.Task:
    result = db.execute(select(models.Task).where(models.Task.id == task_id))
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise exceptions.TaskNotFound()
    
    update_data = task_update_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_by_id(
        task_id: int,
        current_user: usermodels.User,
        db: Session
) -> models.Task:
    result = db.execute(select(models.Task).where(models.Task.id == task_id))
    db_task = result.scalar_one_or_none()

    if db_task is None:
        raise exceptions.TaskNotFound()
    
    if current_user.permissions == userschemas.UserRoles.worker:
        if db_task.worker_id != current_user.id:
            raise exceptions.UserForbidden
    elif current_user.permissions == userschemas.UserRoles.director:
        if db_task.worker.director_id != current_user.id:
            raise exceptions.UserForbidden()
    else:
        raise exceptions.UserForbidden()

    return db_task

def get_tasks_by_worker(
        worker_id: int,
        director_id: int,
        db: Session
) -> List[models.Task]:
    worker = db.execute(select(usermodels.User).where(
        usermodels.User.id == worker_id,
        usermodels.User.director_id == director_id
    )).scalar_one_or_none()

    if worker is None:
        raise exceptions.UserForbidden()
    
    result = db.execute(select(models.Task).where(models.Task.worker_id == worker_id))
    db_tasks = result.scalars().all()

    return db_tasks

def get_my_tasks(
        current_user: usermodels.User,
        db: Session
) -> List[models.Task]:
    if current_user.permissions != userschemas.UserRoles.worker:
        raise exceptions.UserForbidden()
    result = db.execute(select(models.Task).where(models.Task.worker_id == current_user.id))
    db_tasks = result.scalars().all()

    return db_tasks


def get_all_tasks(
        director_id: int,
        db: Session,
) -> List[models.Task]:
    result = db.execute(select(usermodels.User.id).where(usermodels.User.director_id == director_id))
    worker_ids = [row[0] for row in result.fetchall()]
    
    if not worker_ids:
        return []
    
    result_tasks = db.execute(select(models.Task).where(models.Task.worker_id.in_(worker_ids)))
    db_tasks = result_tasks.scalars().all()

    return db_tasks

def delete_task(
        task_id: int,
        current_user: usermodels.User,
        db: Session
) -> dict:
    result = db.execute(select(models.Task).where(models.Task.id == task_id))
    db_task = result.scalar_one_or_none()

    if db_task is None:
        raise exceptions.TaskNotFound()

    if db_task.worker.director_id != current_user.id:
        raise exceptions.UserForbidden()

    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}







    
    
