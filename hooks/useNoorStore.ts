import { create } from 'zustand';

export type AppState = 'welcome' | 'chat' | 'mentors';

export interface Source { uri: string; title: string; }
export interface AiResponse { type: 'VERIFIED_ANSWER' | 'MENTOR_ESCALATION' | 'ERROR'; text: string; sources: Source[]; }
export interface Message { id: number; sender: 'user' | 'ai'; content?: AiResponse; userPrompt?: string; }

interface NoorState {
  appState: AppState;
  messages: Message[];
  isLoading: boolean;
  
  // Actions
  setAppState: (state: AppState) => void;
  sendMessage: (prompt: string) => Promise<void>;
}

export const useNoorStore = create<NoorState>((set, get) => ({
  appState: 'welcome',
  messages: [],
  isLoading: false,

  setAppState: (state) => set({ appState: state }),

  sendMessage: async (prompt: string) => {
    set({ isLoading: true });
    const userMessage: Message = { id: Date.now(), sender: 'user', userPrompt: prompt };
    set((state) => ({ messages: [...state.messages, userMessage] }));

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      if (!response.ok) throw new Error('Network error');
      
      const aiData: AiResponse = await response.json();
      const aiMessage: Message = { id: Date.now() + 1, sender: 'ai', content: aiData };
      set((state) => ({ messages: [...state.messages, aiMessage] }));
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now() + 1,
        sender: 'ai',
        content: { type: 'ERROR', text: 'Connection error. Please try again.', sources: [] },
      };
      set((state) => ({ messages: [...state.messages, errorMessage] }));
    } finally {
      set({ isLoading: false });
    }
  },
}));
