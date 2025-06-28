from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from models.base import Base
from sqlalchemy.orm import relationship
import uuid


class IssueDeptOfficer(Base):
    __tablename__ = "issue_dept_officers"
    id = Column(PG_UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    dept_id = Column(PG_UUID(as_uuid=True), ForeignKey(
        "issue_depts.id"), nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    head_name = Column(String)
    desgn = Column(String)
    phone = Column(String)
    email = Column(String)

    dept = relationship("IssueDept", back_populates="officer")
    user = relationship("User", back_populates="officer")