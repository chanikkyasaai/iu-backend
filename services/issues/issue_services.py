import datetime
from fastapi import Depends, Query, HTTPException
from sqlalchemy import UUID, update
from sqlalchemy.orm import Session
from models.issue import Issue
from models.save import Save
from utils import mdb
from utils.db import get_db


async def get_latest_issues(
    page: int,
    cursor: str | None,
    limit: int,
    db: Session,
    state: str | None = None,
    district: str | None = None,
    taluk: str | None = None,
    area: str | None = None,
    issue_type: str | None = None,
    department: str | None = None,
    user_id: str | None = None
):
    try:
        query = db.query(Issue).filter(Issue.is_deleted == False)

        if cursor:
            try:
                cursor_dt = datetime.datetime.fromisoformat(cursor)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Invalid cursor format. Use ISO format.")
            query = query.filter(Issue.issue_time < cursor_dt)

        if state:
            query = query.filter(Issue.state == state)
        if district:
            query = query.filter(Issue.district == district)
        if taluk:
            query = query.filter(Issue.taluk == taluk)
        if area:
            query = query.filter(Issue.village == area)
        if issue_type:
            query = query.filter(Issue.issue_type == issue_type)
        if department:
            query = query.filter(Issue.dept == department)

        # Ensure latest issues come first by ordering by issue_time DESC
        issues = (
            query.order_by(Issue.created_at.desc())
            .limit(limit)
            .offset((page - 1) * limit)
            .all()
        )

        result = []

        for issue in issues:
            issue_views = await mdb.issue_views.count_documents({"issue_id": str(issue.id)})
            issue_support = await mdb.issue_supports.count_documents({"issue_id": str(issue.id)})
            issue_shares = await mdb.issue_shares.count_documents({"issue_id": str(issue.id)})
            issue_likes = await mdb.issue_likes.count_documents({"issue_id": str(issue.id)})

            is_saved = db.query(Save).filter(Save.issue_id == issue.id).first()
            issue_saved = True if is_saved else False

            is_supported = await mdb.issue_supports.find_one({"issue_id": str(issue.id), "user_id": str(user_id)})
            issue_supported = True if is_supported else False

            result.append({
                "issue": issue,
                "views": issue_views,
                "supports": issue_support,
                "shares": issue_shares,
                "likes": issue_likes,
                "is_saved": issue_saved,
                "is_supported": issue_supported
            })

        return result
    except Exception as e:
        import logging
        logging.exception("Exception while fetching issues : %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to fetch issues. Please try again later."
        )


async def get_latest_issues_admin(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    try:
        offset = (page - 1) * limit

        query = (
            db.query(Issue)
            .filter(Issue.is_deleted == False)
            .order_by(Issue.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        issues = query.all()
        result = []
        for issue in issues:
            total_supports = await mdb.issue_supports.count_documents(
                {"issue_id": str(issue.id)})
            result.append({"issue": issue, "supports": total_supports})
        return result
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch issues. Please try again later.")


def create_issue_in_db(issue_data, db: Session, user_id: str):
    try:

        new_issue = Issue(**issue_data.dict(exclude_unset=True), user_id=user_id)

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
            raise HTTPException(
                status_code=403, detail="User not authorized to update this issue.")

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


def get_issue_by_id(issue_id: str, db: Session):
    try:
        issue = db.query(Issue).filter(Issue.id == issue_id,
                                       Issue.is_deleted == False).first()
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found.")
        return issue
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch issue. Please try again later.")
