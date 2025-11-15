from datetime import timedelta

# ----------------------------
# MongoDB Configuration
# ----------------------------
MONGODB_URL = "mongodb+srv://samxgan_db_user:vidumini123@cluster0.vkm95my.mongodb.net/"
DATABASE_NAME = "sprinter_app"

# ----------------------------
# JWT Configuration
# ----------------------------
SECRET_KEY = "supersecretkey12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days

# ----------------------------
# Model paths
# ----------------------------
MODEL_PATH = "random_forest_model.pkl"
FEATURES_PATH = "feature_columns.pkl"
SCALER_PATH = "sp_scaler.pkl"
EXPLAINER_PATH = "shap_explainer.pkl"

# ----------------------------
# Prediction defaults
# ----------------------------
BENCHMARK_TIME = 13.0
