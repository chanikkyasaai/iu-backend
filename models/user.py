from uuid import UUID
import uuid
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base
from .profile import Profile
from .issue import Issue


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    google_id = Column(String)
    email = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    
    profile = relationship(Profile, back_populates="user", uselist=False)
    issues = relationship(Issue, back_populates="user")
    comments = relationship("Comment", back_populates="user")
    saves = relationship("Save", back_populates="user")
    officer = relationship("IssueDeptOfficer", back_populates="user")
    dept = relationship("IssueDept", back_populates="user")