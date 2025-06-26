from .user import User
from .profile import Profile
from .issue import Issue
from .thread import Thread
from .comment import Comment
from .employee import Employee
# from .follow import Follow
from .issue_depts import IssueDept
from .issue_types import IssueType
from sqlalchemy.orm import relationship

User.profile = relationship("Profile", back_populates="user")
Profile.user = relationship("User", back_populates="profile")

User.issues = relationship("Issue", back_populates="user")
Issue.user = relationship("User", back_populates="issues")

Employee.issues = relationship("Issue", back_populates="employee")
Issue.employee = relationship("Employee", back_populates="issues")

# User.following = relationship("Follow", back_populates="follower")
# Follow.follower = relationship("User", back_populates="following")

# User.followers = relationship("Follow", back_populates="followed")
# Follow.followed = relationship("User", back_populates="followers")