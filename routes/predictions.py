from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models import PredictionHistory
from database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from auth.jwt_handler import get_current_user

router = APIRouter(prefix="/predictions", tags=["Predictions"])

@router.get("/history/{user_id}", response_model=List[PredictionHistory])
async def get_user_prediction_history(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    # Optional: verify user can only access their own history
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's history"
        )

    cursor = db.predictions.find({"user_id": user_id}).sort("timestamp", -1)
    records = await cursor.to_list(length=1000)

    for record in records:
        record["_id"] = str(record["_id"])

    return records

@router.get("/history", response_model=List[PredictionHistory])
async def get_current_user_history(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id"]
    cursor = db.predictions.find({"user_id": user_id}).sort("timestamp", -1)
    records = await cursor.to_list(length=1000)

    for record in records:
        record["_id"] = str(record["_id"])

    return records