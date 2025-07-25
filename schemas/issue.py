from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime


class IssueBase(BaseModel):
    dept_id: Optional[UUID]
    issue_headline: Optional[str]
    issue_desc: Optional[str]
    issue_dept: Optional[Any]
    issue_type: Optional[Any]
    village: Optional[str]
    state: Optional[str]
    district: Optional[str]
    taluk: Optional[str]
    current_status: Optional[str]
    issue_time: Optional[datetime]
    is_anonymous: Optional[bool] = False
    priority: Optional[str] = "low"  # Default priority
    evidence_url: Optional[Any] = None
    created_at: Optional[datetime] = datetime.now()
    is_edited: Optional[bool] = False
    is_deleted: Optional[bool] = False


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    dept_id: Optional[UUID] = None
    issue_headline: Optional[str] = None
    issue_desc: Optional[str] = None
    issue_dept: Optional[str] = None
    issue_type: Optional[str] = None
    village: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    current_status: Optional[str] = None
    issue_time: Optional[datetime] = None
    is_anonymous: Optional[bool] = None
    evidence_url: Optional[Any] = None
    is_edited: Optional[bool] = True
    is_deleted: Optional[bool] = None


class Issue(IssueBase):
    id: UUID

    class Config:
        orm_mode = True


class IssueBatchFilterRequest(BaseModel):
    user_ids: Optional[list[UUID]] = None
    dept_ids: Optional[list[UUID]] = None
    issue_ids: Optional[list[UUID]] = None
    states: Optional[list[str]] = None
    districts: Optional[list[str]] = None
    taluks: Optional[list[str]] = None
    villages: Optional[list[str]] = None
