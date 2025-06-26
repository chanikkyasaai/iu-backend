import datetime
from models.thread import Thread
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException


def fetch_threads_by_issue_id(issue_id: str, user_id: str, db: Session):
    try:
        if not issue_id:
            raise HTTPException(
                status_code=400, detail="Issue ID is required.")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required.")

        stmt = select(Thread).where(Thread.issue_id == issue_id,
                                    Thread.is_deleted == False).order_by(Thread.created_at.desc())
        result = db.execute(stmt)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch threads. Please try again later.")


def create_thread_in_db(thread_data, user_id: str, db: Session):
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required.")

        new_thread = Thread(
            issue_id=thread_data.issue_id,
            thread_headline=thread_data.thread_headline,
            thread_desc=thread_data.thread_desc,
            thread_type=thread_data.thread_type,
            created_at=thread_data.created_at or datetime.datetime.utcnow(),
            is_edited=thread_data.is_edited or False,
            is_deleted=thread_data.is_deleted or False,
            evidence_url=thread_data.evidence_url
        )
        db.add(new_thread)
        db.commit()
        db.refresh(new_thread)
        return new_thread
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to create thread. Please try again later.")


def update_thread_in_db(thread_id: str, thread_data, user_id: str, db: Session):
    try:
        if not thread_id:
            raise HTTPException(
                status_code=400, detail="Thread ID is required.")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required.")

        thread = db.query(Thread).filter(
            Thread.id == thread_id, Thread.is_deleted == False).first()
        if not thread:
            raise HTTPException(
                status_code=404, detail="Thread not found or has been deleted.")

        for key, value in thread_data.dict(exclude_unset=True).items():
            setattr(thread, key, value)

        db.commit()
        db.refresh(thread)
        return thread
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update thread. Please try again later.")


def delete_thread_in_db(thread_id: str, user_id: str, db: Session):
    try:
        if not thread_id:
            raise HTTPException(
                status_code=400, detail="Thread ID is required.")
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required.")

        stmt = select(Thread).where(
            Thread.id == thread_id, Thread.is_deleted == False)
        thread = db.execute(stmt).scalar_one_or_none()
        if not thread:
            raise HTTPException(
                status_code=404, detail="Thread not found or has been deleted.")

        thread.is_deleted = True
        db.commit()
        return {"message": "Thread deleted successfully."}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to delete thread. Please try again later.")
