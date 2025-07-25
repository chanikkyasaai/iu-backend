from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import DatabaseError

from schemas.profile import ProfileCreate, ProfileUpdate
from services.profile import add_following_user, get_following_service, get_profile_service, \
    onboard_service, update_profile_service, add_following_issue, add_following_dept, add_following_location, \
    remove_following_dept, remove_following_issue, remove_following_user, remove_following_location
from utils.access_control import require_creator_or_admin
from utils.db import get_db
from utils.jwt_guard import get_current_user

router = APIRouter(prefix="/profile", tags=["onboarding"])

@router.post("/onboard")
def onboard_user(
    user_data: ProfileCreate,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return onboard_service(user_data, user_id, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.get("/")
def get_profile(
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
                
        return get_profile_service(user_id, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.put("/")
def update_profile(
    user_data: ProfileUpdate,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return update_profile_service(user_data, user_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.get('/following')
def get_following(
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        print(user_id)
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return get_following_service(user_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.post('/follow/user/{following_user_id}')
def add_following_u(
    following_user_id: str,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return add_following_user(user_id, following_user_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.post('/follow/issue/{following_issue_id}')
def add_following_i(
    following_issue_id: str,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return add_following_issue(user_id, following_issue_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.post('/follow/dept/{following_dept_id}')
def add_following_d(
    following_dept_id: str,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return add_following_dept(user_id, following_dept_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.post('/follow/location/{following_location_id}')
def add_following(
    following_location_id: str,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return add_following_location(user_id, following_location_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.delete('/follow/user/{following_user_id}')
def remove_following_u(
    following_user_id: str,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return remove_following_user(user_id, following_user_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.delete('/follow/issue/{following_issue_id}')
def remove_following_i(
    following_issue_id: str,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return remove_following_issue(user_id, following_issue_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.delete('/follow/dept/{following_dept_id}')
def remove_following_d(
    following_dept_id: str,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return remove_following_dept(user_id, following_dept_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.delete('/follow/location/{following_location_id}')
def remove_following(
    following_location_id: str,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return remove_following_location(user_id, following_location_id, db)
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))