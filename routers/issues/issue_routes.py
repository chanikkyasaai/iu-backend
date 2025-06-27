import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.issue import IssueCreate, IssueUpdate
from utils.db import get_db
from services.issues.issue_services import delete_issue_by_id, get_latest_issues, create_issue_in_db, update_issue_in_db
from utils.jwt_guard import get_current_user
from utils.mdb import issue_likes, issue_shares, issue_supports, issue_views

router = APIRouter(prefix="/issues", tags=["issues"])


@router.get("/")
def get_issues(limit: int = 10, cursor: str | None = None, db: Session = Depends(get_db)):
    try:
        return get_latest_issues(cursor=cursor, limit=limit, db=db)
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
        return create_issue_in_db(issue_data, db, user_id)
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
            
        issue_data.is_edited = True  # Ensure is_edited is set to True on update
            
        return update_issue_in_db(issue_id, issue_data, db, user_id)

    except HTTPException as e:
        import logging
        logging.exception(
            "Error updating issue with ID %s: %s", issue_id, str(e))
        raise e
    except Exception as e:
        import logging
        logging.exception("Error updating issue with ID %s: %s", issue_id, str(e))
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
        
@router.post("/{issue_id}/like")
async def like_issue(issue_id: str, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        await issue_likes.insert_one({
            "issue_id": issue_id,
            "user_id": user_id,
            "created_at": datetime.datetime.utcnow()
        })
    except Exception as e:
        import logging
        logging.exception("Error liking issue %s: %s", issue_id, str(e))
        raise HTTPException(400, "Already liked")
    return {"message": "Liked"}

@router.post("/{issue_id}/support")
async def support_issue(issue_id: str, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        await issue_supports.insert_one({
            "issue_id": issue_id,
            "user_id": user_id,
            "created_at": datetime.datetime.utcnow()
        })
    except Exception:
        raise HTTPException(400, "Already supported")
    return {"message": "Supported"}

@router.post("/{issue_id}/{platform}/share")
async def share_issue(issue_id: str, platform: str, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        await issue_shares.insert_one({
            "issue_id": issue_id,
            "user_id": user_id,
            "platform": platform,
            "created_at": datetime.datetime.utcnow()
        })
    except Exception:
        raise HTTPException(400, "Already shared")
    return {"message": "Shared"}


@router.post("/{issue_id}/view")
async def increment_view(issue_id: str):
    try:
        await issue_views.update_one({"issue_id": issue_id},
                                    {"$inc": {"views": 1}},
                                    upsert=True)
        return {"message": "View count incremented"}
    except Exception as e:
        import logging
        logging.exception("Error incrementing view count for issue %s: %s", issue_id, str(e))
        raise HTTPException(status_code=500, detail="Failed to increment view count")


@router.get("/{issue_id}/views")
async def get_issue_with_views(issue_id: str):
    issue = await issue_views.find_one({"issue_id": issue_id})
    if not issue:
        raise HTTPException(404, detail="Issue not found")
    return {
        "issue_id": str(issue["issue_id"]),
        "views": issue.get("views", 0)
    }

@router.get("/{issue_id}/likes")
async def get_issue_likes(issue_id: str):
    try:
        likes = await issue_likes.count_documents({"issue_id": issue_id})
        return {"likes": likes, "issue_id": issue_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch likes: " + str(e))
    
@router.get("/{issue_id}/supports")
async def get_issue_supports(issue_id: str):
    try:
        supports = await issue_supports.count_documents({"issue_id": issue_id})
        return {"supports": supports, "issue_id": issue_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch supports: " + str(e))
    
@router.get("/{issue_id}/shares")
async def get_issue_shares(issue_id: str):
    try:
        shares = await issue_shares.count_documents({"issue_id": issue_id})
        return {"issue_id": issue_id, "platforms": await issue_shares.distinct("platform", {"issue_id": issue_id}), "total_shares": shares}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch shares: " + str(e))