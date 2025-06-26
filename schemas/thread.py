from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime


class ThreadBase(BaseModel):
    issue_id: Optional[UUID]
    thread_headline: str
    thread_desc: str
    thread_type: str
    created_at: Optional[datetime]
    is_edited: Optional[bool]
    is_deleted: Optional[bool]
    evidence_url: Optional[Any]


class ThreadCreate(ThreadBase):
    pass

class ThreadUpdate(ThreadBase):
    issue_id: Optional[UUID] = None
    thread_headline: Optional[str] = None
    thread_desc: Optional[str] = None
    thread_type: Optional[str] = None
    created_at: Optional[datetime] = None
    is_edited: Optional[bool] = True
    is_deleted: Optional[bool] = None
    evidence_url: Optional[Any] = None

class Thread(ThreadBase):
    id: UUID

    class Config:
        orm_mode = True
