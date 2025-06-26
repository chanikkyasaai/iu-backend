from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from schemas.thread import ThreadCreate, ThreadUpdate
from utils.db import get_db
from utils.jwt_guard import get_current_user
from services.threads.thread_services import (
    fetch_threads_by_issue_id,
    create_thread_in_db,
    update_thread_in_db,
    delete_thread_in_db
)

router = APIRouter(prefix="/threads", tags=["threads"])


@router.get("/{issue_id}")
def get_threads(issue_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        return fetch_threads_by_issue_id(issue_id, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to fetch threads. Please try again later.")


@router.post("/")
def create_thread(thread_data: ThreadCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        return create_thread_in_db(thread_data, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to create thread. Please try again later.")


@router.put("/{thread_id}")
def update_thread(thread_id: str, thread_data: ThreadUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        
        thread_data.is_edited = True  # Ensure the thread is marked as edited
        return update_thread_in_db(thread_id, thread_data, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update thread. Please try again later.")


@router.delete("/{thread_id}")
def delete_thread(thread_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
        return delete_thread_in_db(thread_id, user_id, db)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to delete thread. Please try again later.") 
