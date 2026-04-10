# 🧩 SpeakBetter - Product Requirements Document (PRD)

## 🎯 1. Objective
Help Hindi-speaking beginners (e.g., adult learners) improve their spoken English daily using AI, with minimal friction and maximum consistency.

The product focuses on:
*   **Daily Speaking Practice:** One focused task per day.
*   **Instant Correction:** Real-time AI feedback.
*   **Simple Hindi Explanations:** Bridging the language gap.
*   **Habit Formation:** Streak tracking and daily reminders.

## 👤 2. Target Users
### Primary Persona: Hindi-speaking Adult Beginner
*   **Age:** 35–60
*   **Struggles:** Hesitation while speaking, lack of vocabulary, fear of mistakes.
*   **Literacy:** Understands basic Hindi; low patience for complex interfaces.
*   **Key Problems:** No one to practice with, no immediate feedback, lack of structure.

## 💡 3. Core Value Proposition
*“Speak one sentence daily. Get corrected instantly. Improve without fear.”*

## 🧱 4. Feature Scope (MVP)
### 🔥 Core Features
1.  **Daily Task System:** Users receive one specific task per day (e.g., "Describe your morning routine").
2.  **Voice/Text Submission:**
    *   **Phase 1:** Browser-based Speech-to-Text (STT) for ease of use.
    *   **Phase 2:** Native audio processing via Gemini.
3.  **AI Correction Engine (Gemini 2.5 Flash):**
    *   Corrected sentence.
    *   Hindi explanation of the correction.
    *   Encouragement and a proficiency score (0–10).
4.  **Audio Playback:** AI-generated correct pronunciation using Browser TTS.
5.  **Gamification:** Daily streaks and attempt history to keep users engaged.
6.  **Authentication:** Secure JWT-based multi-user support (Register/Login).

## 🏗️ 5. System Architecture
*   **Frontend:** React (Vite) hosted on Netlify.
*   **Backend:** FastAPI (Python) hosted on Render.
*   **AI:** Gemini 2.5 Flash API.
*   **Database:** MongoDB Atlas (NoSQL).
*   **Scheduler:** cron-job.org for daily task generation and server pings.

## 🧠 6. AI Design (Gemini Prompt)
**Role:** Senior English Tutor for Hindi Speakers.
**Input:** `{{user_sentence}}`
**Constraint:** Return strictly valid JSON.
**Rules:** 
*   Keep Hindi simple and colloquial.
*   Feedback must be extremely encouraging.
*   Max 2 sentences for the explanation.

## 🔄 7. User Flow
1.  **Login:** User authenticates via JWT.
2.  **Daily Task:** User sees the current day's task in English and Hindi.
3.  **Practice:** User clicks "Speak", records their response, and reviews the transcript.
4.  **Feedback:** AI analyzes the input and displays correction, Hindi meaning, and score.
5.  **Review:** User listens to the correct pronunciation via TTS.
6.  **Progress:** Streak increases; session is saved.

## 📊 8. Success Metrics
*   **Engagement:** Daily Active Users (DAU) and Task Completion Rate.
*   **Learning:** Average score improvement over 30 days.
*   **Retention:** Percentage of users maintaining a >5 day streak.

## ⚠️ 9. Risks & Mitigations
*   **Render Cold Start:** Mitigated by `cron-job.org` pings every 10 minutes.
*   **Gemini Limits:** Request throttling and caching for frequent phrases.
*   **STT Errors:** Allow users to manually edit the transcript before final submission.

## 🧭 10. Product Philosophy
*   **Consistency > Complexity:** Better to do one task well than many poorly.
*   **Encouragement > Correctness:** Focus on building confidence first.
*   **Zero-Cost Stack:** Designed to run entirely on free tiers.