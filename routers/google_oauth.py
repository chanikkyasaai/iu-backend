from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy import Column
from datetime import datetime, timedelta
from services import google_oauth
from utils.db import get_db
from sqlalchemy.orm import Session
from models.user import User
from fastapi import Depends
import logging
from sqlalchemy.exc import SQLAlchemyError

from utils.jwt_guard import REFRESH_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_MINUTES, create_refresh_token, create_access_token

router = APIRouter(prefix="/oauth", tags=["auth"])


@router.get("/login")
async def login():
    url = google_oauth.get_google_auth_url()
    print(url)

    return RedirectResponse(url)


@router.get("/callback")
async def callback(request: Request, code: str, db: Session = Depends(get_db)):
    logger = logging.getLogger(__name__)
    try:
        token_data = await google_oauth.exchange_code_for_token(code)
        user_info = await google_oauth.get_user_info(token_data["access_token"])
        
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token_expires = timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
        
        user_id = user_info.get('sub') or user_info.get('id')
        if not user_id:
            logger.error(
                f"Google user info missing 'id' or 'sub': {user_info}")
            raise HTTPException(
                status_code=400, detail="Google user info did not return an 'id' or 'sub'.")

        user = db.query(User).filter(User.email == user_info["email"]).first()
        if user:
            user.google_id = user_id
        else:
            user = User(
                email=user_info["email"],
                google_id=user_id,
                created_at=datetime.utcnow(),
            )
            db.add(user)
        db.commit()
        db.refresh(user)

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
            },
        )


        refresh_token = create_refresh_token(
            data={
                "sub": str(user.id),
                "email": user.email,
            },
        )
        
        print(
            f"User logged in with Google OAuth and access token: {access_token} \n Refresh token: {refresh_token}")


        response = HTMLResponse()
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True, 
            # Set to True in production (HTTPS)
            samesite="lax",  # Or "strict" or "none" as needed
            max_age=int(access_token_expires.total_seconds())
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            # Set to True in production (HTTPS)
            samesite="lax",  # Or "strict" or "none" as needed
            max_age=int(refresh_token_expires.total_seconds())
        )

        return response

    except HTTPException as http_exc:
        logger.warning(f"HTTPException in OAuth callback: {http_exc.detail}")
        raise http_exc
    except SQLAlchemyError as db_exc:
        logger.error(
            f"Database error in OAuth callback: {str(db_exc)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500, detail="A database error occurred. Please try again.")
    except Exception as exc:
        logger.error(
            f"Unexpected error in OAuth callback: {str(exc)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred during Google login.")
