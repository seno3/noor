# Noor Path: Your Guided Journey

A safe space with **AI-verified answers** and **seamless human support**.

## Track

Build for the Ummah — Technical

## Inspiration

For students at UIUC, learning about Islam, reconnecting with faith, or seeking to convert is a deeply personal and vulnerable journey. The internet is a minefield. It's filled with "slop," misinformation, and harsh judgments. New learners can't distinguish between a scholarly fact and an unverified opinion. They have personal, subjective questions (e.g., "I feel lonely") but no safe, non-judgmental place to ask them.

We were inspired to create **Noor Path**—a technically brilliant application that provides a safe, guided space for this journey, combining the reliability of verified AI answers with the empathy of human mentors.

## What it does

**Noor Path** is a "technically brilliant" application that creates a safe, guided space. Our UI/UX is not just an app—it's a **scroll-based story** that guides users through their Islamic journey.

1. **A "Grounded AI" App:** A unique, non-generic chat interface that provides answers **powered by Ollama (Mistral model) with RAG capabilities.** Our backend *forces* the AI to provide accurate, empathetic answers and handle different types of questions appropriately.

2. **Human Mentor Escalation:** For subjective, personal questions, our backend *detects* this using keyword detection and invites the user to connect with trusted student mentors from the MSA.

3. **Seamless User Experience:** The app features a beautiful, animated interface with a grainy gradient background, typing effects, and smooth transitions between different "rooms"—Welcome, Chat, and Mentors. This creates a zero-friction flow from a moment of need to human connection.

## How we built it

We built **Noor Path** as a full-stack Next.js application with TypeScript:

**Frontend:**
- Next.js 14 (Pages Router) with TypeScript
- Framer Motion for spring-based animations and smooth transitions
- Tailwind CSS for styling with custom gradient backgrounds
- Zustand for state management
- Custom typing effect for dynamic placeholder text

**Backend:**
- Next.js API routes (`/api/generate`)
- Ollama integration with Mistral model for local AI inference
- Intent detection system using keyword matching for mentor escalation
- System prompts designed for empathetic, accurate responses

**UI/UX:**
- Three-state room system (Welcome → Chat → Mentors) with AnimatePresence transitions
- Grainy gradient background with animated floating orbs
- Bouncy spring animations for all interactions
- Responsive design optimized for all screen sizes

## Challenges we ran into

1. **Implementing proper RAG pipeline:** Initially planned to use Gemini with Google Search grounding, but transitioned to Ollama for local inference while maintaining the core RAG principles.

2. **Creating seamless state transitions:** Building the multi-room interface with smooth animations required careful management of state and animation timing with Framer Motion.

3. **Background effects performance:** Balancing beautiful animated background effects with performance, ensuring they don't distract from content or cause lag.

4. **Intent detection accuracy:** Fine-tuning the keyword-based escalation system to reliably detect when a question requires human mentorship vs. AI response.

## Accomplishments that we're proud of

1. **Technical Brilliance:** Built a full-stack RAG-powered application with proper AI integration, source citation, and intelligent intent detection.

2. **Flawless UI/UX:** Created a unique, non-generic interface that feels like a guided journey rather than just an app. The scroll-based story flow with animated transitions sets us apart.

3. **High Empathy Design:** Every interaction—from the typing placeholder effects to the smooth mentor escalation—is designed to reduce friction and create a safe, welcoming space.

4. **Rapid Development:** Delivered a polished, production-ready application in 36 hours that successfully combines technical innovation with beautiful design.

5. **Beautiful Visual Design:** Implemented custom grainy gradient backgrounds with subtle animated effects that enhance the experience without overwhelming the user.

## What we learned

1. **RAG Implementation:** Learned how to structure system prompts and API calls to force AI models to cite sources and provide verified answers.

2. **Animation Best Practices:** Discovered how to use Framer Motion's spring physics for delightful, bouncy interactions that feel natural and responsive.

3. **State Management:** Explored Zustand for managing complex multi-room state transitions while maintaining clean component architecture.

4. **Intent Detection:** Developed keyword-based escalation systems that can intelligently route users to appropriate resources based on question type.

5. **Empathetic Design:** Learned how small UX details—like typing effects, smooth transitions, and gentle animations—can significantly impact user comfort and trust.

## What's next for Noor

1. **Enhanced AI Capabilities:** Integrate more sophisticated RAG with vector databases and better context management for more accurate responses.

2. **Advanced Intent Detection:** Implement ML-based sentiment analysis and intent classification for more nuanced mentor escalation.

3. **Mentor Management System:** Build an admin interface for mentors to manage their profiles, availability, and communication preferences.

4. **Community Features:** Add features for users to connect with each other, share experiences, and build a supportive community around their journey.

5. **Analytics & Insights:** Implement analytics to understand user needs better and continuously improve the escalation logic and AI responses.

6. **Mobile Optimization:** Further optimize the mobile experience with native-feeling interactions and performance improvements.

7. **Multilingual Support:** Expand to support multiple languages to serve a broader community of learners.
