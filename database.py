from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import MONGODB_URL, DATABASE_NAME

# Async MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
predictions_collection = db["predictions"]

# Dependency function for FastAPI
async def get_database() -> AsyncIOMotorDatabase:
    return db

# Startup function to create indexes
async def create_indexes():
    await users_collection.create_index("email", unique=True)
    await predictions_collection.create_index([("user_id", 1), ("timestamp", -1)])