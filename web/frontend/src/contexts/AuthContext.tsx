import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, ProfileType } from '@/types';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  signup: (email: string, password: string, name: string, profileType: ProfileType) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  updateProfile: (updates: Partial<User>) => void;
  subscribeToTopic: (topicId: string) => void;
  unsubscribeFromTopic: (topicId: string) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Mock user storage (replace with actual API calls)
const STORAGE_KEY = 'scinewsai_user';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch {
        localStorage.removeItem(STORAGE_KEY);
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    // Mock login - replace with API call
    if (!email || !password) {
      return { success: false, error: 'E-mail e senha são obrigatórios!' };
    }

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Mock successful login
    const mockUser: User = {
      id: 'user-' + Date.now(),
      email,
      name: email.split('@')[0],
      profile_type: 'student',
      subscribed_topics: [],
      created_at: new Date().toISOString(),
    };

    setUser(mockUser);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(mockUser));
    return { success: true };
  };

  const signup = async (
    email: string, 
    password: string, 
    name: string, 
    profileType: ProfileType
  ): Promise<{ success: boolean; error?: string }> => {
    if (!email || !password || !name) {
      return { success: false, error: 'Todos os campos são obrigatórios!' };
    }

    if (password.length < 8) {
      return { success: false, error: 'A senha deve ter ao menos 8 caracteres' };
    }

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    const newUser: User = {
      id: 'user-' + Date.now(),
      email,
      name,
      profile_type: profileType,
      subscribed_topics: [],
      created_at: new Date().toISOString(),
    };

    setUser(newUser);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newUser));
    return { success: true };
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem(STORAGE_KEY);
  };

  const updateProfile = (updates: Partial<User>) => {
    if (user) {
      const updated = { ...user, ...updates };
      setUser(updated);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    }
  };

  const subscribeToTopic = (topicId: string) => {
    if (user && !user.subscribed_topics.includes(topicId)) {
      updateProfile({
        subscribed_topics: [...user.subscribed_topics, topicId],
      });
    }
  };

  const unsubscribeFromTopic = (topicId: string) => {
    if (user) {
      updateProfile({
        subscribed_topics: user.subscribed_topics.filter(id => id !== topicId),
      });
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        signup,
        logout,
        updateProfile,
        subscribeToTopic,
        unsubscribeFromTopic,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
}
