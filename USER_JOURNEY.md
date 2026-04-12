# 🗺️ SpeakBetter - User Journey Map

This document outlines the step-by-step experience of a language learner interacting with the SpeakBetter platform.

---

## 📍 Phase 1: The Landing (Discovery)
**Context:** User arrives at the root URL (e.g., `speakbetter.onrender.com/static/index.html`).

### What they see:
- **Hero Reveal:** A sleek, glassmorphic dark-mode interface with vibrant purple and pink accents.
- **The Hook:** "Master English with AI" — a clear value proposition.
- **Auth Gate:** If not logged in, the user sees a centered, glowing Login/Register card.
- **Trust Elements:** Simple, modern typography (Outfit) and a native "App" feel.

---

## 🔐 Phase 2: Onboarding (Account Setup)
**Action:** User registers or logs in.

### The Experience:
- **Registration:** Minimalist form asking for Name, Email, and Password.
- **Instant Access:** Upon success, a JWT token is saved to the browser's `localStorage`, and the interface dynamically transitions to the **Practice View** without a page reload.

---

## 🎯 Phase 3: The Daily Challenge (Core Interaction)
**Action:** User views "Today's Topic".

### The Experience:
- **Task Generation:** The backend calls Gemini 2.5 Flash to generate a unique, culturally relevant speaking prompt (served in both English and Hindi).
- **The Stats:** User sees their "0 Days" streak, motivating them to start their first session.

---

## 🎙️ Phase 4: The Practice Cycle (The Magic Moment)
**Action:** User clicks the **Microphone** button to speak.

### Step-by-Step Flow:
1.  **Recording:** A pulse animation triggers. The user speaks their response to the prompt (e.g., "My favorite food is Pizza").
2.  **Processing:** Upon clicking stop, a "Processing..." glassmorphic overlay appears.
3.  **The Analysis (Stage 1):** Gemini multimodal engine transcribes the voice, corrects the grammar, and translates the nuances into Hindi.
4.  **The Voice (Stage 2):** A high-fidelity native AI voice (Kore) speaks the feedback and the corrected version out loud.
5.  **Visual Feedback:** Three cards appear:
    - **Transcription:** What the user said.
    - **Correction & Hindi:** The perfect version + explanation.
    - **Score:** A big numerical grade (e.g., 8/10).

---

## 📊 Phase 5: Progress & Mastery (Retention)
**Action:** User visits the **Dashboard**.

### What they see:
- **Growth Chart:** A line graph visualization (via Chart.js) showing their scores over the last 10 sessions.
- **Consistency Card:** A persistent streak counter that increments every day they complete a task.
- **History Log:** A scrollable list of past attempts they can revisit to see how far they've come.

---

## 💡 Phase 6: Deep Learning (Optimization)
**Action:** User explores the **Tips** page.

### The Experience:
- **Expert Advice:** User reads curated techniques (Shadowing, Thinking in English) to apply in their next SpeakBetter session.
- **Profile Management:** User updates their name or checks their "Member Since" badge to feel part of the community.

---

## 🔁 Summary of the Loop
1.  **LAND** -> See the beautiful UI.
2.  **AUTH** -> Create an identity.
3.  **REC** -> Speak to the AI.
4.  **LEARN** -> Read corrections & hear native audio.
5.  **TRACK** -> Watch the chart go up.
6.  **REPEAT** -> Build the daily habit.
