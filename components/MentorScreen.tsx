import { motion, AnimatePresence } from 'framer-motion';
import { useNoorStore } from '../hooks/useNoorStore';
import { mentors } from '../data/mentors';

const BackgroundEffects = () => {
  const shapes = Array.from({ length: 6 }, (_, i) => i);
  
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none" style={{ zIndex: -1 }}>
      <div 
        className="absolute inset-0"
        style={{
          background: 'linear-gradient(to bottom, #ffffff 0%, #d1fae5 60%, #a7f3d0 100%)',
        }}
      />
      <div 
        className="absolute inset-0 opacity-[0.15]"
        style={{
          backgroundImage: `
            url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E"),
            url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.4'/%3E%3C/svg%3E")
          `,
          backgroundSize: '200px 200px, 300px 300px',
          mixBlendMode: 'multiply',
        }}
      />
      {shapes.map((i) => (
        <motion.div
          key={i}
          className="absolute rounded-full bg-green-200/20 blur-2xl"
          style={{
            width: `${100 + i * 40}px`,
            height: `${100 + i * 40}px`,
            left: `${(i * 16) % 100}%`,
            top: `${15 + (i * 18) % 65}%`,
          }}
          animate={{
            x: [0, Math.sin(i) * 50, 0],
            y: [0, Math.cos(i) * 50, 0],
            scale: [1, 1.4 + i * 0.1, 1],
            opacity: [0.15, 0.35, 0.15],
          }}
          transition={{
            duration: 18 + i * 4,
            repeat: Infinity,
            ease: "easeInOut",
            delay: i * 1.2,
          }}
        />
      ))}
    </div>
  );
};

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
          <p className="font-medium text-green-500">{mentor.title}</p>
        </div>
      </div>
      <p className="mt-4 text-gray-600">{mentor.bio}</p>
      
      <motion.a 
        whileTap={{ scale: 0.95 }}
        href={mentor.contactUrl}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-6 block w-full text-center rounded-xl bg-green-500 px-4 py-3 font-semibold text-white shadow-lg shadow-green-500/30 transition-all hover:bg-green-600"
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
      className="flex min-h-screen w-full flex-col items-center justify-start p-6 sm:p-12 relative"
    >
      <BackgroundEffects />
      <div className="w-full max-w-6xl relative z-10">
        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={() => setAppState('welcome')}
          className="mb-8 font-semibold text-green-500 hover:text-green-600"
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
            <span className="text-green-500">Meet your mentors.</span>
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

