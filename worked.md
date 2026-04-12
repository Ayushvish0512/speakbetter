# 🧠 SpeakBetter - Deep Technical Documentation (worked.md)

This document provides a comprehensive breakdown of the **SpeakBetter** system, its architecture, file-level dependencies, and the core AI logic.

---

## 🔄 1. The Core Philosophy: Speech-to-Speech (STS) Flow
Unlike traditional apps that convert Speech-to-Text (STT) and then process it, SpeakBetter is designed around a **multi-modal AI pipeline**.

### The Pipeline:
1.  **Capture (Frontend):** The user's voice is captured as an raw audio stream and encoded into an **WebM/MP3** file.
2.  **Upload (Backend):** The binary audio file is sent to the FastAPI server and temporarily stored.
3.  **Phase 1: Analysis (Gemini 2.5 Flash):** The audio is uploaded to the Gemini File API. The system polls for the `ACTIVE` state and then requests a multimodal analysis. Gemini returns a **JSON object** with the transcription, corrections, and pedagogical feedback.
4.  **Phase 2: Native Speech (Gemini 2.5 TTS):** The feedback from Phase 1 is fed into the **Gemini 2.5 Flash Preview TTS** model using high-end prompting techniques (Audio Profiles, Director's Notes).
5.  **Reconstruction:** The backend wraps the raw PCM audio from Gemini into a **WAV container** (24kHz, 16-bit, Mono).
6.  **Delivery:** The frontend receives the JSON analysis and the base64-encoded WAV file, providing an integrated **Speech-to-Speech** experience.

---

## 🏗️ 2. Detailed File & Dependency Map

### 🌐 Backend (/backend)
| File Path | Purpose | Dependencies |
| :--- | :--- | :--- |
| `app/main.py` | The orchestrator. Mounts the UI, handles CORS, and includes all sub-routers. | `FastAPI`, `StaticFiles` |
| `app/core/config.py` | Centralized settings. Uses `pydantic-settings` to validate `.env` variables at startup. | `.env`, `Pydantic` |
| `app/core/database.py` | Async MongoDB client. Singleton pattern used via `db_instance`. | `Motor` |
| `app/core/security.py` | Cryptography module. Handles PBKDF2 hashing and JWT token generation/signing. | `passlib`, `python-jose` |
| `app/models/schemas.py` | Data blueprints. Defines how Users, Sessions, and Tasks look in JSON. | `Pydantic`, `BSON` |
| `app/services/gemini_service.py` | The AI interface. Manages the **google-genai** Client and two-stage pipeline. | `google-genai` |
| `app/routes/auth.py` | Identity management. Register/Login logic. | `core/security`, `models/schemas` |
| `app/routes/submit.py` | The processing hub. Receives audio, triggers Gemini, and saves results. | `services/gemini_service`, `core/database` |
| `app/routes/task.py` | The curriculum manager. Generates daily challenges using AI. | `services/gemini_service` |

### 🖼️ Frontend (/backend/app/static)
| File Path | Purpose | Key Logic |
| :--- | :--- | :--- |
| `index.html` | The entire UI. | Glassmorphism UI, Auth state management, MediaRecorder API for audio. |

---

## ⚙️ 3. How the Technologies Work

### FastAPI: The High-Speed Bridge
FastAPI works asynchronously. When a user uploads audio:
- The request is handled in a **non-blocking** way, allowing the server to handle multiple learners simultaneously.
- It uses **Pydantic** to double-check that no invalid data enters the database, ensuring the app never crashes due to bad input.

### Gemini AI: Beyond Simple Text
Gemini is configured as a **Senior English Tutor**. It follows a strict "System Prompt" that forces it to return **valid JSON**. This allows the app to cleanly parse the AI's "thoughts" and display them in separate UI boxes (Score, Correction, Hindi).

---

## 🧪 4. Testing Procedure

### Protocol A: Standalone AI Test
Before running the full web app, we use `test_audio_processing.py`.
- **Function:** It bypasses the web server and talks directly to Gemini.
- **Why?** To ensure your API Key and the audio file path are valid without the complexity of a browser.
- **Run:** `.\backend\venv\Scripts\python test_audio_processing.py`

### Protocol B: Full System Test
1.  **Database Connection:** Ensure MongoDB is running (FastAPI will log a connection success message).
2.  **Server Start:** `uvicorn app.main:app --reload`.
3.  **UI Verification:**
    - Open `http://localhost:8000/static/index.html`.
    - Check if "Today's Task" appears (Validates `task.py` + Gemini).
    - Record a 5-second clip (Validates `submit.py` + `gemini_service.py` + Audio Upload).

---

## 🔑 5. Critical Commands
| Command | Action | Location |
| :--- | :--- | :--- |
| `py -m venv venv` | Create isolated environment | `/backend` |
| `source venv/Scripts/activate` | Enter environment | `/backend` |
| `pip install -r requirements.txt` | Install the brain | `/backend` |
| `uvicorn app.main:app --reload` | Launch the app | `/backend` |

---

## ⚡ Deployment Note
The backend is configured to use **Environment Variables**. When moving to production (e.g., Render), simply add your `GEMINI_API_KEY` and `MONGODB_URL` to the hosting provider's "Secrets" panel.

---

## 📈 Session Log: April 12, 2026
- **Next-Gen AI Upgrade:**
    - Integrated **Gemini 3 Flash Preview** (`models/gemini-3-flash-preview`) for state-of-the-art Speech-to-Speech performance.
    - Implemented multi-modal `response_modalities=["TEXT", "AUDIO"]` to leverage Gemini 3's native dialogue capabilities.
- **Speech-to-Speech (STS) Flow:**
    - Upgraded AI engine to `gemini-2.5-flash-preview-tts` for native audio output.
    - Implemented `response_modalities=["TEXT", "AUDIO"]` for true conversational flow.
    - Updated frontend with base64 audio playback for AI-generated feedback.
    - Integrated fallback logic to `gemini-1.5-flash` for high reliability.
- **Next-Gen AI Upgrade (Native STS Fix):**
    - **SDK Migration**: Fully migrated to **`google-genai`** SDK (v1.72+) for future-proof integration.
    - Fixed **TypeError** in `Files.upload()` by using the correct `file=` argument instead of `path=`.
    - Implemented a **Two-Stage Pipeline**: 
        1. **Analysis**: `gemini-2.5-flash` for transcription and feedback JSON.
        2. **Native speech**: `gemini-2.5-flash-preview-tts` for high-fidelity audio.
    - Added **File State Polling**: Wait loop ensuring `ACTIVE` state before requests.
    - Added **WAV Header Injection**: Wrapped raw PCM data into a valid WAV container for instant playback.
    - Simplified Login Payload: Resolved 422 errors.
    - UI Polish: Added version v2.0 tag, loading states, and error traceability.
- **Production & Stability Finalization:**
    - **Blueprint Infrastructure**: Created `render.yaml` for 1-click "Infrastructure as Code" deployment.
    - **Hybrid Audio Engine**: Implemented a **Stage-2 Failover** mechanism. If Gemini's native TTS service faces downtime (500 errors), the app automatically falls back to the **Browser Web Speech API**, ensuring uninterrupted user feedback.
    - **Performance Optimization**: Optimized library dependencies (removed old SDKs) to keep build sizes under 400MB.
    - **Local-Production Simulation**: Updated `.env` and `Procfile` to allow for identical behavior between local dev and cloud hosting using `gunicorn`.
