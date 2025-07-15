from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from models.profile import Profile
from utils.db import get_db
from sqlalchemy.orm.attributes import flag_modified


def onboard_service(user_data, user_id, db):
    try:
        # Check if user already exists
        existing_user = db.query(Profile).filter(Profile.user_id == user_id).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail="User already onboarded")

        data = Profile(
            user_id=user_id,
            fullname=user_data.fullname,
            role=user_data.role,
            following_users=user_data.following_users or [],
            following_issues=user_data.following_issues or [],
            following_depts=user_data.following_depts or [],
            following_locations=user_data.following_locations or []
        )
        db.add(data)
        db.commit()
        db.refresh(data)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))

    return JSONResponse(content="User onboarded successfully", status_code=200)


def get_profile_service(user_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        return profile

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))


def update_profile_service(user_data, user_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(profile, key, value)

        db.commit()
        db.refresh(profile)

        return JSONResponse(content="Profile updated successfully", status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))
        
def get_following_service(user_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        following_users = profile.following_users if profile.following_users else []
        following_issues = profile.following_issues if profile.following_issues else []
        following_depts = profile.following_depts if profile.following_depts else []
        following_locations = profile.following_locations if profile.following_locations else []
        
        return {
            "following_users": following_users,
            "following_issues": following_issues,
            "following_depts": following_depts,
            "following_locations": following_locations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))
        

def add_following_user(user_id, following_user_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        if profile.following_users is None:
            profile.following_users = []

        if following_user_id not in profile.following_users:
            profile.following_users.append(following_user_id)
            flag_modified(profile, "following_users")
            db.commit()
            db.refresh(profile)

        return JSONResponse(content="Following user added successfully", status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))


def remove_following_user(user_id, following_user_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        if profile.following_users and following_user_id in profile.following_users:
            profile.following_users.remove(following_user_id)
            flag_modified(profile, "following_users")
            db.commit()
            db.refresh(profile)

        return JSONResponse(content="Following user removed successfully", status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))
        
def add_following_issue(user_id, issue_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        if profile.following_issues is None:
            profile.following_issues = []
            
        if issue_id not in profile.following_issues:
            profile.following_issues.append(issue_id)
            flag_modified(profile, "following_issues")
            db.commit()
            db.refresh(profile)

        return JSONResponse(content="Following issue added successfully", status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))
        
def remove_following_issue(user_id, issue_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        if profile.following_issues and issue_id in profile.following_issues:
            profile.following_issues.remove(issue_id)
            flag_modified(profile, "following_issues")
            db.commit()
            db.refresh(profile)

        return JSONResponse(content="Following issue removed successfully", status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))
        
def add_following_dept(user_id, dept_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        if profile.following_depts is None:
            profile.following_depts = []

        if dept_id not in profile.following_depts:
            profile.following_depts.append(dept_id)
            flag_modified(profile, "following_depts")
            db.commit()
            db.refresh(profile)

        return JSONResponse(content="Following department added successfully", status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))
        
def remove_following_dept(user_id, dept_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        if profile.following_depts and dept_id in profile.following_depts:
            profile.following_depts.remove(dept_id)
            flag_modified(profile, "following_depts")
            db.commit()
            db.refresh(profile)

        return JSONResponse(content="Following department removed successfully", status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))
        
def add_following_location(user_id, location_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        if profile.following_locations is None:
            profile.following_locations = []

        if location_id not in profile.following_locations:
            profile.following_locations.append(location_id)
            flag_modified(profile, "following_locations")
            db.commit()
            db.refresh(profile)

        return JSONResponse(content="Following location added successfully", status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))
        
def remove_following_location(user_id, location_id, db):
    try:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        if profile.following_locations and location_id in profile.following_locations:
            profile.following_locations.remove(location_id)
            flag_modified(profile, "following_locations")
            db.commit()
            db.refresh(profile)

        return JSONResponse(content="Following location removed successfully", status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Database error: " + str(e))