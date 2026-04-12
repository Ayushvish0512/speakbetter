from fastapi import APIRouter, Depends, HTTPException
from app.routes.auth import get_current_user
from app.services.gemini_service import gemini_service
from app.core.database import get_database
from app.models.schemas import sessionBase
from datetime import datetime
from bson import ObjectId

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import os
import shutil

@router.post("/audio")
async def submit_audio(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    db = get_database()
    
    # Save file temporarily
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Process with Gemini
        analysis = await gemini_service.analyze_audio(file_path)
        
        # Save session
        session_doc = {
            "user_id": current_user["_id"],
            "user_input": analysis.get("transcription", ""),
            "corrected_text": analysis["corrected"],
            "hindi_explanation": analysis["hindi"],
            "feedback": analysis["feedback"],
            "score": analysis["score"],
            "date": datetime.utcnow()
        }
        
        await db["sessions"].insert_one(session_doc)
        
        # Update streak
        today = datetime.utcnow().date()
        last_active = current_user.get("last_active")
        
        new_streak = current_user.get("streak", 0)
        if last_active:
            last_active_date = last_active.date()
            if last_active_date == today:
                pass 
            elif (today - last_active_date).days == 1:
                new_streak += 1
            else:
                new_streak = 1
        else:
            new_streak = 1
            
        await db["users"].update_one(
            {"_id": current_user["_id"]},
            {"$set": {"streak": new_streak, "last_active": datetime.utcnow()}}
        )
        
        analysis["streak"] = new_streak
        return analysis
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/text")
async def submit_text(user_input: str, current_user: dict = Depends(get_current_user)):
    # ... previous logic for text ...
    pass
