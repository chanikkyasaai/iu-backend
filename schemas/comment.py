from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class CommentBase(BaseModel):
    issue_id: Optional[UUID]
    username: Optional[str] = None
    comment: Optional[str]
    is_reply: Optional[bool] = False
    comment_id: Optional[UUID] = None
    is_edited: Optional[bool] = False
    is_deleted: Optional[bool] = False


class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    issue_id: Optional[UUID] = None
    username: Optional[str] = None
    comment: Optional[str] = None
    is_reply: Optional[bool] = None
    comment_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    is_edited: Optional[bool] = True
    is_deleted: Optional[bool] = None
    

class Comment(CommentBase):
    id: UUID

    class Config:
        from_attributes = True
