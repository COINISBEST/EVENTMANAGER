import api from '../utils/axios';
import { Event, EventCreate, EventUpdate } from './types';

export const getEvents = async (params?: {
  skip?: number;
  limit?: number;
}) => {
  const response = await api.get<Event[]>('/events', { params });
  return response.data;
};

export const getEvent = async (id: number) => {
  const response = await api.get<Event>(`/events/${id}`);
  return response.data;
};

export const createEvent = async (eventData: EventCreate) => {
  const response = await api.post<Event>('/events', eventData);
  return response.data;
};

export const updateEvent = async (id: number, eventData: EventUpdate) => {
  const response = await api.put<Event>(`/events/${id}`, eventData);
  return response.data;
};

export const deleteEvent = async (id: number) => {
  await api.delete(`/events/${id}`);
}; 