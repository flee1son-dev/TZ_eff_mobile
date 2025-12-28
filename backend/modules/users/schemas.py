from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from typing import Optional

class UserPermissions(str, Enum):
    director = "director"
    administering = "administering"
    worker = "worker"


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email")
    first_name: str = Field(..., min_length= 2, max_length=30, description= "User's name" )
    last_name: str = Field(..., min_length= 2, max_length=50, description="User's last name")
    permissions: UserPermissions = Field(..., description="User's role")
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
    permissions: Optional[UserPermissions] = Field(default=None, description="User's admin status, requires superuser")
    password: Optional[str] = Field(..., min_length=8, max_length=32, description="User's new password")
    password_repeat: Optional[str] = Field(..., min_length=8, max_length=32, description="User's repeat password")

    
class UserDelete(BaseModel):
    is_active: bool = Field(default=False, description="Set to False to deactivate user")