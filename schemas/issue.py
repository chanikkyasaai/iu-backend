from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime

class IssueBase(BaseModel):
    user_id: Optional[UUID]
    employee_id: Optional[UUID]
    issue_headline: str
    issue_desc: str
    issue_dept: Any
    issue_type: Any
    village: Optional[str]
    state: Optional[str]
    district: Optional[str]
    taluk: Optional[str]
    current_status: str
    issue_time: Optional[datetime]
    is_anonymous: Optional[bool]
    evidence_url: Optional[Any]
    created_at: Optional[datetime]
    is_edited: Optional[bool]
    is_deleted: Optional[bool]

class IssueCreate(IssueBase):
    pass

class IssueUpdate(IssueBase):
    issue_headline: Optional[str] = None
    issue_desc: Optional[str] = None
    issue_dept: Optional[Any] = None
    issue_type: Optional[Any] = None
    village: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    current_status: Optional[str] = None
    issue_time: Optional[datetime] = None
    is_anonymous: Optional[bool] = None
    evidence_url: Optional[Any] = None
    is_edited: Optional[bool] = False

class Issue(IssueBase):
    id: UUID

    class Config:
        orm_mode = True