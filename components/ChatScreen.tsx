import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNoorStore, Message } from '../hooks/useNoorStore';
import { AiResponse } from '../hooks/useNoorStore';

const ChatInput = ({ onSend, isLoading }: { onSend: (val: string) => void; isLoading: boolean }) => {
  const [value, setValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (value.trim() && !isLoading) {
      onSend(value);
      setValue('');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.5 }}
      className="sticky bottom-0 bg-gradient-to-t from-white via-white/80 to-transparent p-4"
    >
      <form onSubmit={handleSubmit} className="mx-auto max-w-lg">
        <div className="flex items-center rounded-full bg-white p-2 shadow-xl shadow-purple-100/70 ring-1 ring-slate-100">
          <input
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 bg-transparent px-4 text-slate-700 placeholder-slate-400 focus:outline-none"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="rounded-full bg-gradient-to-r from-pink-500 to-purple-500 p-3 text-white shadow-md shadow-pink-500/30 transition-all hover:brightness-110 disabled:opacity-50"
            disabled={isLoading}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-5 w-5 rotate-90">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009.5 16.571V11.5a1 1 0 012 0v5.071a1 1 0 00.223.632l5 1.429a1 1 0 001.17-1.409l-7-14z" />
            </svg>
          </button>
        </div>
      </form>
    </motion.div>
  );
};

const UserMessage = ({ msg }: { msg: string }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.3 }}
    className="mb-4 flex justify-end"
  >
    <div className="max-w-md rounded-2xl rounded-br-none bg-gradient-to-r from-pink-500 to-purple-500 p-4 text-white shadow-lg shadow-pink-500/30">
      {msg}
    </div>
  </motion.div>
);

const LoadingIndicator = () => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0 }}
    transition={{ duration: 0.3 }}
    className="mb-4 flex justify-start"
  >
    <div className="rounded-2xl rounded-bl-none border border-slate-100 bg-white p-4">
      <div className="flex items-center space-x-2">
        <div className="h-2 w-2 animate-bounce rounded-full bg-slate-300 [animation-delay:-0.3s]"></div>
        <div className="h-2 w-2 animate-bounce rounded-full bg-slate-300 [animation-delay:-0.15s]"></div>
        <div className="h-2 w-2 animate-bounce rounded-full bg-slate-300"></div>
      </div>
    </div>
  </motion.div>
);

const AiMessage = ({ content }: { content: AiResponse }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.3 }}
    className="mb-4 flex justify-start"
  >
    <div className="max-w-md rounded-2xl rounded-bl-none border border-slate-100 bg-white p-4 shadow-md shadow-purple-100/50">
      <p className="whitespace-pre-wrap text-slate-700">{content.text}</p>
      {content.sources && content.sources.length > 0 && (
        <div className="mt-4 rounded-lg border border-green-200 bg-green-50 p-3">
          <span className="text-xs font-bold uppercase text-green-700">Verified Sources</span>
          <ul className="mt-2 list-inside list-decimal space-y-1">
            {content.sources.map((source, index) => (
              <li key={index} className="truncate">
                <a
                  href={source.uri}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm font-medium text-green-800 hover:underline"
                >
                  {source.title || new URL(source.uri).hostname}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  </motion.div>
);

const MentorEscalation = ({ content }: { content: AiResponse }) => {
  const { navigateTo } = useNoorStore();
  const isError = content.type === 'ERROR';
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="mb-4 flex justify-start"
    >
      <div
        className={`max-w-md rounded-2xl rounded-bl-none border p-5 shadow-lg ${
          isError
            ? 'border-red-200 bg-red-50 shadow-red-100/50'
            : 'border-purple-200 bg-purple-50 shadow-purple-100/50'
        }`}
      >
        <p className="whitespace-pre-wrap text-slate-700">{content.text}</p>
        {!isError && (
          <div className="mt-5 flex space-x-3">
            <button
              onClick={() => navigateTo('mentors')}
              className="flex-1 rounded-xl bg-gradient-to-r from-pink-500 to-purple-500 px-4 py-3 font-semibold text-white shadow-md shadow-pink-500/30 transition-all hover:brightness-110"
            >
              Meet the Mentors
            </button>
            <button className="flex-1 rounded-xl bg-slate-100 px-4 py-3 font-medium text-slate-600 ring-1 ring-slate-200 transition-all hover:bg-slate-200">
              No, thanks
            </button>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export const ChatScreen = () => {
  const { messages, isLoading, sendMessage } = useNoorStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const renderMessage = (msg: Message) => {
    if (msg.sender === 'user' && msg.userPrompt) {
      return <UserMessage key={msg.id} msg={msg.userPrompt} />;
    }

    if (msg.sender === 'ai' && msg.content) {
      switch (msg.content.type) {
        case 'VERIFIED_ANSWER':
          return <AiMessage key={msg.id} content={msg.content} />;
        case 'MENTOR_ESCALATION':
        case 'ERROR':
          return <MentorEscalation key={msg.id} content={msg.content} />;
        default:
          return null;
      }
    }
    return null;
  };

  return (
    <div className="flex h-screen flex-col bg-gradient-to-b from-purple-50 to-white font-sans">
      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        <AnimatePresence>
          {messages.map(renderMessage)}
          {isLoading && <LoadingIndicator />}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSend={sendMessage} isLoading={isLoading} />
    </div>
  );
};

