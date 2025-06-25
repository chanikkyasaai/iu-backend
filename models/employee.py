from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

from models.base import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fullname = Column(String)
    role = Column(String)
    state = Column(String)
    district = Column(String)
    false_count = Column(Integer)
    good_count = Column(Integer)
