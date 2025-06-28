# utils/access_control.py

from fastapi import Depends, HTTPException, status
from utils.jwt_guard import get_current_user


def require_creator_or_admin(resource_owner_id: str):
    def _authorize(current_user: dict = Depends(get_current_user)):
        import logging
        logging.info(current_user)
        if current_user.get("role") == "admin" or current_user.get("sub") == resource_owner_id:
            return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    return _authorize
