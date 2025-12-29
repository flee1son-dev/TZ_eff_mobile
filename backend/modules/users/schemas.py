from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from typing import Optional

class UserRoles(str, Enum):
    director = "director"
    worker = "worker"


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email")
    first_name: str = Field(..., min_length= 2, max_length=30, description= "User's name" )
    last_name: str = Field(..., min_length= 2, max_length=50, description="User's last name")
    permissions: UserRoles = Field(default=UserRoles.worker, description="User's role")
    is_active: bool = Field(default=True, deprecated="active or not active user's account")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=32, description="User's password")
    password_repeat: str = Field(..., min_length=8, max_length=32, description="User's repeat password")


class UserResponse(UserBase):
    id: int = Field(..., description="User's primary key")
    
    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None, description="User's new email")
    last_name: Optional[str] = Field(default=None, min_length= 2, max_length=50, description="User's new last name")
    password: Optional[str] = Field(..., min_length=8, max_length=32, description="User's new password")
    password_repeat: Optional[str] = Field(..., min_length=8, max_length=32, description="User's repeat password")

class UserUpdateRoles(BaseModel):
    permissions: Optional[UserRoles] = Field(default=None, description="New user's role")
    
class UserDelete(BaseModel):
    is_active: bool = Field(default=False, description="Set to False to deactivate user")

class AttachWorker(BaseModel):
    worker_id: int = Field(..., description="Worker status user ID")