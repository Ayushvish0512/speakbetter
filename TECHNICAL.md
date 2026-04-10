# 🛠️ SpeakBetter - Technical Specification

## 🏗️ 1. System Overview
SpeakBetter is a decoupled web application designed for high performance and low cost.

*   **Frontend:** React (Vite) → Netlify
*   **Backend:** FastAPI (Python) → Render (Free Tier)
*   **Database:** MongoDB Atlas (M0 Free Tier)
*   **AI Engine:** Google Gemini 2.5 Flash
*   **Scheduling:** cron-job.org

## ⚙️ 2. Tech Stack Detail
### Backend (FastAPI)
*   **Framework:** FastAPI for high-performance async API endpoints.
*   **Auth:** PyJWT for secure token-based authentication.
*   **Database Driver:** Motor (async MongoDB driver) or PyMongo.
*   **Validation:** Pydantic models for request/response validation.

### Frontend (React)
*   **Framework:** React 18+ with Vite for fast builds.
*   **State Management:** React Context or Redux Toolkit.
*   **APIs:** Browser SpeechRecognition (STT) and SpeechSynthesis (TTS).

## 📁 3. Project Structure (Backend)
```
backend/
├── app/
│   ├── main.py              # Entry point
│   ├── core/
│   │   ├── config.py        # Env vars & constants
│   │   ├── database.py      # MongoDB connection
│   │   └── security.py      # JWT & Password hashing
│   ├── models/              # MongoDB Schemas (Pydantic)
│   ├── routes/
│   │   ├── auth.py          # Register/Login
│   │   ├── submit.py        # Voice submission & AI processing
│   │   ├── task.py          # Daily task retrieval
│   │   └── progress.py      # User stats & streaks
│   ├── services/
│   │   ├── gemini_service.py # AI prompt logic
│   │   └── streak_service.py # Logic for daily active users
│   └── utils/
├── requirements.txt
└── .env
```

## 🗄️ 4. Database Schema (MongoDB)
### Users Collection
```json
{
  "_id": "ObjectId",
  "name": "Ravi",
  "email": "ravi@example.com",
  "hashed_password": "...",
  "streak": 5,
  "last_active": "2026-04-10T08:00:00Z"
}
```
### Sessions Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "date": "2026-04-10T08:05:00Z",
  "input_text": "I go market",
  "corrected_text": "I am going to the market",
  "hindi_explanation": "...",
  "score": 6
}
```
### Tasks Collection
```json
{
  "date": "2026-04-10",
  "task_en": "Describe your morning routine",
  "task_hi": "अपनी सुबह की दिनचर्या के बारे में बताएं"
}
```

## 🧠 5. Gemini AI Integration
**Prompt Template:**
```text
You are an English tutor for a Hindi-speaking beginner. 
Analyze the following sentence: "{{user_input}}"

Return JSON only:
{
  "corrected": "Corrected sentence",
  "hindi": "Simple Hindi explanation",
  "feedback": "Encouraging comment",
  "score": 8
}
```

## 🔐 6. Authentication Flow
1.  **Register/Login:** Users receive a JWT upon successful authentication.
2.  **Protected Endpoints:** `/submit-voice`, `/progress`, and `/get-task` require an `Authorization: Bearer <token>` header.
3.  **Token Payload:** Includes `user_id` and `exp` (expiration).

## ⏰ 7. Scheduler Jobs (cron-job.org)
*   **Ping Backend:** `GET /` every 10 minutes to prevent Render from sleeping.
*   **Daily Task:** `POST /daily-task` at 00:00 UTC to generate the day's challenge using Gemini.

## 🚀 8. Deployment Strategy
*   **Backend:** Automated deployments from the `main` branch via Render.
*   **Frontend:** Continuous deployment via Netlify with environment variables configured for the Production API URL.
*   **Security:** CORS configured to only allow requests from the Netlify domain.
