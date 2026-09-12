import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: 'customer' | 'admin';
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

function createAuthStore(): Writable<AuthState> {
  const initialState: AuthState = {
    user: null,
    token: localStorage.getItem('authToken'),
    isAuthenticated: !!localStorage.getItem('authToken'),
    isLoading: false,
    error: null,
  };

  const { subscribe, set, update } = writable<AuthState>(initialState);

  return {
    subscribe,
    set,
    update,
    login: (token: string, user: User) => {
      localStorage.setItem('authToken', token);
      update((state) => ({
        ...state,
        token,
        user,
        isAuthenticated: true,
        error: null,
      }));
    },
    logout: () => {
      localStorage.removeItem('authToken');
      update((state) => ({
        ...state,
        token: null,
        user: null,
        isAuthenticated: false,
        error: null,
      }));
    },
    setError: (error: string) => {
      update((state) => ({ ...state, error }));
    },
  };
}

export const authStore = createAuthStore();
