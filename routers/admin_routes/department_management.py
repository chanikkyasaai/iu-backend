from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.issue_dept_officers import IssueDeptOfficerCreate, IssueDeptOfficerUpdate
from schemas.issue_depts import IssueDeptCreate, IssueDeptUpdate
from services.admin_services.department_management import create_department_in_db, update_department_in_db, add_officer_to_department_in_db,\
    delete_officer_in_db, delete_department_in_db, update_officer_in_department_in_db, get_departments_from_db
from utils.db import get_db
from utils.jwt_guard import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/department")
def create_department(department_data: IssueDeptCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        
        return create_department_in_db(department_data, db, user_id)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to create department. Please try again later.")
        
@router.put("/department/{department_id}")
def update_department(department_id: str, department_data: IssueDeptUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        
        return update_department_in_db(department_id, department_data, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update department. Please try again later.")
        
@router.post("/department/{department_id}/officer")
def add_officer_to_department(department_id: str, officer_data: IssueDeptOfficerCreate,
                    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        
        return add_officer_to_department_in_db(department_id, officer_data, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to add officer to department. Please try again later.")

@router.put("/department/{department_id}/officer/{officer_id}")
def update_officer_in_department(department_id: str, officer_id: str, 
                    officer_data: IssueDeptOfficerUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        
        return update_officer_in_department_in_db(department_id, officer_id, officer_data, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update officer in department. Please try again later.")
        
@router.delete("/department/{department_id}")
def delete_department(department_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        
        return delete_department_in_db(department_id, user_id, db)
    except Exception as e:
        raise e
        
@router.delete("/officer/{officer_id}")
def delete_officer(officer_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        
        return delete_officer_in_db(officer_id, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to delete officer. Please try again later.")

@router.get("/departments")
def get_departments(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated.")
        
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        
        return get_departments_from_db(db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch departments. Please try again later.")