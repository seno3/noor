import { motion, AnimatePresence } from 'framer-motion';
import { useNoorStore } from '../hooks/useNoorStore';
import { mentors } from '../data/mentors';

const MentorProfileCard = ({ mentor }: { mentor: typeof mentors[0] }) => {
  return (
    <motion.div 
      layout="position"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      transition={{ type: 'spring', stiffness: 300, damping: 25 }}
      className="w-full max-w-md rounded-2xl border border-gray-100 bg-white p-6 shadow-2xl shadow-gray-200/50"
    >
      <div className="flex flex-col sm:flex-row items-center sm:space-x-4">
        <img src={mentor.imageUrl} alt={mentor.name} className="h-20 w-20 rounded-full flex-shrink-0" />
        <div className="mt-4 sm:mt-0 text-center sm:text-left">
          <h3 className="text-xl font-bold text-gray-900">{mentor.name}</h3>
          <p className="font-medium text-pink-500">{mentor.title}</p>
        </div>
      </div>
      <p className="mt-4 text-gray-600">{mentor.bio}</p>
      
      <motion.a 
        whileTap={{ scale: 0.95 }}
        href={mentor.contactUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-6 block w-full text-center rounded-xl bg-pink-500 px-4 py-3 font-semibold text-white shadow-lg shadow-pink-500/30 transition-all hover:bg-pink-600"
      >
        Contact {mentor.name.split(' ')[0]}
      </motion.a>
    </motion.div>
  );
};

export const MentorScreen = () => {
  const { setAppState } = useNoorStore();

  return (
    <motion.div
      key="mentors"
      initial={{ opacity: 0, scale: 1.1 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ type: 'spring', stiffness: 260, damping: 20 }}
      className="flex min-h-screen w-full flex-col items-center justify-start p-6 sm:p-12 bg-gray-50"
    >
      <div className="w-full max-w-6xl">
        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={() => setAppState('welcome')}
          className="mb-8 font-semibold text-pink-500 hover:text-pink-600"
        >
          &larr; Back to Chat
        </motion.button>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ type: 'spring', stiffness: 100, delay: 0.2 }}
          className="text-center"
        >
          <h1 className="mb-12 text-center text-4xl font-bold text-gray-900">
            You're not alone.
            <br />
            <span className="text-pink-500">Meet your mentors.</span>
          </h1>
        </motion.div>
        
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-2 place-items-center">
          <AnimatePresence>
            {mentors.map((mentor) => (
              <MentorProfileCard key={mentor.id} mentor={mentor} />
            ))}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );
};

