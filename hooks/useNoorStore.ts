import { useState, useEffect } from 'react';

export type AppState = 'welcome' | 'chat' | 'mentors' | 'scheduling';

export interface Source {
  uri: string;
  title: string;
}

export interface AiResponse {
  type: 'VERIFIED_ANSWER' | 'MENTOR_ESCALATION' | 'ERROR';
  text: string;
  sources: Source[];
}

export interface Message {
  id: number;
  sender: 'user' | 'ai';
  content?: AiResponse;
  userPrompt?: string;
}

let globalState = {
  appState: 'welcome' as AppState,
  messages: [] as Message[],
  isLoading: false,
  selectedMentorUrl: '',
};

let listeners: React.Dispatch<React.SetStateAction<typeof globalState>>[] = [];

const setState = (
  newState: Partial<typeof globalState> | ((prev: typeof globalState) => Partial<typeof globalState>)
) => {
  if (typeof newState === 'function') {
    globalState = { ...globalState, ...newState(globalState) };
  } else {
    globalState = { ...globalState, ...newState };
  }
  listeners.forEach((listener) => listener(globalState));
};

export const useNoorStore = () => {
  const [state, _setState] = useState(globalState);

  if (!listeners.includes(_setState)) {
    listeners.push(_setState);
  }

  useEffect(() => {
    return () => {
      listeners = listeners.filter((l) => l !== _setState);
    };
  }, []);

  const navigateTo = (state: AppState) => setState({ appState: state });

  const startScheduling = (calendlyUrl: string) => {
    setState({ selectedMentorUrl: calendlyUrl, appState: 'scheduling' });
  };

  const addMessage = (message: Message) => {
    setState((prev) => ({ messages: [...prev.messages, message] }));
  };

  const sendMessage = async (prompt: string) => {
    setState({ isLoading: true });
    const userMessage: Message = {
      id: Date.now(),
      sender: 'user',
      userPrompt: prompt,
    };
    addMessage(userMessage);

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const aiData: AiResponse = await response.json();

      const aiMessage: Message = {
        id: Date.now() + 1,
        sender: 'ai',
        content: aiData,
      };
      addMessage(aiMessage);
    } catch (error) {
      addMessage({
        id: Date.now() + 1,
        sender: 'ai',
        content: {
          type: 'ERROR',
          text: 'I seem to be having trouble connecting. Please check your internet and try again.',
          sources: [],
        },
      });
    } finally {
      setState({ isLoading: false });
    }
  };

  return { ...state, navigateTo, startScheduling, sendMessage, addMessage };
};

