import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { AnimatePresence } from 'framer-motion';
import Head from 'next/head';

function MyApp({ Component, pageProps, router }: AppProps) {
  return (
    <>
      <Head>
        <title>Noor Path - Your Guided Journey</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </Head>
      <AnimatePresence mode="wait">
        <Component {...pageProps} key={router.asPath} />
      </AnimatePresence>
    </>
  );
}

export default MyApp;

