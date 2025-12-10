import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, ProfileType } from '@/types';
import { authApi } from '@/lib/apiService';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  signup: (email: string, password: string, name: string, profileType: ProfileType) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  updateProfile: (updates: Partial<User>) => void;
  subscribeToTopic: (topicId: string) => void;
  unsubscribeFromTopic: (topicId: string) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// User storage key
const STORAGE_KEY = 'scinewsai_user';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for token first - if no token, user is not authenticated
    const token = localStorage.getItem('access_token');
    const stored = localStorage.getItem(STORAGE_KEY);
    
    // Only restore user if token exists
    if (token && stored) {
      try {
        const parsedUser = JSON.parse(stored);
        // Validate that user has required fields
        if (parsedUser.id && parsedUser.email) {
          setUser(parsedUser);
        } else {
          localStorage.removeItem(STORAGE_KEY);
          localStorage.removeItem('access_token');
        }
      } catch (e) {
        console.error('Error parsing stored user:', e);
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem('access_token');
      }
    } else if (!token && stored) {
      // If token doesn't exist but user data does, clear it
      localStorage.removeItem(STORAGE_KEY);
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      if (!email || !password) {
        return { success: false, error: 'E-mail e senha são obrigatórios!' };
      }

      const response = await authApi.login(email, password);
      
      if (response.access_token) {
        localStorage.setItem('access_token', response.access_token);
        if (response.refresh_token) {
          localStorage.setItem('refresh_token', response.refresh_token);
        }
        
        // Get current user - only if we have a valid token
        try {
          const userResponse = await authApi.getCurrentUser();
          if (userResponse && userResponse.id) {
            setUser(userResponse);
            localStorage.setItem(STORAGE_KEY, JSON.stringify(userResponse));
            return { success: true };
          }
        } catch (userError) {
          console.error('Error fetching current user:', userError);
          // Still consider login successful if we have a token
          return { success: true };
        }
      }
      
      return { success: false, error: 'Falha no login' };
    } catch (error: any) {
      console.error('Login error:', error);
      
      // Make sure user is not set on error
      setUser(null);
      
      // Try to extract error message from different response formats
      let errorMessage = 'Erro ao fazer login';
      
      if (error?.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error?.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error?.message) {
        errorMessage = error.message;
      }
      
      return { success: false, error: errorMessage };
    }
  };

  const signup = async (
    email: string, 
    password: string, 
    name: string, 
    profileType: ProfileType
  ): Promise<{ success: boolean; error?: string }> => {
    try {
      if (!email || !password || !name) {
        return { success: false, error: 'Todos os campos são obrigatórios!' };
      }

      if (password.length < 8) {
        return { success: false, error: 'A senha deve ter ao menos 8 caracteres' };
      }

      const response = await authApi.register(email, password, name);
      
      if (response.access_token) {
        localStorage.setItem('access_token', response.access_token);
        if (response.refresh_token) {
          localStorage.setItem('refresh_token', response.refresh_token);
        }
        
        const newUser: User = {
          id: response.user?.id || 'user-' + Date.now(),
          email,
          name,
          profile_type: profileType,
          subscribed_topics: [],
          created_at: new Date().toISOString(),
        };
        
        setUser(newUser);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(newUser));
        return { success: true };
      }
      
      return { success: false, error: 'Falha no registro' };
    } catch (error: any) {
      console.error('Signup error:', error);
      return { success: false, error: error?.response?.data?.detail || 'Erro ao se registrar' };
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
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
        setUser,
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
