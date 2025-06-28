from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from models.base import Base
import uuid

class IssueDept(Base):
    __tablename__ = "issue_depts"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    dept = Column(String)
    location = Column(String)
    desc = Column(String)
    category = Column(String)
    negative_count = Column(Integer, default=0)
    positive_count = Column(Integer, default=0)

    officer = relationship("IssueDeptOfficer", back_populates="dept")
    user = relationship("User", back_populates="dept")
    issues = relationship("Issue", back_populates="dept")