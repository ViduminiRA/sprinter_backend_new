import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10080))  # 7 days

# Model paths
MODEL_PATH = os.getenv("MODEL_PATH", "random_forest_model.pkl")
FEATURES_PATH = os.getenv("FEATURES_PATH", "feature_columns.pkl")
# Add to config.py
SCALER_PATH = "sp_scaler.pkl"
EXPLAINER_PATH = "shap_explainer.pkl"


# Prediction defaults
BENCHMARK_TIME = float(os.getenv("BENCHMARK_TIME", 13.0))
