from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user
from app.core.database import get_database
from typing import List

router = APIRouter()

@router.get("/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    return {
        "name": current_user["name"],
        "streak": current_user.get("streak", 0),
        "last_active": current_user.get("last_active")
    }

@router.get("/history")
async def get_user_history(current_user: dict = Depends(get_current_user)):
    db = get_database()
    cursor = db["sessions"].find({"user_id": current_user["_id"]}).sort("date", -1).limit(10)
    history = await cursor.to_list(length=10)
    
    # Convert ObjectId and datetime for JSON serialization
    for session in history:
        session["_id"] = str(session["_id"])
        session["user_id"] = str(session["user_id"])
        session["date"] = session["date"].isoformat()
        
    return history
