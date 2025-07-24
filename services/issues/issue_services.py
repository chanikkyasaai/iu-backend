import datetime
from fastapi import Depends, Query, HTTPException
from sqlalchemy import UUID, update, or_
from sqlalchemy.orm import Session
from models.issue import Issue
from models.issue_depts import IssueDept
from models.profile import Profile
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


from sqlalchemy import or_

async def get_issues_by_batch_filters(
    db: Session,
    user_ids: list[str] = None,
    dept_ids: list[str] = None,
    issue_ids: list[str] = None,
    states: list[str] = None,
    districts: list[str] = None,
    taluks: list[str] = None,
    villages: list[str] = None,
):
    try:
        query = db.query(Issue).filter(Issue.is_deleted == False)
        conditions = []
        if user_ids:
            conditions.append(Issue.user_id.in_(user_ids))
        if dept_ids:
            conditions.append(Issue.dept_id.in_(dept_ids))
        if issue_ids:
            conditions.append(Issue.id.in_(issue_ids))
        if states:
            conditions.append(Issue.state.in_(states))
        if districts:
            conditions.append(Issue.district.in_(districts))
        if taluks:
            conditions.append(Issue.taluk.in_(taluks))
        if villages:
            conditions.append(Issue.village.in_(villages))
        if conditions:
            query = query.filter(or_(*conditions))
        issues = query.order_by(Issue.created_at.desc()).all()
        result = []
        for issue in issues:
            # Determine which filter(s) matched
            matched_on = []
            if user_ids and str(issue.user_id) in user_ids:
                matched_on.append("user_id")
            if dept_ids and str(issue.dept_id) in dept_ids:
                matched_on.append("dept_id")
            if issue_ids and str(issue.id) in issue_ids:
                matched_on.append("issue_id")
            if states and issue.state in states:
                matched_on.append("state")
            if districts and issue.district in districts:
                matched_on.append("district")
            if taluks and issue.taluk in taluks:
                matched_on.append("taluk")
            if villages and issue.village in villages:
                matched_on.append("village")
            
            issue_author_profile = db.query(Profile).filter(
                Profile.user_id == issue.user_id).first()
            issue_author = issue_author_profile.fullname if issue_author_profile else None

            dept_name = db.query(IssueDept).filter(
                IssueDept.id == issue.dept_id).first()
            issue_dept_name = dept_name.dept if dept_name else None

            issue_views = await mdb.issue_views.count_documents({"issue_id": str(issue.id)})
            issue_support = await mdb.issue_supports.count_documents({"issue_id": str(issue.id)})
            issue_shares = await mdb.issue_shares.count_documents({"issue_id": str(issue.id)})
            issue_likes = await mdb.issue_likes.count_documents({"issue_id": str(issue.id)})
            is_saved = db.query(Save).filter(Save.issue_id == issue.id).first()
            issue_saved = True if is_saved else False
            result.append({
                "issue": {
                    "id": str(issue.id),
                    "issue_headline": issue.issue_headline,
                    "issue_desc": issue.issue_desc,
                    "issue_type": issue.issue_type,
                    "created_at": str(issue.created_at),
                    "current_status": issue.current_status,
                    "user_id": issue.user_id,
                    "dept_id": issue.dept_id,
                    "district": issue.district,
                    "state": issue.state,
                    "taluk": issue.taluk,
                    "village": issue.village,
                    "author_name": issue_author or "Unknown",
                    "issue_dept": issue_dept_name or "Unknown",
                    "is_anonymous": issue.is_anonymous,
                    "is_edited": issue.is_edited,
                },
                "views": issue_views,
                "supports": issue_support,
                "shares": issue_shares,
                "likes": issue_likes,
                "is_saved": issue_saved,
                "matched_on": matched_on,
            })

        return result
    except Exception as e:
        import logging
        logging.exception("Exception while batch filtering issues : %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to fetch issues. Please try again later."
        )


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
