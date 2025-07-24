from motor.motor_asyncio import AsyncIOMotorClient
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv(".env")

MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(
    MONGO_URL, uuidRepresentation="standard")
db = client["iu"]

# Collections
issue_likes = db["issue_likes"]
issue_supports = db["issue_supports"]
issue_shares = db["issue_shares"]
comment_likes = db["comment_likes"]
thread_supports = db["thread_supports"]
issue_views = db["issue_views"]

async def test_connection():
    try:
        await client.admin.command("ping")
        print("MongoDB connection successful")
    except Exception as e:
        print("MongoDB connection failed:", e)

async def init_indexes():
    # Create indexes for issue_likes
    await issue_likes.create_index([("issue_id", 1), ("user_id", 1)], unique=True)
    
    # Create indexes for issue_supports
    await issue_supports.create_index([("issue_id", 1), ("user_id", 1)], unique=True)
    
    # Create indexes for issue_shares
    await issue_shares.create_index([("issue_id", 1), ("platform", 1)], unique=True)
    
    # Create indexes for comment_likes
    await comment_likes.create_index([("comment_id", 1), ("user_id", 1)], unique=True)
    
    # Create indexes for thread_supports
    await thread_supports.create_index([("thread_id", 1), ("user_id", 1)], unique=True)
    
    # Create indexes for issue_views
    await issue_views.create_index([("issue_id", 1), ("views", 1)], unique=True)
    
    await test_connection()