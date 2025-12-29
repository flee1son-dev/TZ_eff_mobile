from pydantic import BaseModel, EmailStr, Field
from backend.modules.users import schemas as userschemas


class UserRegister(userschemas.UserCreate):
    pass

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="user's email")
    password: str = Field(..., description="user's password")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
