import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
} from '@mui/material';
import {
  Event as EventIcon,
  Person as PersonIcon,
  Security as SecurityIcon,
  Notifications as NotificationsIcon,
} from '@mui/icons-material';
import { useAuth } from '../hooks/useAuth';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  const stats = [
    {
      title: 'Active Events',
      value: '5',
      icon: <EventIcon sx={{ fontSize: 40 }} />,
      color: '#4caf50',
    },
    {
      title: 'Total Users',
      value: '150',
      icon: <PersonIcon sx={{ fontSize: 40 }} />,
      color: '#2196f3',
    },
    {
      title: 'Security Score',
      value: '85%',
      icon: <SecurityIcon sx={{ fontSize: 40 }} />,
      color: '#ff9800',
    },
    {
      title: 'Notifications',
      value: user?.unread_notifications.toString() || '0',
      icon: <NotificationsIcon sx={{ fontSize: 40 }} />,
      color: '#f44336',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Welcome back, {user?.full_name}
      </Typography>

      <Grid container spacing={3}>
        {stats.map((stat) => (
          <Grid item xs={12} sm={6} md={3} key={stat.title}>
            <Paper
              sx={{
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                height: 140,
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <Typography color="textSecondary" gutterBottom>
                  {stat.title}
                </Typography>
                <Box sx={{ color: stat.color }}>{stat.icon}</Box>
              </Box>
              <Typography component="p" variant="h4">
                {stat.value}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} sx={{ mt: 3 }}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Events
            </Typography>
            {/* Add event list component here */}
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Activity Feed
            </Typography>
            {/* Add activity feed component here */}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 