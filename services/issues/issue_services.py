import datetime
from fastapi import Depends, Query, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session
from models.issue import Issue
from utils.db import get_db


def get_latest_issues(
    cursor: str | None = Query(None),  # could be issue.created_at or UUID
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Issue).filter(Issue.is_deleted == False)

        if cursor:
            query = query.filter(Issue.created_at < cursor)

        issues = query.order_by(Issue.created_at.desc()).limit(limit).all()
        return issues
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch issues. Please try again later.")


def create_issue_in_db(issue_data, db: Session, user_id: str):
    try:
        new_issue = Issue(**issue_data.dict(exclude_unset=True), user_id=user_id, created_at=datetime.datetime.utcnow(), is_edited=False, is_deleted=False)

        db.add(new_issue)
        db.commit()
        db.refresh(new_issue)
        return new_issue
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to create issue. Please try again later.")


def delete_issue_by_id(issue_id: str, user_id: str, db: Session):
    try:
        issue = db.query(Issue).filter(Issue.id == issue_id,
                                        Issue.user_id == user_id).first()
        if not issue:
            raise HTTPException(
                status_code=404, detail="Issue not found or unauthorized.")

        issue.is_deleted = True
        db.commit()
        return {"message": "Issue deleted successfully"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to delete issue. Please try again later.")


def update_issue_in_db(issue_id: str, issue_data, db: Session, user_id: str):
    try:
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found.")
        if str(issue.user_id) != user_id:
            raise HTTPException(status_code=403, detail="User not authorized to update this issue.")

        for field, value in issue_data.dict(exclude_unset=True).items():
            setattr(issue, field, value)

        db.commit()
        db.refresh(issue)
        return issue
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update issue. Please try again later.")
