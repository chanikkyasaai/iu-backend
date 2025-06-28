from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid
from models.base import Base

class Profile(Base):
    __tablename__ = "profile"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    fullname = Column(String, nullable=False)
    role = Column(String, nullable=False)
    following_users = Column(JSON)
    following_issues = Column(JSON)
    following_depts = Column(JSON)
    following_locations = Column(JSON)
    is_deleted = Column(Integer, default=1)
    
    user = relationship("User", back_populates="profile", uselist=False)
