from sqlalchemy import Column, TIMESTAMP, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from models.base import Base

class Save(Base):
    __tablename__ = "saves"
    issue_id = Column(PG_UUID(as_uuid=True), ForeignKey("issues.id"), primary_key=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True))

    issue = relationship("Issue", back_populates="saves", uselist=False)
    user = relationship("User", back_populates="saves")