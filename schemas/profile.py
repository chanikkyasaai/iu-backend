from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List, Dict, Any


class ProfileBase(BaseModel):
    fullname: Optional[str]
    role: Optional[str]
    following_users: Optional[List[Dict[str, Any]]]
    following_issues: Optional[List[Dict[str, Any]]]
    # Note: Fixed typo from "depts" to "depts" to match your model
    following_depts: Optional[List[Dict[str, Any]]]
    following_locations: Optional[List[Dict[str, Any]]]


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    fullname: Optional[str] = None
    role: Optional[str] = None
    following_users: Optional[List[str]] = Field(default_factory=list)
    following_issues: Optional[List[str]] = Field(default_factory=list)
    following_depts: Optional[List[str]] = Field(default_factory=list)
    following_locations: Optional[List[str]] = Field(default_factory=list)

class Profile(ProfileBase):
    id: UUID

    class Config:
        orm_mode = True