from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import dotenv
import os

dotenv.load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(str(DATABASE_URL))
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
