import Head from 'next/head';
import { motion, AnimatePresence } from 'framer-motion';
import { useNoorStore } from '../hooks/useNoorStore';
import { WelcomeScreen } from '../components/WelcomeScreen';
import { MentorScreen } from '../components/MentorScreen';

export default function Home() {
  const { appState } = useNoorStore();

  return (
    <>
      <Head>
        <title>Noor - Your Guided Journey</title>
        <meta name="description" content="A safe, verified guide for your Islamic journey." />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <AnimatePresence mode="wait">
        {appState === 'welcome' && <WelcomeScreen />}
        {appState === 'mentors' && <MentorScreen />}
      </AnimatePresence>
    </>
  );
}
