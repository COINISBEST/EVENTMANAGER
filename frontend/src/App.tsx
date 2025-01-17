import React from 'react';
import { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { CircularProgress, Box } from '@mui/material';
import { AuthProvider } from './contexts/AuthContext';
import theme from './theme';
import ErrorBoundary from './components/common/ErrorBoundary';
import RoleBasedRoute from './components/common/RoleBasedRoute';
import { UserRole } from './types/common';

// Lazy load components
const Login = React.lazy(() => import('./components/auth/Login'));
const Register = React.lazy(() => import('./components/auth/Register'));
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const MainLayout = React.lazy(() => import('./components/layout/MainLayout'));
const ProtectedRoute = React.lazy(() => import('./components/common/ProtectedRoute'));
const AdminDashboard = React.lazy(() => import('./pages/admin/AdminDashboard'));
const FoodStallDashboard = React.lazy(() => import('./pages/stalls/FoodStallDashboard'));
const GameStallDashboard = React.lazy(() => import('./pages/stalls/GameStallDashboard'));
const VolunteerDashboard = React.lazy(() => import('./pages/volunteer/VolunteerDashboard'));
const StudentDashboard = React.lazy(() => import('./pages/student/StudentDashboard'));

const LoadingSpinner = () => (
  <Box
    sx={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
    }}
  >
    <CircularProgress />
  </Box>
);

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <Router>
            <Suspense fallback={<LoadingSpinner />}>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route
                  path="/*"
                  element={
                    <ProtectedRoute>
                      <MainLayout>
                        <Routes>
                          {/* Add your routes here */}
                        </Routes>
                      </MainLayout>
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </Suspense>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
};

export default App; 