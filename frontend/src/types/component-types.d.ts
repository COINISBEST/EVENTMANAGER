import type { ReactElement, ReactNode } from 'react';
import type { Theme } from '@mui/material/styles';

export interface BaseComponentProps {
  children?: ReactNode;
  className?: string;
}

export interface WithTheme {
  theme: Theme;
}

export interface WithError {
  error?: string | null;
}

export interface WithLoading {
  isLoading?: boolean;
}

export interface WithOnSubmit<T = any> {
  onSubmit: (data: T) => Promise<void> | void;
}

export interface WithOnClose {
  onClose: () => void;
}

export interface DialogProps extends BaseComponentProps, WithOnClose {
  open: boolean;
  title?: string;
  maxWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  fullWidth?: boolean;
}

export interface FormProps<T = any> extends BaseComponentProps, WithError, WithLoading, WithOnSubmit<T> {
  initialValues?: Partial<T>;
}

export interface ListProps<T = any> extends BaseComponentProps, WithError, WithLoading {
  items: T[];
  onItemClick?: (item: T) => void;
}

export interface CardProps<T = any> extends BaseComponentProps {
  item: T;
  onClick?: (item: T) => void;
} 