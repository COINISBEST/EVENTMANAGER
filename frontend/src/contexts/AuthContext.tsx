import React, { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContextType, User, RegisterData } from '../types/common';
import api from '../utils/axios';

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        const response = await api.get<User>('/auth/me');
        setUser(response.data);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      setError(null);
      const response = await api.post('/auth/login', { email, password });
      const { access_token, user: userData, requires_2fa } = response.data;
      
      if (requires_2fa) {
        navigate('/2fa', { state: { temp_token: response.data.temp_token } });
        return;
      }

      localStorage.setItem('token', access_token);
      setUser(userData);
      navigate('/dashboard');
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Login failed');
      throw error;
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      localStorage.removeItem('token');
      setUser(null);
      navigate('/login');
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      setError(null);
      await api.post('/auth/register', userData);
      navigate('/login');
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Registration failed');
      throw error;
    }
  };

  const verify2FA = async (code: string) => {
    try {
      setError(null);
      const temp_token = localStorage.getItem('temp_token');
      const response = await api.post('/auth/verify-2fa', { code, temp_token });
      const { access_token, user: userData } = response.data;
      
      localStorage.setItem('token', access_token);
      localStorage.removeItem('temp_token');
      setUser(userData);
      navigate('/dashboard');
    } catch (error: any) {
      setError(error.response?.data?.detail || '2FA verification failed');
      throw error;
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    register,
    verify2FA,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext; 