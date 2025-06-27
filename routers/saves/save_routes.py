from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import DatabaseError
from services.saves.saves_services import get_saves_service, save_issue_service, unsave_issue_service
from utils.db import get_db
from utils.jwt_guard import get_current_user
from uuid import UUID

router = APIRouter(prefix = "/save", tags = ["saves"])

@router.get("/")
def get_saves(
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return get_saves_service(user_id, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

@router.post("/{issue_id}")
def save_issue(
    issue_id: str,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return save_issue_service(issue_id, user_id, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    
@router.delete("/{issue_id}")
def unsave_issue(
    issue_id: UUID,
    get_current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        user_id = get_current_user.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        return unsave_issue_service(issue_id, user_id, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))