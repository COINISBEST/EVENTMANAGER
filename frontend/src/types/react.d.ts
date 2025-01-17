import React from 'react';
import { Theme } from '@mui/material/styles';

declare module 'react' {
  interface FunctionComponent<P = {}> {
    (props: P, context?: any): ReactElement<any, any> | null;
  }
}

declare module '@mui/material/styles' {
  interface Theme {
    status: {
      danger: string;
    };
  }
  interface ThemeOptions {
    status?: {
      danger?: string;
    };
  }
} 