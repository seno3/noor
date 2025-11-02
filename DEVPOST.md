# Noor Path: Your Guided Journey

A safe space with **AI-verified answers** and **seamless human support**.

## Track

Build for the Ummah — Technical

## The Problem

For students at UIUC, learning about Islam, reconnecting with faith, or seeking to convert is a deeply personal and vulnerable journey. The internet is a minefield. It's filled with "slop," misinformation, and harsh judgments. New learners can't distinguish between a scholarly fact and an unverified opinion. They have personal, subjective questions (e.g., "I feel lonely") but no safe, non-judgmental place to ask them.

## Our Solution: A Flawless, High-Empathy "Vertical Journey"

**Noor Path** is a "technically brilliant" application that creates a safe, guided space. Our UI/UX is not an app, it's a **scroll-based story**.

1.  **A "Grounded AI" App:** A unique, non-generic chat interface that provides answers **powered by the Gemini API with Google Search grounding.** This isn't a generic chatbot. Our backend *forces* the AI to *only* use real-time search results for its answers, and it **cites every source** it uses.

2.  **Human Mentor Escalation:** For subjective, personal questions, our backend *detects* this and skips the AI, inviting the user to continue their "journey" down the page to the mentor section.

3.  **Seamless Scheduling (with Calendly):** When a user clicks "Schedule" on a mentor, the card **animates inline** to reveal the Calendly widget. This is a **zero-friction, zero-page-load** flow from a moment of fear to a confirmed human connection.

## 3-Minute Video Script (This script wins all UI/UX points)

**[0:00 - 0:30] The Problem (Problem Definition: 4/4)**

* (Show our **Welcome Screen**, full-screen. The text animates in.)

* **VOICEOVER:** "Meet 'Noor,' a student on campus. She's new to Islam and has questions. But the internet is full of confusing, unverified 'slop'. How does she know who to trust? Where can she ask personal questions without fear?"

**[0:30 - 1:15] The "Unique & Technical" Chat (UI/UX: 4/4, Technical: 4/4)**

* (User scrolls down. The "Crossroads" scene appears. Click "I recently accepted Islam." The page *smoothly auto-scrolls* down to the **ChatUI**.)

* **VOICEOVER:** "This is Noor Path. It's not a website; it's a 'Vertical Journey.' We've created a unique, scroll-based flow. Let's ask a question."

* (Type "How do I perform Wudu?" The AI message appears, with the text AND the "Verified Sources" box.)

* **VOICEOVER:** "This is our 'technically brilliant' solution. Our backend is a Next.js API that uses the Gemini API with **Google Search grounding**. We force the AI to *only* use real-time search results and to **cite every source**. This isn't a generic chatbot; it's a *verified* guide."

**[1:15 - 2:45] The "Flawless" Mentor Flow (Impact: 4/4, UI/UX: 4/4)**

* (Now, type in "I feel lonely and scared to tell my family.")

* **VOICEOVER:** "But what about a personal question? Our backend *detects* this is a subjective, human-level question. It *skips* the AI."

* (The purple "Mentor Escalation" card appears. Click "Continue your journey".)

* **VOICEOVER:** "And this is our **flawless user flow**. The app understands this is the next step. The user continues down the path..."

* (The page *smoothly auto-scrolls* down to the "Mentor Grove" scene. The mentor cards animate in.)

* **VOICEOVER:** "...to our Mentor Grove. Here, Noor can see real UIUC students. Let's schedule with Ahmed."

* (Click "Schedule a Chat" on Ahmed's profile. **Show this clearly:** The *other* mentor card animates *out*, and the Calendly embed animates *in* right below Ahmed's card.)

* **VOICEOVER:** "With one click, the Calendly widget loads *inline*. No popups. No new pages. This is a seamless, zero-friction path from a moment of fear to a confirmed human connection."

**[2:45 - 3:00] The Close**

* (Show the `api/generate.ts` code in the repo, highlighting the `SYSTEM_INSTRUCTION`.)

* **VOICEOVER:** "We built a full-stack, RAG-powered, narrative-driven app with a flawless, high-empathy UI in 36 hours. This is Noor Path. Thank you."
