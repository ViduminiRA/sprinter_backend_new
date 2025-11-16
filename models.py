from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Auth Models
class UserSignUp(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

# Prediction Models
class PredictRequest(BaseModel):
    today_time: float
    weather_type: str
    track_type: str
    target_date: str

class PredictResponse(BaseModel):
    # predicted_time: float
    adjusted_time: float
    benchmark: float
    gap: float
    probability: float
    verdict: str
    horizon_days: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PredictionHistory(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    user_email: EmailStr
    input: PredictRequest
    output: PredictResponse
    timestamp: datetime

    class Config:
        populate_by_name = True