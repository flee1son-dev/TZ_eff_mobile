from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., max_length=50, description="Task's title")
    description: Optional[str] = Field(max_length=500, description="Task's description")
    completed: bool = Field(default=False, description="Task ыtatus")

class TaskCreate(TaskBase):
    worker_id: int = Field(..., description="Task's worker ID")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=50, description="Task's new title")
    description: Optional[str] = Field(default=None, max_length=500, description="Task's new description")
    completed: Optional[bool] = Field(default=None, description="Update task status")
    worker_id: Optional[int] = Field(default=None, description="Task's new worker ID")

class TaskResponse(TaskBase):
    id: int = Field(..., description="Task's ID")
    worker_id: int = Field(..., description="Task's worker ID")

