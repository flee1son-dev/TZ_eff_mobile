from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.modules.users import services, schemas, models
from backend.core import security, exceptions

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("", response_model=list[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_all_workers(
    db: Session = Depends(get_db),
    current_user: models.User  = Depends(security.get_current_user)
):
    if current_user.permissions != schemas.UserRoles.director:
        raise exceptions.UserForbidden()

    return services.get_all_workers(director_id=current_user.id, db=db)


@router.get("/profile", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_profile(
    user_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return services.get_profile()


@router.get("/{user_id}", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_worker(
    worker_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    if current_user.permissions != schemas.UserRoles.director:
        raise exceptions.UserForbidden()
    
    return services.get_worker(worker_id=worker_id, director_id=current_user.id, db=db)





@router.put("/update/{worker_id}", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def update_worker_from_director(
    worker_id: int,
    worker_update_data: schemas.UserUpdateFromDirector,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.permissions != schemas.UserRoles.director:
        raise exceptions.UserForbidden()
    
    return services.update_user_from_director(worker_id=worker_id, director_id=current_user.id, worker_update_data=worker_update_data, db=db)

@router.put("/profile/update", response_models=schemas.UserResponse, status_code=status.HTTP_200_OK)
def update_profile(
    update_data: schemas.UserUpdate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return services.update_profile(current_user=current_user, user_update_data=update_data, db=db)


@router.put("/attach", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def attack_worker(
    worker_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return services.attach_worker_to_director(current_user=current_user, worker_id=worker_id, db=db)

@router.delete("/user_id")
def delete_user(
    user_id: int,
    user_delete_data: schemas.UserDelete,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    return services.delete_user(user_id=user_id, user_delete_data=user_delete_data, current_user=current_user, db=db)







