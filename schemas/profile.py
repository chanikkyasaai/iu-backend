from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List, Any


class ProfileBase(BaseModel):
    user_id: Optional[UUID] = None
    fullname: str
    role: str
    following_users: Optional[Any] = None
    following_issues: Optional[Any] = None
    following_depts: Optional[Any] = None
    following_locations: Optional[Any] = None


class ProfileCreate(ProfileBase):
    
    pass


class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: UUID

    class Config:
        orm_mode = True