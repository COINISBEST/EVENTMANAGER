import api from '../utils/axios';
import { MenuItem } from './types';

export const getMenuItems = async (stallId: number) => {
  const response = await api.get<MenuItem[]>(`/stalls/${stallId}/menu-items`);
  return response.data;
};

export const createMenuItem = async (stallId: number, itemData: Omit<MenuItem, 'id' | 'stall_id'>) => {
  const response = await api.post<MenuItem>(`/stalls/${stallId}/menu-items`, itemData);
  return response.data;
};

export const updateMenuItem = async (
  stallId: number,
  itemId: number,
  itemData: Partial<MenuItem>
) => {
  const response = await api.put<MenuItem>(
    `/stalls/${stallId}/menu-items/${itemId}`,
    itemData
  );
  return response.data;
};

export const deleteMenuItem = async (stallId: number, itemId: number) => {
  await api.delete(`/stalls/${stallId}/menu-items/${itemId}`);
}; 