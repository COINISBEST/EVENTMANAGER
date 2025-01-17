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
  Chip,
} from '@mui/material';
import {
  Assignment as AssignmentIcon,
  Event as EventIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';

interface Assignment {
  id: number;
  eventName: string;
  role: string;
  time: string;
  status: 'pending' | 'active' | 'completed';
}

const VolunteerDashboard: React.FC = () => {
  const assignments: Assignment[] = [
    {
      id: 1,
      eventName: 'Tech Conference',
      role: 'Registration Desk',
      time: '9:00 AM - 12:00 PM',
      status: 'active',
    },
    // Add more assignments
  ];

  const getStatusColor = (status: Assignment['status']) => {
    switch (status) {
      case 'pending':
        return 'warning';
      case 'active':
        return 'success';
      case 'completed':
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Volunteer Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              My Assignments
            </Typography>
            <List>
              {assignments.map((assignment) => (
                <ListItem
                  key={assignment.id}
                  sx={{ borderBottom: 1, borderColor: 'divider' }}
                >
                  <ListItemIcon>
                    <AssignmentIcon />
                  </ListItemIcon>
                  <ListItemText
                    primary={assignment.eventName}
                    secondary={
                      <>
                        <Typography component="span" variant="body2">
                          {assignment.role}
                        </Typography>
                        <br />
                        <Typography component="span" variant="body2" color="text.secondary">
                          {assignment.time}
                        </Typography>
                      </>
                    }
                  />
                  <Chip
                    label={assignment.status}
                    color={getStatusColor(assignment.status)}
                    size="small"
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              Upcoming Events
            </Typography>
            {/* Add upcoming events list */}
          </Paper>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Schedule
            </Typography>
            {/* Add schedule calendar */}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default VolunteerDashboard; 