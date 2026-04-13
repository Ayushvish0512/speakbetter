from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user
from app.core.database import get_database
from datetime import datetime
from app.services.gemini_service import gemini_service
import json

router = APIRouter()

@router.get("/")
async def get_daily_task(current_user: dict = Depends(get_current_user)):
    db = get_database()
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Check if task exists for today
    task = await db["tasks"].find_one({"date": today_str})
    
    if not task:
        # Generate a new task using Gemini (or use a predefined list)
        prompt = """
        You are a Language Learning Assistant. Generate a simple daily English speaking challenge for a Hindi speaker.
        The task must be related to daily life, professional skills, or travel.
        Example: "Describe your favorite childhood memory" or "How do you handle a busy day at work?".
        Return EXACTLY this JSON format (no markdown):
        {"task_en": "Task in English", "task_hi": "Task in Hindi"}
        """
        
        try:
            response = await gemini_service.generate_with_retry(
                model=gemini_service.analysis_model,
                contents=prompt
            )
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            task_data = json.loads(text)
        except Exception as e:
            print(f"DEBUG: Task generation failed ({e}). Using fallback.")
            task_data = {
                "task_en": "Describe your morning routine.",
                "task_hi": "अपनी सुबह की दिनचर्या के बारे में बताएं।"
            }
        
        task_doc = {
            "date": today_str,
            "task_en": task_data.get("task_en", "Describe your morning routine."),
            "task_hi": task_data.get("task_hi", "अपनी सुबह की दिनचर्या के बारे में बताएं।")
        }
        await db["tasks"].insert_one(task_doc)
        task = task_doc

    return {
        "task_en": task["task_en"],
        "task_hi": task["task_hi"],
        "date": task["date"]
    }

@router.get("/all")
async def get_all_tasks(current_user: dict = Depends(get_current_user)):
    db = get_database()
    tasks = await db["tasks"].find().to_list(100)
    for t in tasks:
        t["_id"] = str(t["_id"])
    return tasks

@router.post("/")
async def create_task(task_data: dict, current_user: dict = Depends(get_current_user)):
    db = get_database()
    # In a real app, check if user is admin
    result = await db["tasks"].insert_one(task_data)
    return {"id": str(result.inserted_id), "status": "created"}

@router.put("/{task_id}")
async def update_task(task_id: str, task_data: dict, current_user: dict = Depends(get_current_user)):
    db = get_database()
    from bson import ObjectId
    result = await db["tasks"].update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task_data}
    )
    if result.modified_count:
        return {"status": "updated"}
    return {"status": "no change"}
