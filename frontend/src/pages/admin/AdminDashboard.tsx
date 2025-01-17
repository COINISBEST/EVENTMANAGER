import React from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  People,
  Store,
  SportsEsports,
  EventAvailable,
  Security,
} from '@mui/icons-material';
import { useAuth } from '../../hooks/useAuth';

const AdminDashboard: React.FC = () => {
  const { user } = useAuth();

  const stats = [
    {
      title: 'Total Users',
      value: '250',
      icon: <People />,
    },
    {
      title: 'Food Stalls',
      value: '15',
      icon: <Store />,
    },
    {
      title: 'Game Stalls',
      value: '10',
      icon: <SportsEsports />,
    },
    {
      title: 'Active Events',
      value: '5',
      icon: <EventAvailable />,
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>

      <Grid container spacing={3}>
        {stats.map((stat) => (
          <Grid item xs={12} sm={6} md={3} key={stat.title}>
            <Paper sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
              <ListItemIcon>{stat.icon}</ListItemIcon>
              <Box sx={{ ml: 2 }}>
                <Typography variant="h6">{stat.value}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.title}
                </Typography>
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} sx={{ mt: 3 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activities
            </Typography>
            <List>
              {/* Add activity items here */}
            </List>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              System Health
            </Typography>
            {/* Add system health metrics here */}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AdminDashboard; 