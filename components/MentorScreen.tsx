import { motion, AnimatePresence } from 'framer-motion';
import { useNoorStore } from '../hooks/useNoorStore';
import { mentors } from '../data/mentors';
import { InlineWidget } from 'react-calendly';

const MentorProfileCard = ({ mentor }: { mentor: (typeof mentors)[0] }) => {
  const { startScheduling } = useNoorStore();

  return (
    <div className="rounded-2xl border border-slate-100 bg-white p-6 shadow-lg shadow-purple-100/50">
      <div className="flex items-center space-x-4">
        <img src={mentor.imageUrl} alt={mentor.name} className="h-20 w-20 rounded-full" />
        <div>
          <h3 className="text-xl font-bold text-slate-800">{mentor.name}</h3>
          <p className="text-purple-600">{mentor.title}</p>
        </div>
      </div>
      <p className="mt-4 text-slate-600">{mentor.bio}</p>
      <button
        onClick={() => startScheduling(mentor.calendlyUrl)}
        className="mt-6 w-full rounded-xl bg-gradient-to-r from-pink-500 to-purple-500 px-4 py-3 font-semibold text-white shadow-md shadow-pink-500/30 transition-all hover:brightness-110"
      >
        Schedule a Chat
      </button>
    </div>
  );
};

export const CalendlyEmbed = () => {
  const { selectedMentorUrl, navigateTo } = useNoorStore();

  return (
    <div className="p-4 md:p-8">
      <button
        onClick={() => navigateTo('mentors')}
        className="mb-4 font-semibold text-purple-600 hover:text-purple-800"
      >
        &larr; Back to Mentors
      </button>
      <div className="h-[700px] overflow-hidden rounded-2xl shadow-2xl shadow-purple-200/50">
        <InlineWidget url={selectedMentorUrl} styles={{ height: '700px', width: '100%' }} />
      </div>
    </div>
  );
};

export const MentorScreen = () => {
  const { appState, navigateTo } = useNoorStore();

  return (
    <motion.div
      className="absolute inset-0 z-10 flex h-screen flex-col overflow-y-auto bg-white font-sans"
      initial={{ x: '100%' }}
      animate={{ x: 0 }}
      exit={{ x: '100%' }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
    >
      <div className="flex-shrink-0 p-6 shadow-sm shadow-purple-100/50">
        <button
          onClick={() => navigateTo('chat')}
          className="mb-2 font-semibold text-purple-600 hover:text-purple-800"
        >
          &larr; Back to Chat
        </button>
        <h1 className="text-3xl font-bold text-slate-800">Meet Your Mentors</h1>
        <p className="mt-2 text-lg text-slate-500">
          Our mentors are UIUC students just like you, trained to listen and help.
        </p>
      </div>

      <div className="flex-1 bg-gradient-to-b from-purple-50 to-white p-6">
        <AnimatePresence mode="wait">
          {appState === 'mentors' && (
            <motion.div
              key="mentor-list"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="mx-auto max-w-4xl space-y-6"
            >
              {mentors.map((mentor) => (
                <MentorProfileCard key={mentor.id} mentor={mentor} />
              ))}
            </motion.div>
          )}

          {appState === 'scheduling' && (
            <motion.div
              key="calendly-embed"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="mx-auto max-w-4xl"
            >
              <CalendlyEmbed />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

