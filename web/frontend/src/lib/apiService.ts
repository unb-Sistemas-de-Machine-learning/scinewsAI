import api from './api';
import { Article, Topic, User } from '@/types';

export const articlesApi = {
  // Get all articles with optional filters
  getAll: async (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    topic?: string;
  }) => {
    const response = await api.get('/api/articles/', { params });
    return response.data;
  },

  // Get single article
  getById: async (id: string) => {
    const response = await api.get(`/api/articles/${id}/`);
    return response.data as Article;
  },
};

export const topicsApi = {
  // Get all topics
  getAll: async () => {
    const response = await api.get('/api/topics/');
    return response.data as Topic[];
  },

  // Get single topic
  getById: async (id: string) => {
    const response = await api.get(`/api/topics/${id}/`);
    return response.data as Topic;
  },

  // Get articles by topic
  getArticles: async (topicId: string, params?: { skip?: number; limit?: number }) => {
    const response = await api.get(`/api/topics/${topicId}/articles/`, { params });
    return response.data;
  },
};

export const usersApi = {
  // Get current user
  getCurrentUser: async () => {
    const response = await api.get('/api/users/me/');
    return response.data as User;
  },

  // Get user by id
  getById: async (id: string) => {
    const response = await api.get(`/api/users/${id}/`);
    return response.data as User;
  },

  // Update user profile
  update: async (id: string, data: Partial<User>) => {
    const response = await api.put(`/api/users/${id}/`, data);
    return response.data as User;
  },

  // Subscribe to topic
  subscribeTopic: async (topicId: string) => {
    const response = await api.post(`/api/users/me/topics/${topicId}/subscribe/`);
    return response.data as User;
  },

  // Unsubscribe from topic
  unsubscribeTopic: async (topicId: string) => {
    const response = await api.delete(`/api/users/me/topics/${topicId}/subscribe/`);
    return response.data as User;
  },
};

export const authApi = {
  // Login - sends form-encoded data (OAuth2 standard)
  login: async (email: string, password: string) => {
    try {
      const params = new URLSearchParams();
      params.append('username', email); // OAuth2PasswordRequestForm uses 'username'
      params.append('password', password);
      
      const response = await api.post('/api/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      return response.data;
    } catch (error: any) {
      // Re-throw with better error handling
      throw error;
    }
  },

  // Register
  register: async (email: string, password: string, name: string) => {
    const response = await api.post('/api/auth/register', { email, password, name });
    return response.data;
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me/');
    return response.data as User;
  },

  // Logout
  logout: async () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
};

export const newsletterApi = {
  // Subscribe to newsletter
  subscribe: async (email: string) => {
    const response = await api.post('/api/newsletter/subscribe', { email });
    return response.data;
  },

  // Unsubscribe from newsletter
  unsubscribe: async (email: string) => {
    const response = await api.post('/api/newsletter/unsubscribe', { email });
    return response.data;
  },
};

export const likesApi = {
  // Like an article
  like: async (articleId: string) => {
    const response = await api.post(`/api/articles/${articleId}/like/`);
    return response.data;
  },

  // Unlike an article
  unlike: async (articleId: string) => {
    const response = await api.delete(`/api/articles/${articleId}/like/`);
    return response.data;
  },

  // Get like status for an article
  getStatus: async (articleId: string) => {
    const response = await api.get(`/api/articles/${articleId}/like-status/`);
    return response.data;
  },

  // Get public like count (no authentication required)
  getCount: async (articleId: string) => {
    const response = await api.get(`/api/articles/${articleId}/likes/`);
    return response.data;
  },
};
