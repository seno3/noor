# Noor Path

A safe space with AI-verified answers and seamless human support for your Islamic journey.

## Getting Started

First, install the dependencies:

```bash
npm install
```

Create a `.env.local` file in the root directory and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Project Structure

- `/pages` - Next.js pages and API routes
- `/components` - React components
- `/hooks` - Custom React hooks
- `/data` - Static data files
- `/styles` - Global styles

## Key Features

- **AI-Powered Chat**: Uses Gemini API with Google Search grounding for verified answers
- **Human Mentor Escalation**: Detects personal questions and connects users with mentors
- **Seamless Scheduling**: Integrated Calendly widget for booking mentor sessions
- **Smooth Animations**: Framer Motion animations for all screen transitions

