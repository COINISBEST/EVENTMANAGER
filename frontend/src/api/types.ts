export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_verified: boolean;
  unread_notifications: number;
}

export enum UserRole {
  ADMIN = 'admin',
  EVENT_TEAM = 'event_team',
  VOLUNTEER = 'volunteer',
  STUDENT = 'student',
  FOOD_STALL = 'food_stall',
  GAME_STALL = 'game_stall',
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
  requires_2fa?: boolean;
  temp_token?: string;
}

export interface Device {
  id: string;
  device_name: string;
  ip_address: string;
  last_used: string;
  is_trusted: boolean;
  location_city?: string;
  location_country?: string;
}

export interface SecurityStatus {
  devices: number;
  trusted_devices: number;
  suspicious_devices: number;
  has_2fa: boolean;
  security_score: number;
  recent_activities: Activity[];
}

export interface Activity {
  id: number;
  activity_type: string;
  description: string;
  ip_address: string;
  created_at: string;
}

export interface Event {
  id: number;
  name: string;
  description: string;
  venue: string;
  date: string;
  capacity: number;
  poster_url?: string;
  is_active: boolean;
  created_at: string;
  created_by: number;
}

export interface EventCreate {
  name: string;
  description: string;
  venue: string;
  date: string;
  capacity: number;
  poster_url?: string;
}

export interface EventUpdate extends Partial<EventCreate> {
  is_active?: boolean;
}

export interface Order {
  id: number;
  user_id: number;
  stall_id: number;
  status: OrderStatus;
  total_amount: number;
  created_at: string;
  items: OrderItem[];
}

export interface OrderItem {
  id: number;
  item_id: number;
  name: string;
  quantity: number;
  price: number;
  subtotal: number;
}

export enum OrderStatus {
  PENDING = 'pending',
  PREPARING = 'preparing',
  READY = 'ready',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled'
}

export interface MenuItem {
  id: number;
  stall_id: number;
  name: string;
  description: string;
  price: number;
  image_url?: string;
  is_available: boolean;
  category: string;
} 