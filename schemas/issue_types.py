from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class IssueTypeBase(BaseModel):
    type: str


class IssueTypeCreate(IssueTypeBase):
    pass


class IssueTypeUpdate(BaseModel):
    type: Optional[str] = None


class IssueType(IssueTypeBase):
    id: UUID

    class Config:
        orm_mode = True
