import { AnimatePresence, motion } from 'framer-motion';
import { useNoorStore } from '../hooks/useNoorStore';
import { WelcomeScreen } from '../components/WelcomeScreen';
import { ChatScreen } from '../components/ChatScreen';
import { MentorScreen } from '../components/MentorScreen';

const pageVariants = {
  initial: { opacity: 0 },
  in: { opacity: 1 },
  out: { opacity: 0 },
};

const pageTransition = {
  type: 'tween',
  ease: 'anticipate',
  duration: 0.5,
};

export default function Home() {
  const { appState } = useNoorStore();

  return (
    <div className="relative h-screen overflow-hidden">
      <AnimatePresence mode="wait">
        {appState === 'welcome' && (
          <motion.div
            key="welcome"
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
            className="h-full w-full"
          >
            <WelcomeScreen />
          </motion.div>
        )}

        {appState === 'chat' && (
          <motion.div
            key="chat"
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
            className="h-full w-full"
          >
            <ChatScreen />
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {(appState === 'mentors' || appState === 'scheduling') && <MentorScreen />}
      </AnimatePresence>
    </div>
  );
}

