# 🧠 SpeakBetter - AI-Powered English Speaking App

SpeakBetter is an AI-driven platform designed to help Hindi-speaking beginners master spoken English through daily practice, instant feedback, and gamified progress.

## 🚀 Vision
Help everyone speak English confidently by providing a safe, encouraging, and structured environment for daily practice.

## ✨ Key Features
*   **Daily Challenges:** One task per day in both English and Hindi.
*   **AI Corrections:** Instant feedback on grammar, pronunciation, and vocabulary via Gemini AI.
*   **Hindi Explanations:** Understand *why* a correction was made in your native language.
*   **Streak System:** Build a habit with daily progress tracking.
*   **Voice Integration:** Real-time speech-to-text for a natural practice experience.

## 🏗️ Technical Stack
*   **Frontend:** [React](https://reactjs.org/) (Vite) + [Netlify](https://www.netlify.com/)
*   **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python) + [Render](https://render.com/)
*   **AI:** [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/)
*   **Database:** [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
*   **Scheduler:** [cron-job.org](https://cron-job.org/)

## 📁 Project Overview
### Backend (`/backend`)
The FastAPI backend handles user authentication, AI prompt engineering, and session storage. It follows a modular architecture with clear separation between routes, services, and models.

### Frontend (`/frontend`)
The React frontend provides a minimal, easy-to-use interface focused on "one-click" interactions. It utilizes browser-native APIs for speech recognition and synthesis to keep the application lightweight and free.

## ⚙️ Core Workflows
1.  **Authentication:** Secure JWT login/register.
2.  **Daily Flow:** Task → Speak → Correct → Listen → Progress.
3.  **Automation:** Cron jobs handle daily task rotation and server maintenance.

## 🧭 Project Philosophy
*   **Minimalism:** No clutter, just practice.
*   **Consistency:** Focus on small, daily improvements.
*   **Zero Cost:** Entirely built using industry-standard free tiers.

---
*Helping the world speak better, one sentence at a time.*
