import { motion } from 'framer-motion';
import { useNoorStore } from '../hooks/useNoorStore';

const paths = [
  {
    icon: '💖',
    title: "I'm Muslim, I want to reconnect",
    subtitle: 'Grew up Muslim, looking for a gentle way back to your faith on campus.',
  },
  {
    icon: '✨',
    title: 'I recently accepted Islam',
    subtitle: 'Need safe answers and human follow-up as you start your journey.',
  },
  {
    icon: '🎓',
    title: "I'm taking an Intro to Islam class",
    subtitle: 'Using this as a guided companion for your studies.',
  },
];

export const WelcomeScreen = () => {
  const { navigateTo } = useNoorStore();

  return (
    <div className="flex min-h-screen w-full flex-col items-center justify-center bg-gradient-to-b from-purple-50 via-white to-white p-4 font-sans">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.2 }}
        className="text-center"
      >
        <span className="text-5xl">✨</span>
        <h1 className="mt-4 text-4xl font-bold text-slate-800">Welcome to Noor Path</h1>
        <p className="mt-3 text-lg text-slate-500">
          A gentle, modern guide for your Islamic journey.
          <br />
          Safe, non-judgmental support tailored to campus life.
        </p>
      </motion.div>

      <motion.h2
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.7, delay: 0.8 }}
        className="mt-20 text-2xl font-bold text-slate-700"
      >
        How can we help you?
      </motion.h2>

      <div className="mt-8 grid max-w-4xl grid-cols-1 gap-6 md:grid-cols-3">
        {paths.map((path, i) => (
          <motion.div
            key={path.title}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 1.2 + i * 0.2 }}
          >
            <button
              onClick={() => navigateTo('chat')}
              className="group h-full w-full transform rounded-2xl border border-slate-100 bg-white p-8 text-left shadow-lg shadow-purple-100/50 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl hover:shadow-purple-200/50"
            >
              <span className="text-4xl">{path.icon}</span>
              <h3 className="mt-4 text-xl font-bold text-slate-800">{path.title}</h3>
              <p className="mt-2 text-slate-500">{path.subtitle}</p>
            </button>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

