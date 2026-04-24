import { create } from 'zustand';
import { AuthState } from './auth';

interface AppState extends AuthState {
  isLoading: boolean;
  error: string | null;
  setAuth: (auth: AuthState) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  isAuthenticated: false,
  user: null,
  session: null,
  token: null,
  isLoading: false,
  error: null,

  setAuth: (auth) => set({ ...auth }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));