from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Body, Cookie, Response
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from utils.jwt_guard import ACCESS_TOKEN_EXPIRE_MINUTES, refresh_access_token, REFRESH_TOKEN_EXPIRE_DAYS

from utils.jwt_guard import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


class RefreshTokenRequest(BaseModel):
    refresh_token: Optional[str] = None


@router.post("/refresh-token")
def refresh_token(
    response: Response,
    data: RefreshTokenRequest = Body(default=None),
    refresh_token_cookie: Optional[str] = Cookie(
        default=None, alias="refresh_token"),
):
    try:
        # Prefer cookie, fallback to body
        refresh_token = refresh_token_cookie or (
            data.refresh_token if data else None)
        if not refresh_token:
            raise HTTPException(
                status_code=401, detail="Refresh token is required."
            )

        # ... your logic to refresh ...
        new_access_token = refresh_access_token(refresh_token)
        access_token_expires = timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token_expires = timedelta(
            days=int(REFRESH_TOKEN_EXPIRE_DAYS)
        )

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=int(access_token_expires.total_seconds())
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=int(refresh_token_expires.total_seconds())
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
