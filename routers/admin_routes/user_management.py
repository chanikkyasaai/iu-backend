from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import DatabaseError
from schemas.profile import ProfileUpdate
from services.admin_services.user_management import get_all_users_service, get_user_stats_service, suspend_user_in_db, update_user_in_db
from utils.jwt_guard import get_current_user
from utils.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users&page={page}")
async def get_all_users(page: int = 1, limit: int = 10, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if page < 1:
            raise HTTPException(status_code=400, detail="Invalid page number.")
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        return await get_all_users_service(page=page, limit=limit, db=db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch users. Please try again later.")
        
@router.get("/total-stats")
def get_user_stats(current_user: dict= Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        return get_user_stats_service(db=db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch users. Please try again later.")
        
@router.put("/update-user/{user_id}")
def update_user(user_id: str, user_data: ProfileUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        
        return update_user_in_db(user_id, user_data, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update user. Please try again later.")
        
@router.delete("/suspend-user/{user_id}")
def suspend_user(user_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        
        return suspend_user_in_db(user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to suspend user. Please try again later.")