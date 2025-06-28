from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class IssueDeptOfficerBase(BaseModel):
    head_name: Optional[str] = ""
    desgn: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[EmailStr] = ""


class IssueDeptOfficerCreate(IssueDeptOfficerBase):
    pass


class IssueDeptOfficerUpdate(BaseModel):
    head_name: Optional[str] = None
    desgn: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class IssueDeptOfficerRead(IssueDeptOfficerBase):
    id: UUID

    class Config:
        orm_mode = True
