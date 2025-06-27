import datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from schemas.comment import CommentCreate, CommentUpdate
from utils.db import get_db
from utils.jwt_guard import get_current_user
from services.comments.comment_services import (
    fetch_comments_by_issue_id,
    create_comment_in_db,
    update_comment_in_db,
    delete_comment_in_db  
)

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/{issue_id}")
def get_comments(issue_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        return fetch_comments_by_issue_id(issue_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch comments. Please try again later.")
        
@router.post("/")
def create_comment(comment_data: CommentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        return create_comment_in_db(comment_data, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to create comment. Please try again later.")
        
@router.put("/{comment_id}")
def update_comment(comment_id: str, comment_data: CommentUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
            
        return update_comment_in_db(comment_id, comment_data, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update comment. Please try again later.")
        
@router.delete("/{comment_id}")
def delete_comment(comment_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        return delete_comment_in_db(comment_id, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to delete comment. Please try again later.")    
        
@router.post("/{comment_id}/like")
async def like_comment(comment_id: str, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated.")
        
        from utils.mdb import comment_likes  # Import here to avoid circular dependency
        await comment_likes.insert_one({
            "comment_id": comment_id,
            "user_id": user_id,
            "created_at": datetime.datetime.utcnow()
        })
    except Exception:
        raise HTTPException(400, "Already liked")
    
    return {"message": "Liked"}