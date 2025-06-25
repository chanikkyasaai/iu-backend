from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.issue import IssueCreate, IssueUpdate
from utils.db import get_db
from services.issues.issue_services import delete_issue_by_id, get_latest_issues, create_issue_in_db, update_issue_in_db
from utils.jwt_guard import get_current_user

router = APIRouter(prefix="/issues", tags=["issues"])


@router.get("/")
def get_issues():
    try:
        return get_latest_issues()
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch issues. Please try again later.")


@router.post("/")
def create_issue(issue_data: IssueCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        issue_data.user_id = user_id
        return create_issue_in_db(issue_data, db)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to create issue. Please try again later.")


@router.put("/{issue_id}")
def update_issue(issue_id: str, issue_data: IssueUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        if issue_data.user_id == user_id:
            return update_issue_in_db(issue_id, issue_data, db)
        else:
            raise HTTPException(
                status_code=403, detail="User not authorized to update this issue.")
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update issue. Please try again later.")


@router.delete("/{issue_id}")
def delete_issue(issue_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        return delete_issue_by_id(issue_id, user_id, db)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to delete issue. Please try again later.")
        
