import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  role: string;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  sessionExpired: boolean;
  setAuth: (user: User, token: string) => void;
  setAccessToken: (token: string) => void;
  setUser: (user: User) => void;
  logout: (expired?: boolean) => void;
  clearSessionExpired: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  accessToken: null,
  isAuthenticated: false,
  sessionExpired: false,
  setAuth: (user, token) => set({ user, accessToken: token, isAuthenticated: true, sessionExpired: false }),
  setAccessToken: (token) => set({ accessToken: token }),
  setUser: (user) => set({ user, isAuthenticated: true }),
  logout: (expired = false) => set({ user: null, accessToken: null, isAuthenticated: false, sessionExpired: expired }),
  clearSessionExpired: () => set({ sessionExpired: false }),
}));
