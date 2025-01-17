declare module 'axios' {
  export interface AxiosResponse<T = any> {
    data: T;
    status: number;
    statusText: string;
    headers: any;
    config: any;
    request?: any;
  }

  export interface AxiosError<T = any> extends Error {
    config: any;
    code?: string;
    request?: any;
    response?: AxiosResponse<T>;
    isAxiosError: boolean;
    toJSON: () => object;
  }
}

declare module '@mui/material/*';
declare module '@mui/icons-material/*';
declare module '@mui/lab/*';
declare module '@mui/system';
declare module '@mui/styles';
declare module '@mui/x-date-pickers/*';
declare module 'formik';
declare module 'yup'; 