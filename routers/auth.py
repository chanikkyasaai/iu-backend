from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from utils.jwt_guard import refresh_access_token

from utils.jwt_guard import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/refresh-token")
def refresh_token(
    refresh_token: str | None = None,
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, detail="User not authenticated.")
            
        if not refresh_token:
            raise HTTPException(
                status_code=401, detail="Refresh token is required.")
        
        # Assuming you have a function to verify and refresh the token
        new_access_token = refresh_access_token(refresh_token)
        
        return {"access_token": new_access_token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to refresh token: {str(e)}"
        )