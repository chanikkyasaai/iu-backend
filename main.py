from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from sqlalchemy import text

from utils.db import get_db

from routers.comments.comment_routes import router as comment_router
from routers.threads.thread_routes import router as thread_router
from routers.issues.issue_routes import router as issue_router
from routers.auth import router as auth_router
from routers.profile import router as profile_router
from routers.google_oauth import router as google_oauth_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


def test_db():
    import logging

    logging.basicConfig(level=logging.INFO)
    logging.info("Testing database connection...")

    try:
        db_gen = get_db()             # This is a generator
        # Get the actual session (or connection) from it
        db = next(db_gen)
        result = db.execute(text("SELECT 1;"))  # SQLAlchemy Session.execute
        db_gen.close()                # Clean up the generator

        logging.info(result)
        if result.scalar() == 1:
            logging.info("Database connection successful.")
            return {"db_status": "connected"}
        else:
            logging.error("Database test query failed.")
            return {"db_status": "disconnected"}

    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return {"db_status": "error", "detail": str(e)}

test_db()  # Call the test function to check DB connection

app.include_router(google_oauth_router)
app.include_router(profile_router)
app.include_router(auth_router)
app.include_router(issue_router)
app.include_router(thread_router)
app.include_router(comment_router)