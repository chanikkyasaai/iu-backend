from sqlalchemy import Column, String, TIMESTAMP, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

from models.base import Base


class Comment(Base):
    __tablename__ = "comments"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    issue_id = Column(PG_UUID(as_uuid=True), ForeignKey("issues.id"))
    username = Column(String)
    comment = Column(String, nullable=False)
    likes = Column(Integer)
    is_reply = Column(Boolean)
    comment_id = Column(PG_UUID(as_uuid=True), ForeignKey("comments.id"))
    created_at = Column(TIMESTAMP(timezone=True))
    is_edited = Column(Boolean)
    is_deleted = Column(Boolean)
    
    replies = relationship("Comment", back_populates="parent_comment", remote_side=[id])
    parent_comment = relationship("Comment", back_populates="replies", remote_side=[comment_id])
