# database.py

from pymongo import MongoClient
from config import MONGODB_URL, DATABASE_NAME

# --- Connection Check ---
# Check for None explicitly. This will cause an immediate failure if the
# Railway environment variables weren't correctly loaded into os.environ.

if MONGODB_URL is None or MONGODB_URL == "mongodb://localhost:27017/":
    raise EnvironmentError(
        "MONGODB_URL environment variable is not set. Cannot connect to database."
    )

if DATABASE_NAME is None or DATABASE_NAME == "local_sprinter_app":
     raise EnvironmentError(
        "DATABASE_NAME environment variable is not set. Cannot select database."
    )

# --- Top-Level Connection ---
# This will execute upon import, but the explicit checks above ensure
# MONGODB_URL and DATABASE_NAME are strings.

try:
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
except Exception as e:
    # Catch any connection errors (e.g., bad URL format) immediately
    print(f"FATAL: Could not connect to MongoDB: {e}")
    raise e


# --- Collections ---
users_collection = db["users"]
predictions_collection = db["predictions"]

# --- Indexes (This is okay to run at top level) ---
try:
    users_collection.create_index("email", unique=True)
except Exception as e:
    # Log the error but don't stop the worker boot if indexing fails
    print(f"Warning: Failed to create index on users collection: {e}")