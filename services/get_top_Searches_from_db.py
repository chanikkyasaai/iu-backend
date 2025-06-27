from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.employee import Employee
from models.issue import Issue
from utils import mdb
from models.issue_depts import IssueDept
from sqlalchemy import desc, func

async def get_top_searches_from_db(db: Session):
    try:
        # Top Departments
        top_depts = db.query(IssueDept).order_by(
            desc(IssueDept.negative_count + IssueDept.positive_count)
        ).limit(3).all()

        # Top Locations
        top_loc = db.query(
            Issue.state,
            func.count(Issue.state).label("count")
        ).group_by(Issue.state).order_by(
            func.count(Issue.state).desc()
        ).limit(3).all()

        top_issues_cursor = mdb.issue_views.find(
            {},
            {"_id": 0, "issue_name": 1, "issue_count": 1}
        ).sort("issue_count", -1).limit(3)
        top_issues = await top_issues_cursor.to_list(length=3)

        return {
            "top_depts": [(dept.dept_name, dept.negative_count + dept.positive_count, dept.state) for dept in top_depts],
            "top_locations": [(loc[0], loc[1]) for loc in top_loc],
            "top_issues": [(issue["issue_name"], issue["issue_count"], issue["_id"]) for issue in top_issues]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch top searches: {str(e)}")


def get_top_departments_from_db(db: Session):
    try:
        top_depts = db.query(IssueDept).order_by(
            desc(IssueDept.negative_count + IssueDept.positive_count)
        ).limit(3).all()
        return [(dept.id, dept.dept_name, dept.negative_count + dept.positive_count, dept.state) for dept in top_depts]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch top departments: {str(e)}")


def get_top_officials_from_db(db: Session):
    try:
        top_officials = db.query(Employee).order_by(
            desc(Employee.false_count + Employee.good_count)
        ).limit(3).all()
        return [(official.id, official.name, official.false_count + official.good_count, official.state) for official in top_officials]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch top officials: {str(e)}")
