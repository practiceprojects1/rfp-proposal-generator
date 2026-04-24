import type { AppProps } from 'next/app';
import '../styles/globals.css';
import { useEffect } from 'react';
import { useAppStore } from '../lib/store';
import { authService } from '../lib/auth';

export default function App({ Component, pageProps }: AppProps) {
  const setAuth = useAppStore((state) => state.setAuth);

  useEffect(() => {
    // Check for existing session on load
    authService.getCurrentSession().then((session) => {
      if (session) {
        setAuth({
          isAuthenticated: true,
          user: authService.getCurrentUser(),
          session,
          token: session.getIdToken().getJwtToken(),
        });
        localStorage.setItem('authToken', session.getIdToken().getJwtToken());
      }
    });
  }, [setAuth]);

  return <Component {...pageProps} />;
}