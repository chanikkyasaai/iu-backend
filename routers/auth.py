from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from utils.jwt_guard import refresh_access_token

from utils.jwt_guard import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/refresh-token")
def refresh_token(
    refresh_token: RefreshTokenRequest,
):
    try:
        if not refresh_token:
            raise HTTPException(
                status_code=401, detail="Refresh token is required.")
        
        # Assuming you have a function to verify and refresh the token
        new_access_token = refresh_access_token(refresh_token.refresh_token)
        
        return {"access_token": new_access_token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to refresh token: {str(e)}"
        )