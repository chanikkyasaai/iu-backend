import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.issue_depts import IssueDept
from schemas.issue import IssueCreate, IssueUpdate, IssueBatchFilterRequest
from typing import Optional
from utils.access_control import require_creator_or_admin
from utils.db import get_db
from services.issues.issue_services import delete_issue_by_id, get_latest_issues, create_issue_in_db, get_latest_issues_admin, update_issue_in_db, get_issue_by_id, get_issues_by_batch_filters
from utils.jwt_guard import get_current_user
from utils.mdb import issue_likes, issue_shares, issue_supports, issue_views

router = APIRouter(prefix="/issues", tags=["issues"])

@router.get("")
async def get_issues(
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    cursor: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    taluk: Optional[str] = None,
    area: Optional[str] = None,
    issue_type: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        if page < 1:
            raise HTTPException(status_code=400, detail="Invalid page number.")
        
        user_id = current_user.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        
        return await get_latest_issues(
            page=page,  
            cursor=cursor,
            limit=limit,
            db=db,
            state=state,
            district=district,
            taluk=taluk,
            area=area,
            issue_type=issue_type,
            department=department,
            user_id = user_id
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch issues. Please try again later."
        )
        
@router.get("/admin&page={page}")
async def get_issues_admin(page: int = 1, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        if page < 1:
            raise HTTPException(status_code=400, detail="Invalid page number.")
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized.")
        return await get_latest_issues_admin(page=page, limit=limit, db=db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch issues. Please try again later.")

@router.post("")
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
        
        issue = get_issue_by_id(issue_id, db)
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found.")

        # Ensure access control (creator or admin)
        require_creator_or_admin(str(issue.user_id))(current_user)
                        
        return update_issue_in_db(issue_id, issue_data, db, str(issue.user_id))

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
            
        issue = get_issue_by_id(issue_id, db)
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found.")

        # Ensure access control (creator or admin)
        require_creator_or_admin(str(issue.user_id))(current_user)
        
        return delete_issue_by_id(issue_id, str(issue.user_id), db)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to delete issue. Please try again later.")
       
@router.get("/alldepts")
def get_all_departments(db: Session = Depends(get_db)):
    try:
        departments = db.query(IssueDept).all()
        
        result = []
        
        for department in departments:            
            result.append({
                "name" : department.dept,
                "id" : department.id
            })
        return result
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch departments. Please try again later.")
       
@router.post("/{issue_id}/like")
async def like_issue(issue_id: str, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        
        if issue_likes.find_one({"issue_id": issue_id, "user_id": user_id}):
            await issue_likes.delete_one({"issue_id": issue_id, "user_id": user_id})
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
        
        found = await issue_supports.find_one({"issue_id": issue_id, "user_id": user_id})
        if found:
            await issue_supports.delete_one({"issue_id": issue_id, "user_id": user_id})
            return {"message": "Unsupported"}
        
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

@router.post("/batch_filter")
async def batch_filter_issues(
    filters: IssueBatchFilterRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        return await get_issues_by_batch_filters(
            db=db,
            user_ids=[str(uid) for uid in filters.user_ids] if filters.user_ids else None,
            dept_ids=[str(did) for did in filters.dept_ids] if filters.dept_ids else None,
            issue_ids=[str(iid) for iid in filters.issue_ids] if filters.issue_ids else None,
            states=filters.states,
            districts=filters.districts,
            taluks=filters.taluks,
            villages=filters.villages,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to batch filter issues. Please try again later.")