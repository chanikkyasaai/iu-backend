from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from models.employee import Employee
from models.issue import Issue
from utils import mdb
from utils.db import get_db
from models.issue_depts import IssueDept


def get_top_searches_from_db(db: Session, ):
    try:
        top_depts = db.query(IssueDept).order_by(IssueDept.negative_count.desc() + IssueDept.positive_count.desc()).limit(3).all()

        top_loc = db.query(Issue.state).group_by(Issue.state).order_by(
            Issue.state.count().desc()).limit(3).all()
        
        top_issues = mdb.issue_supports.aggregate([
            {"$group": {"_id": "$issue_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 3}
        ])
        
        return {
            "top_depts": [(dept.dept_name, dept.negative_count + dept.positive_count, dept.state) for dept in top_depts],
            "top_locations": [(loc.state, loc.count) for loc in top_loc],
            "top_issues": [top_issues ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top searches: {str(e)}")

def get_top_departments_from_db(db: Session, ):
    try:
        top_depts = db.query(IssueDept).order_by(IssueDept.negative_count.desc() + IssueDept.positive_count.desc()).limit(3).all()
        return [(dept.dept_name, dept.negative_count + dept.positive_count, dept.state) for dept in top_depts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top departments: {str(e)}")
    
def get_top_officials_from_db(db: Session, ):
    try:
        top_officials = db.query(Employee).order_by(
            Employee.negative_count.desc() + Employee.positive_count.desc()).limit(3).all()
        return [(official.name, official.negative_count + official.positive_count, official.state) for official in top_officials]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top officials: {str(e)}")