from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.issue import Issue
from models.issue_dept_officers import IssueDeptOfficer
from models.issue_depts import IssueDept
from fastapi import HTTPException

from models.user import User

def create_department_in_db(department_data, db: Session, user_id):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        new_department = IssueDept(**department_data.dict(exclude_unset=True), user_id=user_id)
        
        db.add(new_department)
        db.commit()
        db.refresh(new_department)
        
        return JSONResponse(status_code=201, content={"message": "Department created successfully"})
    except Exception as e:
        import logging
        logging.exception("Error creating department: %s", str(e))
        raise HTTPException(
            status_code=500, detail="Failed to create department. Please try again later.")
        
def update_department_in_db(department_id, department_data, user_id, db: Session):
    try:
        department = db.query(IssueDept).filter(
            IssueDept.id == department_id).first()
        
        if not department:
            raise HTTPException(status_code=404, detail="Department not found.")
        
        if str(department.user_id) != str(user_id):
            raise HTTPException(status_code=403, detail="User not authorized to update this department.")
        
        for field, value in department_data.dict(exclude_unset=True).items():
            setattr(department, field, value)

        db.commit()
        db.refresh(department)
        return department
    except Exception as e:
        import logging
        logging.exception("Error updating department: %s", str(e))
        raise HTTPException(
            status_code=500, detail="Failed to update department. Please try again later.")
        
def delete_department_in_db(department_id, user_id, db: Session):
    try:
        department = db.query(IssueDept).filter(
            IssueDept.id == department_id).first()
        
        officers = db.query(IssueDeptOfficer).filter(
            IssueDeptOfficer.dept_id == department_id).all()
        
        if officers:
            raise HTTPException(status_code=400, detail="Cannot delete department with officers.")
        
        if not department:
            raise HTTPException(status_code=404, detail="Department not found.")
        
        if str(department.user_id) != str(user_id):
            raise HTTPException(status_code=403, detail="User not authorized to delete this department.")
        
        db.delete(department)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Department deleted successfully"})
    except Exception as e:
        import logging
        logging.exception("Error deleting department: %s", str(e))
        raise HTTPException(
            status_code=500, detail="Failed to delete department. Please try again later.")
        
def add_officer_to_department_in_db(department_id, officer_data, user_id, db: Session):
    try:
        department = db.query(IssueDept).filter(
            IssueDept.id == department_id).first()
        
        if not department:
            raise HTTPException(status_code=404, detail="Department not found.")
        
        new_officer = IssueDeptOfficer(
            **officer_data.dict(exclude_unset=True), user_id=user_id, dept_id=department_id)
        
        db.add(new_officer)
        db.commit()
        db.refresh(new_officer)
        
        return JSONResponse(status_code=201, content={"message": "Officer added to department successfully"})
    except Exception as e:
        import logging
        logging.exception("Error adding officer to department: %s", str(e))
        raise HTTPException(
            status_code=500, detail="Failed to add officer to department. Please try again later.")
        
def update_officer_in_department_in_db(department_id, officer_id, officer_data, user_id, db: Session):
    try:
        department = db.query(IssueDept).filter(IssueDept.id == department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found.")
        
        officer = db.query(IssueDeptOfficer).filter(
            IssueDeptOfficer.id == officer_id).first()
        
        if not officer:
            raise HTTPException(status_code=404, detail="Officer not found.")
        
        if str(officer.user_id) != str(user_id):
            raise HTTPException(status_code=403, detail="User not authorized to update this officer.")
        
        for field, value in officer_data.dict(exclude_unset=True).items():
            setattr(officer, field, value)

        db.commit()
        db.refresh(officer)
        return officer
    except Exception as e:
        import logging
        logging.exception("Error updating officer in department: %s", str(e))
        raise HTTPException(
            status_code=500, detail="Failed to update officer in department. Please try again later.")
        
def delete_officer_in_db(officer_id, user_id, db: Session):
    try:
        officer = db.query(IssueDeptOfficer).filter(
            IssueDeptOfficer.id == officer_id).first()
        
        if not officer:
            raise HTTPException(status_code=404, detail="Officer not found.")
        
        if str(officer.user_id) != str(user_id):
            raise HTTPException(status_code=403, detail="User not authorized to delete this officer.")
        
        db.delete(officer)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Officer deleted successfully"})
    except Exception as e:
        import logging
        logging.exception("Error deleting officer: %s", str(e))
        raise HTTPException(
            status_code=500, detail="Failed to delete officer. Please try again later.")
        
def get_departments_from_db(db: Session):
    try:
        departments = db.query(IssueDept).all()
        
        results = []
        
        for department in departments:
            officers = db.query(IssueDeptOfficer).filter(
                IssueDeptOfficer.dept_id == department.id).all()
            
            pending_issues = db.query(Issue).filter(
                Issue.dept_id == department.id, Issue.current_status == "Pending").count()
            
            resolved_issues = db.query(Issue).filter(
                Issue.dept_id == department.id, Issue.current_status == "Resolved").count()
            
            score = db.query(IssueDept).filter(IssueDept.id == department.id).first()
            
            if not score:
                raise HTTPException(status_code=404, detail="Score not found.")
            
            corruption_score = (score.negative_count/(score.negative_count + score.positive_count)) * 100
            
            results.append({
                "department" : department,
                "officers" : officers,
                "pending_issues" : pending_issues,
                "resolved_issues" : resolved_issues,
                "corruption_score" : corruption_score,
                "total_issues" : score.negative_count + score.positive_count
            })
        
        return results
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch departments. Please try again later.")