from datetime import timedelta
from fastapi import APIRouter, Cookie, Response
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from utils.jwt_guard import ACCESS_TOKEN_EXPIRE_MINUTES, refresh_access_token

from utils.jwt_guard import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])

class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/refresh-token")
def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None, alias="refresh_token")
):
    try:
        if not refresh_token:
            raise HTTPException(
                status_code=401, detail="Refresh token is required.")

        new_access_token = refresh_access_token(refresh_token)
        access_token_expires = timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=int(access_token_expires.total_seconds())
        )
        return {"access_token": new_access_token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to refresh token: {str(e)}"
        )        

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Cookies cleared"}
