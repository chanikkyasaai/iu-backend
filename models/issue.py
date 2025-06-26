from sqlalchemy import Column, String, TIMESTAMP, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.base import Base
import uuid

class Issue(Base):
    __tablename__ = "issues"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    employee_id = Column(PG_UUID(as_uuid=True), ForeignKey("employees.id"))
    issue_headline = Column(String, nullable=False)
    issue_desc = Column(String, nullable=False)
    issue_dept = Column(JSON, nullable=False)
    issue_type = Column(JSON, nullable=False)
    village = Column(String)
    state = Column(String)
    district = Column(String)
    taluk = Column(String)
    current_status = Column(String, nullable=False)
    issue_time = Column(TIMESTAMP(timezone=True))
    is_anonymous = Column(Boolean)
    evidence_url = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True))
    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="issues")
    employee = relationship("Employee", back_populates="issues")
    threads = relationship("Thread", back_populates="issue")
