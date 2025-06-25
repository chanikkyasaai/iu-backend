from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Save(BaseModel):
    issue_id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
