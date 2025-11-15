# config.py

import os
from datetime import timedelta
from dotenv import load_dotenv

# --- Environment Variable Loading ---
# This line loads variables from a local .env file when developing locally.
# It does NOTHING when run on Railway, as the variables are injected by the platform.
load_dotenv() 

# --- MongoDB Configuration ---
# Use os.getenv/os.environ.get for all variables for consistency.
# Note: In production (Railway), the default values are IGNORED.
MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://localhost:27017/") 
DATABASE_NAME = os.environ.get("DATABASE_NAME", "local_sprinter_app") 

# --- JWT Configuration ---
# Ensure these have sane defaults or check for None later if they are critical.
SECRET_KEY = os.getenv("SECRET_KEY", "default_local_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
# Convert to int safely, relying on Railway to provide a valid value.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10080))

# --- Model Paths ---
MODEL_PATH = os.getenv("MODEL_PATH", "random_forest_model.pkl")
FEATURES_PATH = os.getenv("FEATURES_PATH", "feature_columns.pkl")
SCALER_PATH = os.getenv("SCALER_PATH", "sp_scaler.pkl")
EXPLAINER_PATH = os.getenv("EXPLAINER_PATH", "shap_explainer.pkl")

# --- Prediction defaults ---
BENCHMARK_TIME = float(os.getenv("BENCHMARK_TIME", 13.0))