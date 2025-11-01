# Noor Path: Your Guided Journey

A safe space with **AI-verified answers** and **seamless human support**.

## Track

Build for the Ummah — Technical

## The Problem

For students at UIUC, learning about Islam, reconnecting with faith, or seeking to convert is a deeply personal and vulnerable journey. The internet is a minefield. It's filled with "slop," misinformation, and harsh judgments. New learners can't distinguish between a scholarly fact and an unverified opinion. They have personal, subjective questions (e.g., "I'm scared to tell my family") but no safe, non-judgmental place to ask them.

## Our Solution: A Flawless, High-Empathy Flow

**Noor Path** is a "technically brilliant" application that creates a safe, guided space. Our UI/UX is not an app, it's a *flow*.

1.  **A "Grounded AI" App:** A unique, non-generic chat interface that provides answers **powered by the Gemini API with Google Search grounding.** This isn't a generic chatbot. Our backend *forces* the AI to *only* use real-time search results for its answers, and it **cites every source** it uses. This *is* the verified-source solution.

2.  **Human Mentor Escalation:** For subjective, personal questions (e.g., "I feel lonely"), our backend *detects* this and skips the AI, immediately offering to connect the user with a trusted human mentor from the campus MSA.

3.  **Seamless Scheduling (with Calendly):** When a user accepts, they are taken to a "Meet Your Mentors" screen. They can see real student mentor profiles and, with one click, book a time *directly in the app* via an inline Calendly embed. **No friction, no drop-off.**

## Technical Brilliance

We built a full-stack Next.js application in 36 hours.

* **Frontend:** A polished, unique, and fluid multi-screen UI built with React, TypeScript, and **Framer Motion** for all page-level transitions.

* **Backend (`/api/generate`):** A robust Next.js API route that acts as our "brain."

    * It performs **intent detection** (fact vs. personal escalation).

    * For facts, it implements **Retrieval-Augmented Generation (RAG)** by calling the Gemini API with `tools: [{"google_search": {} }]` enabled.

    * It uses a strong **System Instruction** to enforce a "cite-your-sources" policy and prevent the AI from answering with unverified "slop."

* **Seamless Integration:** We use `react-calendly` to embed the scheduling flow directly, creating a *truly* seamless user flow from question to human support.

## 3-Minute Video Script

(This script is designed to perfectly demonstrate our unique flow.)

**[0:00 - 0:30] The Problem**

* (Show our **WelcomeScreen**.)

* **VOICEOVER:** "Meet 'Noor,' a student on campus. She's new to Islam and has questions. But the internet is full of confusing, unverified 'slop'. How does she know who to trust? Where can she ask personal questions without fear?"

**[0:30 - 1:15] The "Technically Brilliant" Chat**

* (Click "I recently accepted Islam." The *entire screen* animates and transitions to the **ChatScreen**.)

* **VOICEOVER:** "This is Noor Path. It's a gentle, guided chat. Let's ask a question."

* (Type "How do I perform Wudu?" The AI message appears, with the text AND the "Verified Sources" box.)

* **VOICEOVER:** "This is our 'technically brilliant' solution. Our backend is a Next.js API that uses the Gemini API with **Google Search grounding**. We force the AI to *only* use real-time search results and to **cite every source**. This isn't a generic chatbot; it's a *verified* guide."

**[1:15 - 2:45] The "Flawless" Mentor Flow (The Winning Feature)**

* (Now, type in "I feel lonely and scared to tell my family.")

* **VOICEOVER:** "But what about a personal question? Our backend *detects* this is a subjective, human-level question. It *skips* the AI."

* (The purple "Mentor Escalation" card appears. Click "Meet the Mentors".)

* **VOICEOVER:** "And this is our **flawless user flow**. The app *instantly* slides in our 'Meet Your Mentors' screen. Noor can see real UIUC students."

* (Show the mentor profiles. Click "Schedule a Chat" on Ahmed's profile.)

* **VOICEOVER:** "With one click, she's not sent to another site. The Calendly scheduling widget loads *inline*. She can book a time right here. This is a seamless, zero-friction path from a moment of fear to a confirmed human connection."

**[2:45 - 3:00] The Close**

* (Show the `api/generate.ts` code in the repo.)

* **VOICEOVER:** "We built a full-stack, RAG-powered, multi-screen application with a flawless, high-empathy UI in 36 hours. This is Noor Path. Thank you."

