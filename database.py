from pymongo import MongoClient
from config import MONGODB_URL, DATABASE_NAME

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
predictions_collection = db["predictions"]  # Optional: store prediction history

# Create indexes
users_collection.create_index("email", unique=True)