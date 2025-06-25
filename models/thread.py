from sqlalchemy import Column, String, TIMESTAMP, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid

from models.base import Base


class Thread(Base):
    __tablename__ = "threads"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    issue_id = Column(PG_UUID(as_uuid=True), ForeignKey("issues.id"))
    thread_headline = Column(String, nullable=False)
    thread_desc = Column(String, nullable=False)
    thread_type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True))
    is_edited = Column(Boolean)
    is_deleted = Column(Boolean)
    evidence_url = Column(JSON)
    
    issue = relationship("Issue", back_populates="threads")
