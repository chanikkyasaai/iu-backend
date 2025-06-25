from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class EmployeeBase(BaseModel):
    fullname: Optional[str]
    role: Optional[str]
    state: Optional[str]
    district: Optional[str]
    false_count: Optional[int]
    good_count: Optional[int]

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: UUID

    class Config:
        orm_mode = True