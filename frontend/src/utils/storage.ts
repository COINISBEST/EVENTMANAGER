export const getStoredToken = (): string | null => {
  return localStorage.getItem('token');
};

export const setStoredToken = (token: string): void => {
  localStorage.setItem('token', token);
};

export const removeStoredToken = (): void => {
  localStorage.removeItem('token');
}; 