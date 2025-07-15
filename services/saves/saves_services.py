import datetime


def save_issue_service(issue_id, user_id, db):
    """
    
    :param issue_id: UUID of the issue to save or unsave.
    :param user_id: UUID of the user performing the action.
    :param db: Database session.
    :return: Success message or error message.
    """
    from models.save import Save  # Import here to avoid circular dependency
    from sqlalchemy.exc import IntegrityError

    try:
        from models.issue import Issue  # Import here to avoid circular dependency
        from models.user import User  # Import here to avoid circular dependency
        
        found = db.query(Save).filter(Save.issue_id == issue_id, Save.user_id == user_id).first()
        if found:
            db.delete(found)
            db.commit()
            return {"error": "Issue unsaved."}

        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if not issue:
            return {"error": "Issue not found."}

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "User not found."}

        save = Save(issue_id=issue_id, user_id=user_id, created_at=datetime.datetime.utcnow())
        db.add(save)
        db.commit()
        return {"message": "Issue saved successfully."}
    except IntegrityError:
        db.rollback()
        return {"error": "Issue already saved by user."}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
def get_saves_service(user_id, db):
    """
    Retrieve all saved issues for a user.

    :param user_id: UUID of the user.
    :param db: Database session.
    :return: List of saved issues or error message.
    """
    from models.save import Save  # Import here to avoid circular dependency
    from models.issue import Issue  # Import here to avoid circular dependency

    try:
        saves = db.query(Save).filter(Save.user_id == user_id).all()
        if not saves:
            return {"message": "No saved issues found."}

        saved_issues = [db.query(Issue).filter(Issue.id == save.issue_id).first() for save in saves]
        return {"saved_issues": saved_issues}
    except Exception as e:
        return {"error": str(e)}
    
def unsave_issue_service(issue_id, user_id, db):
    """
    Unsave an issue for a user.

    :param issue_id: UUID of the issue to unsave.
    :param user_id: UUID of the user performing the action.
    :param db: Database session.
    :return: Success message or error message.
    """
    from models.save import Save  # Import here to avoid circular dependency

    try:
        save = db.query(Save).filter(Save.issue_id == issue_id, Save.user_id == user_id).first()
        if not save:
            return {"error": "Save not found."}

        db.delete(save)
        db.commit()
        return {"message": "Issue unsaved successfully."}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}