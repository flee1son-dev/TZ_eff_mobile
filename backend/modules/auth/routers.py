from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.modules.auth import schemas as authschemas, services
from backend.modules.users import schemas as userschemas
from backend

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", response_model=userschemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: authschemas.UserRegister,
    db: Session = Depends(get_db)
):
    return services.register_user(user_data=user_data, db=db)


@router.post("login", response_model=authschemas.TokenResponse, status_code=status.HTTP_200_OK)
def login(
    user_data: authschemas.UserLogin,
    db: Session = Depends(get_db)
):
    return services.login_user(user_data=user_data, db=db)

