import { ReactNode } from 'react';

export interface BaseProps {
  children?: ReactNode;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_verified: boolean;
  avatar_url?: string;
}

export enum UserRole {
  ADMIN = 'admin',
  EVENT_TEAM = 'event_team',
  VOLUNTEER = 'volunteer',
  STUDENT = 'student',
  FOOD_STALL = 'food_stall',
  GAME_STALL = 'game_stall',
}

export interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  verify2FA: (code: string) => Promise<void>;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  role: UserRole;
} 