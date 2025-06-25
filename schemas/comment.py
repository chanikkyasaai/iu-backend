from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class CommentBase(BaseModel):
    issue_id: Optional[UUID]
    username: Optional[str]
    comment: str
    is_reply: Optional[bool]
    comment_id: Optional[UUID]
    created_at: Optional[datetime]
    is_edited: Optional[bool]
    is_deleted: Optional[bool]


class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    comment: str 
    is_edited: Optional[bool] = None
    is_deleted: Optional[bool] = None

class Comment(CommentBase):
    id: UUID

    class Config:
        orm_mode = True
