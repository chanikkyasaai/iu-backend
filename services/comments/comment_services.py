from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.comment import Comment
from schemas.comment import CommentCreate, CommentUpdate

def fetch_comments_by_issue_id(issue_id: str, db: Session):
    try:
        comments = db.query(Comment).filter(Comment.issue_id == issue_id, Comment.is_deleted == False).all()
        comments_reply = []
        for comment in comments:
            replies = db.query(Comment).filter(Comment.parent_id == comment.id, Comment.is_deleted == False).all()
            comments_reply.append({
                "comment": comment,
                "replies": replies
            })
        return comments_reply
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch comments. Please try again later.")


def create_comment_in_db(comment_data: CommentCreate, user_id: str, db: Session):
    try:
        new_comment = Comment(**comment_data.dict(), user_id=user_id)
        new_comment.is_reply = comment_data.is_reply if comment_data.is_reply is not None else False
        new_comment.is_edited = False
        new_comment.is_deleted = False
        if comment_data.is_reply and comment_data.comment_id:
            new_comment.parent_id = comment_data.comment_id
        else:
            new_comment.parent_id = None
        new_comment.created_at = comment_data.created_at if comment_data.created_at else datetime.utcnow()

        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        
        return new_comment
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to create comment. Please try again later.")


def update_comment_in_db(comment_id: str, comment_data: CommentUpdate, user_id: str, db: Session):
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found.")
        for key, value in comment_data.dict().items():
            setattr(comment, key, value)
        
        comment.is_edited = True
        db.commit()
        return comment
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update comment. Please try again later.")


def delete_comment_in_db(comment_id: str, user_id: str, db: Session):
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found.")
        
        comment.is_deleted = True
        db.commit()
        return {"detail": "Comment deleted successfully."}
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to delete comment. Please try again later.")
