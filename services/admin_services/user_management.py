from fastapi import HTTPException
from models.issue import Issue
from models.user import User
from models.profile import Profile
from sqlalchemy.orm import Session
from utils.mdb import db as mdb

async def get_all_users_service(page: int, limit:int, db):
    try:
        offset = (page - 1) * limit
        users = db.query(User).offset(offset).limit(limit).all()
        
        result = []
        for user in users:
            profile = db.query(Profile).filter(Profile.user_id == user.id).first()
            
            issues = db.query(Issue).filter(Issue.user_id == user.id)
            user_issue_supports = 0
            issues_count = 0
            
            for issue in issues:
                user_issue_supports = user_issue_supports + await mdb.issue_supports.count_documents({"issue_id": str(issue.id)})
                issues_count += int(1)
            
            result.append({"user": user, "profile": profile, "role": profile.role,
                            "issue_submitted": issues_count, "user_supports": user_issue_supports})

        return result
    except Exception as e:
        import logging
        logging.exception("Exception while fetching users : %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to fetch users. Please try again later.")
        

def get_user_stats_service(db):
    try:
        users_count = db.query(Profile).count()
        
        del_users = db.query(Profile).filter(
            Profile.is_deleted == -1).count()
        
        return {"total_users": users_count, "suspended_users": del_users}
    except Exception as e:
        import logging
        logging.exception("Exception while fetching users : %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to fetch users. Please try again later.")
        
def update_user_in_db(user_id: str, user_data, db: Session):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="User not found.")
        
        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(profile, field, value)
        
        db.commit()
        db.refresh(profile)
        return profile
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update user. Please try again later.")
        
def suspend_user_in_db(user_id: str, db: Session):
    try:
        user = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        user.is_deleted = -1
        db.commit()
        db.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to suspend user. Please try again later.")