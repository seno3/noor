import type { NextApiRequest, NextApiResponse } from 'next';

const ESCALATION_KEYWORDS: string[] = [
  'scared', 'family', 'depressed', 'lonely', 'afraid', 'personal', 'feel', 'doubt', 'ambiguous', 'subjective'
];

const SYSTEM_INSTRUCTION = `You are "Noor Path," a gentle, supportive, and empathetic guide for Muslims. Your job is to answer questions about Islam with care, accuracy, and empathy.

RULES:

1.  Provide helpful, accurate information about Islamic teachings, practices, and guidance.

2.  Be gentle, non-judgmental, and supportive in your responses.

3.  If you're uncertain about something or if a question is very personal/complex, suggest connecting with a mentor.

4.  Keep your answers concise (2-3 sentences), empathetic, and clear.

5.  If the user's prompt is a simple greeting (like "hi" or "hello"), just respond with a kind, short greeting.

6.  Remember that this is a safe space for Muslims at all stages of their journey.

`;

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { prompt } = req.body;

  if (!prompt) {
    return res.status(400).json({ error: 'Prompt is required' });
  }

  const lowerPrompt = prompt.toLowerCase();

  const isEscalation = ESCALATION_KEYWORDS.some((keyword) =>
    lowerPrompt.includes(keyword)
  );

  if (isEscalation) {
    return res.status(200).json({
      type: 'MENTOR_ESCALATION',
      text: "That's a very personal and important question. For support like this, it's best to talk to a person, not an AI. Would you like to connect with a trusted student mentor from the MSA?",
      sources: [],
    });
  }

  const ollamaUrl = process.env.OLLAMA_URL || 'http://localhost:11434';
  const ollamaModel = process.env.OLLAMA_MODEL || 'mistral';

  const apiUrl = `${ollamaUrl}/api/chat`;

  const payload = {
    model: ollamaModel,
    messages: [
      {
        role: 'system',
        content: SYSTEM_INSTRUCTION,
      },
      {
        role: 'user',
        content: prompt,
      },
    ],
    stream: false,
  };

  try {
    const apiResponse = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!apiResponse.ok) {
      const errorText = await apiResponse.text();
      throw new Error(`API error: ${apiResponse.statusText} - ${errorText}`);
    }

    const result = await apiResponse.json();

    if (!result.message || !result.message.content) {
      throw new Error('Invalid API response structure');
    }

    const text = result.message.content;
    const sources: { uri: string; title: string }[] = [];

    res.status(200).json({
      type: 'VERIFIED_ANSWER',
      text: text,
      sources: sources,
    });
  } catch (error: any) {
    console.error(error.message);
    res.status(500).json({
      type: 'ERROR',
      text: "I'm having trouble connecting to my knowledge base right now. Please try again in a moment.",
      sources: [],
    });
  }
}

