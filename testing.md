# 🧪 SpeakBetter - Quality Assurance & Testing Guide (testing.md)

This guide explains how to rigorously test the SpeakBetter application and the objective criteria for judging if the AI is meeting the project goals.

---

## 🏗️ 1. The Three-Tier Testing Approach

To ensure SpeakBetter works perfectly, testing is divided into three levels:

### Level 1: Core AI Logic (The Script)
Before using the UI, we test the "brain" using `test_audio_processing.py`.
- **Method:** Run `.\backend\venv\Scripts\python test_audio_processing.py`.
- **What to look for:**
    - Does it connect to Gemini without error?
    - Does `result.json` contain valid, readable Hindi characters?
    - Is the `score` logically consistent with the grammar mistakes?

### Level 2: API & Integration (The Backend)
Validate the FastAPI endpoints using the `/docs` (Swagger) UI.
- **Method:** Go to `http://localhost:8000/docs`.
- **Tests:** 
    - `/auth/register`: Create a test user.
    - `/task/`: Does it return a task for today?
    - `/progress/history`: Does it show your previous runs?

### Level 3: User Experience (The Frontend)
Testing the complete STS (Speech-to-Speech) loop.
- **Method:** Use the app at `http://localhost:8000/static/index.html`.
- **Verification:**
    - **Record UI:** Does the mic button pulse?
    - **Playback:** Does the speech synthesis (TTS) sound natural and match the corrected text?
    - **Streaks:** Does your streak count increase after a successful submission?

---

## ⚖️ 2. How to Judge "Quality" (Success Criteria)

A "Good" result is defined by three key factors: **Accuracy, Pedagogy, and Friction.**

### 🎯 A. Accuracy (The Correction)
- **The Bar:** The corrected sentence must be grammatically flawless but still maintain the *meaning* of the original spoken sentence.
- **PASS:** User says "Me go school," AI corrects to "I am going to school."
- **FAIL:** AI changes the whole topic or fails to fix basic word order.

### 🍱 B. Hindi Explanation (The Pedagogy)
- **The Bar:** The Hindi must be simple, encouraging, and *explain the mistake* rather than just translating.
- **PASS:** AI explains *why* "me" should be "I" in simple Hindi.
- **FAIL:** AI gives advanced, complex Sanskritized Hindi that a beginner can't understand.

### ⚡ C. Latency (The Speed)
- **The Bar:** Processing audio (including Gemini upload + processing) should take under 5-8 seconds.
- **FAIL:** If processing takes >20 seconds, the user will lose focus. (Note: Gemini Flash is optimized for speed).

---

## 📋 3. Testing Checklist for the User

1. [ ] **Mute/Silence Test:** Speak nothing and click stop. Check if the AI handles empty audio gracefully.
2. [ ] **Intentional Mistake Test:** Speak a sentence with a common mistake (e.g., "I has a pen"). Check if Gemini identifies "has" vs "have".
3. [ ] **Audio Quality Test:** Record in a noisy room vs a quiet room. Gemini 2.0/Flash excels at noise cancellation.
4. [ ] **Streak Midnight Test:** Does the daily task rotate automatically at 00:00 UTC?
5. [ ] **Cross-Device Test:** Open the URL on your mobile phone (if on the same network). Does the mic work on mobile browsers?

---

## 🛠️ Troubleshooting Common Failures

| Issue | Likely Cause | Solution |
| :--- | :--- | :--- |
| **"Could not start recording"** | Mic Permission | Allow mic access in your browser padlock icon (HTTPS might be needed for some browsers). |
| **Empty Feedback** | Gemini Quota | Check your Google AI Studio dashboard for quota limits. |
| **Login Errors** | Database | Ensure MongoDB is running and correctly linked in `.env`. |

---

*“Consistency Build Confidence.” – The goal of testing is to ensure the user feels safe making mistakes.*
