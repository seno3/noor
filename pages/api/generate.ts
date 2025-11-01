import type { NextApiRequest, NextApiResponse } from 'next';

const ESCALATION_KEYWORDS: string[] = [
  'scared', 'family', 'depressed', 'lonely', 'afraid', 'personal', 'feel', 'doubt',
];

const SYSTEM_INSTRUCTION = `You are "Noor Path," a gentle, supportive, and empathetic guide for Muslims. Your ONLY job is to answer the user's question based *exclusively* on the provided Google Search results.

RULES:

1.  **DO NOT** answer from your own knowledge. Your knowledge is not verified.

2.  **ONLY** use the provided search results from the <tool_use> block.

3.  You **MUST** cite your sources. After a sentence, add a citation like [1], [2], etc., corresponding to the search result.

4.  If the search results are not relevant to the user's question, you **MUST** apologize and say: "I'm sorry, I couldn't find a verified source for that specific question. Would you like me to connect you with a mentor who can help?"

5.  Keep your answers concise (2-3 sentences), empathetic, and clear.

6.  If the user's prompt is a simple greeting (like "hi" or "hello"), just respond with a kind, short greeting. Do not use search.

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

  const apiKey = process.env.GEMINI_API_KEY || '';
  
  if (!apiKey) {
    return res.status(500).json({
      type: 'ERROR',
      text: "I'm having trouble connecting to my knowledge base right now. Please configure the GEMINI_API_KEY environment variable.",
      sources: [],
    });
  }

  const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;

  const payload = {
    contents: [{ parts: [{ text: prompt }] }],
    tools: [{ "google_search": {} }],
    systemInstruction: {
      parts: [{ text: SYSTEM_INSTRUCTION }],
    },
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

    const candidate = result.candidates?.[0];
    if (!candidate || !candidate.content?.parts?.[0]?.text) {
      throw new Error('Invalid API response structure');
    }

    const text = candidate.content.parts[0].text;
    let sources: { uri: string; title: string }[] = [];

    const groundingMetadata = candidate.groundingMetadata;
    if (groundingMetadata && groundingMetadata.groundingAttributions) {
      sources = groundingMetadata.groundingAttributions
        .map((attribution: any) => ({
          uri: attribution.web?.uri,
          title: attribution.web?.title,
        }))
        .filter((source: any) => source.uri && source.title);
    }

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

