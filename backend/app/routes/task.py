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
        # For simplicity, let's use a small predefined list or ask Gemini
        prompt = """
        Generate a simple daily English speaking task for a Hindi-speaking beginner.
        Example: "Describe your favorite food" or "What did you do yesterday?".
        Return JSON: {"task_en": "Task in English", "task_hi": "Task in Hindi"}
        """
        response = gemini_service.model.generate_content(prompt)
        try:
            text = response.text.strip()
            if text.startswith("```json"): text = text[7:-3].strip()
            task_data = json.loads(text)
        except:
            task_data = {
                "task_en": "Describe your morning routine.",
                "task_hi": "अपनी सुबह की दिनचर्या के बारे में बताएं।"
            }
        
        task_doc = {
            "date": today_str,
            "task_en": task_data["task_en"],
            "task_hi": task_data["task_hi"]
        }
        await db["tasks"].insert_one(task_doc)
        task = task_doc

    return {
        "task_en": task["task_en"],
        "task_hi": task["task_hi"],
        "date": task["date"]
    }
