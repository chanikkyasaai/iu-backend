from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from models.base import Base
import uuid

class IssueDept(Base):
    __tablename__ = "issue_depts"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    dept = Column(String)
    negative_count = Column(Integer, default=0)
    positive_count = Column(Integer, default=0)
