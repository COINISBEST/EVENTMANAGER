import { Theme } from '@mui/material/styles';

declare module '@mui/styles/defaultTheme' {
  interface DefaultTheme extends Theme {}
}

declare global {
  interface Window {
    config: {
      API_URL: string;
    };
  }
}

export {}; 