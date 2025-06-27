from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.issue_depts import IssueDept
from models.employee import Employee

def get_bottom_departments_from_db(db: Session, ):
    try:
        bottom_depts = db.query(IssueDept).order_by(IssueDept.negative_count.asc() + IssueDept.positive_count.asc()).limit(3).all()
        return [(dept.dept_name, dept.negative_count + dept.positive_count, dept.state) for dept in bottom_depts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch bottom departments: {str(e)}")

def get_bottom_officials_from_db(db: Session, ):
    try:
        bottom_officials = db.query(Employee).order_by(Employee.negative_count.asc() + Employee.positive_count.asc()).limit(3).all()
        return [(official.name, official.negative_count + official.positive_count, official.state) for official in bottom_officials]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch bottom officials: {str(e)}")