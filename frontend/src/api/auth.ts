import api from '../utils/axios';
import { LoginResponse, User } from './types';

export const login = async (email: string, password: string): Promise<LoginResponse> => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);
  
  const response = await api.post<LoginResponse>('/token', formData);
  return response.data;
};

export const register = async (userData: {
  email: string;
  password: string;
  full_name: string;
  role: string;
}) => {
  const response = await api.post('/register', userData);
  return response.data;
};

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get('/users/me');
  return response.data;
};

export const logout = async () => {
  await api.post('/logout');
};

export const verify2FA = async (token: string) => {
  const response = await api.post('/2fa/verify', { token });
  return response.data;
};

export const setup2FA = async () => {
  const response = await api.post('/2fa/setup');
  return response.data;
}; 