import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNoorStore, Message, AiResponse } from '../hooks/useNoorStore';

const typingOptions = [
  "I want to reconnect",
  "I recently accepted Islam",
  "I'm in an Intro to Islam class"
];

const useTypingEffect = (options: string[], typingSpeed: number = 100, deletingSpeed: number = 50, pauseDuration: number = 2000) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [displayText, setDisplayText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const currentOption = options[currentIndex];
    
    if (!isDeleting) {
      if (displayText.length < currentOption.length) {
        const timeout = setTimeout(() => {
          setDisplayText(currentOption.slice(0, displayText.length + 1));
        }, typingSpeed);
        return () => clearTimeout(timeout);
      } else {
        const timeout = setTimeout(() => {
          setIsDeleting(true);
        }, pauseDuration);
        return () => clearTimeout(timeout);
      }
    } else {
      if (displayText.length > 0) {
        const timeout = setTimeout(() => {
          setDisplayText(currentOption.slice(0, displayText.length - 1));
        }, deletingSpeed);
        return () => clearTimeout(timeout);
      } else {
        setIsDeleting(false);
        setCurrentIndex((prev) => (prev + 1) % options.length);
      }
    }
  }, [displayText, isDeleting, currentIndex, options, typingSpeed, deletingSpeed, pauseDuration]);

  return displayText;
};

const ChatInput = ({ onSend, isLoading }: { onSend: (val: string) => void; isLoading: boolean }) => {
  const [value, setValue] = useState('');
  const typingText = useTypingEffect(typingOptions);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (value.trim() && !isLoading) { 
      onSend(value); 
      setValue(''); 
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mx-auto mt-4">
      <div className="flex items-center rounded-xl bg-white p-2 shadow-2xl shadow-pink-500/10 ring-1 ring-gray-100">
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={typingText || "Ask a question..."}
          className="flex-1 bg-transparent px-4 text-gray-900 placeholder-gray-400 focus:outline-none"
          disabled={isLoading}
        />
        <motion.button
          whileTap={{ scale: 0.9 }}
          type="submit"
          className="rounded-lg bg-pink-500 p-3 text-white shadow-lg shadow-pink-500/30 transition-all hover:bg-pink-600 disabled:opacity-50"
          disabled={isLoading}
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-5 w-5 rotate-90">
            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009.5 16.571V11.5a1 1 0 012 0v5.071a1 1 0 00.223.632l5 1.429a1 1 0 001.17-1.409l-7-14z" />
          </svg>
        </motion.button>
      </div>
    </form>
  );
};

const UserMessage = ({ msg }: { msg: string }) => (
  <motion.div
    layout
    initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ type: 'spring', stiffness: 300, damping: 20 }}
    className="mb-4 flex justify-end"
  >
    <div className="max-w-md rounded-2xl rounded-br-none bg-pink-500 p-4 text-white shadow-lg shadow-pink-500/30">
      {msg}
    </div>
  </motion.div>
);
const LoadingIndicator = () => (
  <motion.div
    layout
    initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
    className="flex justify-start mb-4"
  >
    <div className="rounded-2xl rounded-bl-none border border-gray-100 bg-white p-4">
      <div className="flex items-center space-x-2">
        <div className="h-2 w-2 animate-bounce rounded-full bg-gray-300 [animation-delay:-0.3s]"></div>
        <div className="h-2 w-2 animate-bounce rounded-full bg-gray-300 [animation-delay:-0.15s]"></div>
        <div className="h-2 w-2 animate-bounce rounded-full bg-gray-300"></div>
      </div>
    </div>
  </motion.div>
);
const AiMessage = ({ content }: { content: AiResponse }) => (
  <motion.div
    layout
    initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ type: 'spring', stiffness: 300, damping: 20 }}
    className="mb-4 flex justify-start"
  >
    <div className="max-w-md rounded-2xl rounded-bl-none border border-gray-100 bg-white p-4 text-gray-800 shadow-md shadow-gray-100">
      <p className="whitespace-pre-wrap">{content.text}</p>
      {content.sources && content.sources.length > 0 && (
        <div className="mt-4 rounded-lg border border-green-200 bg-green-50 p-3">
          <span className="text-xs font-bold uppercase text-green-700">Verified Sources</span>
          <ul className="mt-2 list-inside list-decimal space-y-1">
            {content.sources.map((source, index) => (
              <li key={index} className="truncate">
                <a href={source.uri} target="_blank" rel="noopener noreferrer" className="text-sm font-medium text-green-800 hover:underline">
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
  const { setAppState } = useNoorStore();
  const isError = content.type === 'ERROR';
  
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ type: 'spring', stiffness: 300, damping: 20 }}
      className="mb-4 flex justify-start"
    >
      <div className={`max-w-md rounded-2xl rounded-bl-none border p-5 shadow-lg ${
          isError 
          ? 'border-red-200 bg-red-50 text-red-800 shadow-red-100' 
          : 'border-pink-200 bg-pink-50 text-pink-800 shadow-pink-100'
      }`}>
        <p className="whitespace-pre-wrap font-medium">{content.text}</p>
        {!isError && (
          <div className="mt-5 flex space-x-3">
            <motion.button 
              whileTap={{ scale: 0.95 }}
              onClick={() => setAppState('mentors')}
              className="flex-1 rounded-xl bg-pink-500 px-4 py-3 font-semibold text-white shadow-lg shadow-pink-500/30 transition-all hover:bg-pink-600">
              Meet the Mentors
            </motion.button>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export const WelcomeScreen = () => {
  const { messages, isLoading, sendMessage, setAppState } = useNoorStore();
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
        case 'VERIFIED_ANSWER': return <AiMessage key={msg.id} content={msg.content} />;
        case 'MENTOR_ESCALATION':
        case 'ERROR': return <MentorEscalation key={msg.id} content={msg.content} />;
        default: return null;
      }
    }
    return null;
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        delayChildren: 0.3,
        staggerChildren: 0.2,
      },
    },
    exit: {
      opacity: 0,
      transition: { duration: 0.3 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { type: 'spring', stiffness: 100 }
    },
  };

  return (
    <motion.div
      key="welcome"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="flex min-h-screen w-full flex-col bg-white text-gray-900"
    >
      <motion.div variants={itemVariants} className="text-center pt-12 pb-8 px-4">
        <motion.div
          animate={{ scale: [1, 1.2, 1], rotate: [0, -10, 10, 0] }}
          transition={{ repeat: Infinity, duration: 2, delay: 1 }}
          className="mb-4 text-6xl"
        >
          ✨
        </motion.div>
        <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-7xl">Noor Path</h1>
        <p className="mt-4 text-xl text-gray-600">
          A gentle, modern guide for your Islamic journey.
        </p>
      </motion.div>

      <div className="flex-1 flex flex-col max-w-2xl mx-auto w-full px-4 pb-4">
        <div className="flex-1 space-y-4 overflow-y-auto min-h-0">
          <AnimatePresence>
            {messages.map(renderMessage)}
            {isLoading && <LoadingIndicator />}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>
        
        <div className="pt-4">
          <ChatInput onSend={sendMessage} isLoading={isLoading} />
        </div>
      </div>
    </motion.div>
  );
};
