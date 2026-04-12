# 🎙️ SpeakBetter

An AI-powered English speaking practice app for Hindi speakers.

## 🚀 Features
- **Daily Challenges:** English & Hindi tasks to keep you motivated.
- **AI Feedback:** Instant transcription and correction via Google Gemini.
- **Hindi Explanations:** Understand corrections in your native language.
- **Streak System:** Build a daily habit.
- **Browser TTS:** Listen to the correct pronunciation.

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML/JS/CSS (Served by FastAPI)
- **AI:** Google Gemini 1.5 Flash
- **Database:** MongoDB

## 🏃 Getting Started

### 1. Prerequisites
- Python 3.9+
- MongoDB installed locally or a MongoDB Atlas URI.
- Google Gemini API Key.

### 2. Setup
1. Clone the repository.
2. Navigate to the `backend` folder.
3. Create a virtual environment:
   ```bash
   py -m venv venv
   ```
4. Activate the venv:
   ```bash
   .\venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Create a `.env` file in the `backend` folder and fill in your details:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=speakbetter
   JWT_SECRET=your_jwt_secret
   GEMINI_API_KEY=your_gemini_api_key
   ```

### 3. Running the App
1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Open your browser at `http://localhost:8000/static/index.html`.

## 🧪 Testing Audio
Run the standalone test script to verify Gemini integration:
```bash
python test_audio_processing.py
```
*(Make sure to update the audio file path in the script)*