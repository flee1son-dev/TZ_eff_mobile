from backend.modules.tasks import models, schemas, services
from backend.modules.users import models as usermodels, schemas as userchemas
from backend.core import security, exceptions
from backend.core.database import get_db
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/create", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: schemas.TaskCreate,
    current_user: usermodels.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
    ):
    if current_user.permissions != userchemas.UserRoles.director:
        raise exceptions.UserForbidden()
    
    return services.create_task(task_data=task_data, db= db)


@router.put("/update/{task_id}", response_model=schemas.TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    task_update_data: schemas.TaskUpdate,
    current_user: usermodels.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.permissions != userchemas.UserRoles.director:
        raise exceptions.UserForbidden()
    return services.update_task(task_id=task_id, task_update_data=task_update_data, db=db)


@router.get("/{task_id}", response_model=schemas.TaskResponse, status_code=status.HTTP_200_OK)
def get_task(
    task_id: int,
    current_user: usermodels.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return services.get_task_by_id(task_id=task_id, current_user=current_user, db=db)

@router.get("/{worker_id}", response_model=list[schemas.TaskResponse], status_code=status.HTTP_200_OK)
def get_tasks_by_worker(
    worker_id: int,
    current_user: usermodels.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.permissions != userchemas.UserRoles.director:
        raise exceptions.UserForbidden()
    
    return services.get_tasks_by_worker(worker_id=worker_id, director_id=current_user.id, db=db)

@router.get("/my", response_model=list[schemas.TaskResponse], status_code=status.HTTP_200_OK)
def get_my_tasks(
    current_user: usermodels.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return services.get_my_tasks(current_user=current_user, db=db)


@router.get("/", response_model=list[schemas.TaskResponse], status_code=status.HTTP_200_OK)
def all_tasks(
    current_user: usermodels.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.permissions != userchemas.UserRoles.director:
        raise exceptions.UserForbidden()
    return services.get_all_tasks(director_id=current_user.id, db=db)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: usermodels.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.permissions != userchemas.UserRoles.director:
        raise exceptions.UserForbidden()
    
    return services.delete_task(task_id=task_id, current_user=current_user, db=db)

    
    
