from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from utils.jwt_guard import get_current_user
from services.get_top_Searches_from_db import get_top_searches_from_db, get_top_departments_from_db, get_top_officials_from_db

router = APIRouter(prefix="/top", tags=["search"])

@router.get("/search")
def get_top_searches(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated.")
        
        # Assuming a function get_top_searches_from_db exists to fetch top searches
        return get_top_searches_from_db(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top searches: {str(e)}")
    
@router.get("/departments")
def get_top_departments(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated.")
        
        # Assuming a function get_top_departments_from_db exists to fetch top departments
        return get_top_departments_from_db(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top departments: {str(e)}")
    
@router.get("/officials")
def get_top_officials(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated.")
        
        # Assuming a function get_top_officials_from_db exists to fetch top officials
        return get_top_officials_from_db(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top officials: {str(e)}")
    