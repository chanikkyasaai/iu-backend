from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.comment import Comment
from schemas.comment import CommentCreate, CommentUpdate
from utils.mdb import comment_likes
from models.profile import Profile

async def fetch_comments_by_issue_id(issue_id: str, db: Session):
    try:
        top_level_comments = db.query(Comment).filter(
            Comment.issue_id == issue_id,
            Comment.is_reply == False,
            Comment.is_deleted == False
        ).order_by(Comment.created_at.desc()).all()

        comments_with_replies = []

        for comment in top_level_comments:
            # Fetch replies to this comment
            replies = db.query(Comment).filter(
                Comment.comment_id == comment.id,
                Comment.is_reply == True,
                Comment.is_deleted == False
            ).all()
            likes = await comment_likes.count_documents({"comment_id": comment.id})
            is_liked = await comment_likes.find_one({"comment_id": comment.id, "user_id": comment.user_id})

            comments_with_replies.append({
                "comment": comment,
                "supports": likes,
                "is_supported": True if is_liked else False,
                "replies": replies
            })

        return comments_with_replies
    except Exception as e:
        import logging
        logging.exception("Exception while fetching comments : %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to fetch comments. Please try again later.")


def create_comment_in_db(comment_data, user_id: str, db: Session):
    try:
        username = db.query(Profile).filter(Profile.user_id == user_id).first()
        
        new_comment = Comment(
            issue_id=comment_data.issue_id,
            username=username.fullname if username else None,
            comment=comment_data.comment,
            is_reply=comment_data.is_reply if comment_data.is_reply is not None else False,
            comment_id=comment_data.comment_id if comment_data.is_reply else None,
            created_at=datetime.utcnow(),
            is_edited=False,
            is_deleted=False,
            user_id=user_id
        )

        if comment_data.is_reply and not comment_data.comment_id:
            raise HTTPException(
                status_code=400, detail="Comment ID is required for replies.")

        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)

        return new_comment
    except Exception as e:
        import logging
        logging.exception("Exception :{e}", e)
        raise HTTPException(
            status_code=500, detail="Failed to create comment. Please try again later.")


def update_comment_in_db(comment_id: str, comment_data: CommentUpdate, user_id: str, db: Session):
    try:
        comment = db.query(Comment).filter(
            Comment.id == comment_id, Comment.user_id == user_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found.")
        for attr, value in comment_data.dict(exclude_unset=True).items():
            setattr(comment, attr, value)

        comment.is_edited = True
        db.commit()
        db.refresh(comment)
        return comment
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update comment. Please try again later.")


def delete_comment_in_db(comment_id: str, user_id: str, db: Session):
    try:
        comment = db.query(Comment).filter(
            Comment.id == comment_id, Comment.user_id == user_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found.")

        comment.is_deleted = True
        db.commit()
        return {"detail": "Comment deleted successfully."}
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to delete comment. Please try again later.")
