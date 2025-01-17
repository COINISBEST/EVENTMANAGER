import api from '../utils/axios';
import { Order } from './types';

export const getOrders = async (params?: {
  skip?: number;
  limit?: number;
  status?: string;
}) => {
  const response = await api.get<Order[]>('/orders', { params });
  return response.data;
};

export const getOrder = async (id: number) => {
  const response = await api.get<Order>(`/orders/${id}`);
  return response.data;
};

export const createOrder = async (orderData: {
  stall_id: number;
  items: { item_id: number; quantity: number }[];
}) => {
  const response = await api.post<Order>('/orders', orderData);
  return response.data;
};

export const updateOrderStatus = async (id: number, status: string) => {
  const response = await api.patch<Order>(`/orders/${id}/status`, { status });
  return response.data;
};

export const cancelOrder = async (id: number) => {
  const response = await api.delete<Order>(`/orders/${id}`);
  return response.data;
}; 