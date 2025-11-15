from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta, datetime
import joblib
import pandas as pd
import numpy as np

from models import (
    UserSignUp, UserSignIn, Token, UserResponse,
    PredictRequest, PredictResponse
)
from auth import (
    hash_password, verify_password, create_access_token, get_current_user
)
from database import users_collection, predictions_collection
from config import (
    MODEL_PATH, FEATURES_PATH, BENCHMARK_TIME,
    ACCESS_TOKEN_EXPIRE_MINUTES, SCALER_PATH
)

# Initialize FastAPI
app = FastAPI(
    title="Sprinter Prediction API",
    version="2.0.0",
    description="ML-powered sprinter performance prediction with authentication"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model at startup
model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURES_PATH)
scaler = joblib.load(SCALER_PATH)

# ==================== AUTH ENDPOINTS ====================

@app.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(user: UserSignUp):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_dict = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "created_at": pd.Timestamp.utcnow()
    }
    users_collection.insert_one(user_dict)

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signin", response_model=Token)
def signin(user: UserSignIn):
    db_user = users_collection.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=UserResponse)
def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user


# ==================== PREDICTION HELPERS ====================

def build_feature_row(req: PredictRequest) -> pd.DataFrame:
    """Build feature DataFrame from prediction request."""
    row = {col: 0 for col in feature_cols}

    # Set SP_ columns
    for col in feature_cols:
        if col.startswith("SP_"):
            row[col] = req.today_time

    # Set categorical variables
    wt_col = f"Weather_Type_{req.weather_type}"
    tt_col = f"Track_Type_{req.track_type}"
    if wt_col in row:
        row[wt_col] = 1
    if tt_col in row:
        row[tt_col] = 1

    df = pd.DataFrame([row])[feature_cols]

    # Scale SP_ columns
    sp_cols = [col for col in df.columns if col.startswith("SP_")]
    df[sp_cols] = scaler.transform(df[sp_cols])

    return df


def calculate_verdict(gap: float, prob: float) -> str:
    """Determine verdict based on gap and probability."""
    if prob < 0.001:
        return "🔧 No Chance"
    elif prob >= 0.75:
        return "🏅 Likely Winner"
    elif prob >= 0.3:
        return "🥈 Top 3 Potential"
    else:
        return "🔧 Needs Improvement"


# ==================== PREDICTION ENDPOINT ====================

@app.post("/predict", response_model=PredictResponse)
def predict(
        req: PredictRequest,
        current_user: dict = Depends(get_current_user)
):
    try:
        features_df = build_feature_row(req)
        pred_time = float(model.predict(features_df)[0])

        target_date = datetime.strptime(req.target_date, "%Y-%m-%d")
        today = datetime.now()
        horizon_days = (target_date - today).days

        if horizon_days < 0:
            horizon_days = 0
            w_model = 0.0
            w_today = 1.0
        else:
            w_model = np.clip(horizon_days / 365, 0, 1)
            w_today = 1 - w_model

        adjusted_time = w_model * pred_time + w_today * req.today_time

        gap_adj = adjusted_time - BENCHMARK_TIME
        prob_raw = float(1 / (1 + np.exp(5 * gap_adj)))
        prob = prob_raw if prob_raw >= 0.001 else 0.0

        verdict = calculate_verdict(gap_adj, prob)

        response = PredictResponse(
            # predicted_time=round(pred_time, 4),
            adjusted_time=round(adjusted_time, 4),
            benchmark=BENCHMARK_TIME,
            gap=round(gap_adj, 4),
            probability=prob,
            verdict=verdict,
            horizon_days=max(0, horizon_days)
        )

        predictions_collection.insert_one({
            "user_id": current_user["id"],
            "user_email": current_user["email"],
            "input": req.dict(),
            "output": response.dict(),
            "timestamp": pd.Timestamp.utcnow()
        })

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


# ==================== HEALTH CHECK ====================

@app.get("/")
def root():
    return {
        "message": "Sprinter Prediction API",
        "status": "running",
        "version": "2.0.0"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}