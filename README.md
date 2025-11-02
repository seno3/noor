# Noor Path (MTCHacks 2025 Submission)

Noor Path is a high-empathy, full-stack application designed to provide a safe, non-judgmental space for individuals learning about Islam.

Our app is built on a **"flawless" Vertical Journey flow:**

1.  **Welcome:** A full-screen, cinematic welcome to the "Noor Path."

2.  **Crossroads:** The user selects their persona (e.g., "I recently accepted Islam").

3.  **Chat:** The page auto-scrolls to our "technically brilliant" chat UI, which uses a **real RAG (Retrieval-Augmented Generation) backend** with Google Search grounding to provide *verified, cited answers*.

4.  **Mentor Escalation:** For personal questions, our backend detects the user's intent and offers a human connection.

5.  **Mentor Grove:** The user auto-scrolls to the mentor section.

6.  **Seamless Scheduling:** When the user clicks "Schedule," the mentor card **animates inline** to reveal the Calendly widget. This is a **zero-friction, zero-page-load** flow from question to human support.

## Technical Brilliance

* **Frontend:** A unique, single-page, scroll-based journey built with Next.js, TypeScript, and `framer-motion` for all layout and scroll animations.

* **Backend (`/api/generate`):** A robust Next.js API route that performs:

    1.  **Intent Detection** (Fact vs. Personal Escalation).

    2.  **Real-Time RAG** via Gemini (`gemini-2.5-flash-preview-09-2025`) and Google Search grounding.

    3.  **System Instruction** enforcement to guarantee cited, safe answers and prevent AI "slop."

* **Flawless UI/UX:** Our most critical feature is the inline Calendly embed, which uses `framer-motion`'s `layout` prop and `AnimatePresence` to create a seamless scheduling experience without ever leaving the page.

## How to Run

1.  `npm install`

2.  Replace the placeholder URLs in `/data/mentors.ts` with your real Calendly links.

3.  Create a `.env.local` file with your Gemini API key:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

4.  `npm run dev`
