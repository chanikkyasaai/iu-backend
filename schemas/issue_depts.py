from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class IssueDeptBase(BaseModel):
    dept: str
    negative_count: Optional[int] = 0
    positive_count: Optional[int] = 0

class IssueDeptCreate(IssueDeptBase):
    pass

class IssueDeptUpdate(BaseModel):
    dept: Optional[str] = None
    negative_count: Optional[int] = None
    positive_count: Optional[int] = None

class IssueDept(IssueDeptBase):
    id: UUID

    class Config:
        orm_mode = True