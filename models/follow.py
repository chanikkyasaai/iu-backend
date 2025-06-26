# from sqlalchemy import Column, ForeignKey
# from sqlalchemy.dialects.postgresql import UUID as PG_UUID
# from sqlalchemy.orm import relationship
# from .base import Base
# import uuid

# class Follow(Base):
#     __tablename__ = "follows"

#     id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
#     follower_user_id = Column(PG_UUID(as_uuid=True),  nullable=False)
#     followed_user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

#     follower = relationship('User', foreign_keys=[
#                             follower_user_id], back_populates='following')
#     followed = relationship('User', foreign_keys=[
#                             followed_user_id], back_populates='followers')
