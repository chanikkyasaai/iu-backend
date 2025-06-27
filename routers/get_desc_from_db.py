from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from utils.jwt_guard import get_current_user
from services.get_desc_services import get_bottom_departments_from_db, get_bottom_officials_from_db

router = APIRouter(prefix="/bottom", tags=["description"])

@router.get("/departments")
def get_bottom_departments(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated.")
        
        # Assuming a function get_bottom_departments_from_db exists to fetch bottom departments
        return get_bottom_departments_from_db(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch bottom departments: {str(e)}")
    
@router.get("/officials")
def get_bottom_officials(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated.")
        
        # Assuming a function get_bottom_officials_from_db exists to fetch bottom officials
        return get_bottom_officials_from_db(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch bottom officials: {str(e)}")