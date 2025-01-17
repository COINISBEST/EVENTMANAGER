import React from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardMedia,
  Button,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  Event as EventIcon,
  ConfirmationNumber as TicketIcon,
  Receipt as ReceiptIcon,
} from '@mui/icons-material';

interface Ticket {
  id: number;
  eventName: string;
  date: string;
  ticketType: string;
  status: 'valid' | 'used' | 'expired';
}

const StudentDashboard: React.FC = () => {
  const tickets: Ticket[] = [
    {
      id: 1,
      eventName: 'Tech Conference 2024',
      date: '2024-03-15',
      ticketType: 'Regular',
      status: 'valid',
    },
    // Add more tickets
  ];

  const getStatusColor = (status: Ticket['status']) => {
    switch (status) {
      case 'valid':
        return 'success';
      case 'used':
        return 'default';
      case 'expired':
        return 'error';
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              My Tickets
            </Typography>
            <List>
              {tickets.map((ticket) => (
                <ListItem
                  key={ticket.id}
                  sx={{ borderBottom: 1, borderColor: 'divider' }}
                >
                  <ListItemText
                    primary={ticket.eventName}
                    secondary={
                      <>
                        <Typography component="span" variant="body2">
                          Date: {new Date(ticket.date).toLocaleDateString()}
                        </Typography>
                        <br />
                        <Typography component="span" variant="body2">
                          Type: {ticket.ticketType}
                        </Typography>
                      </>
                    }
                  />
                  <ListItemSecondaryAction>
                    <Chip
                      label={ticket.status}
                      color={getStatusColor(ticket.status)}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => {/* Handle view ticket */}}
                    >
                      View
                    </Button>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>

          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Upcoming Events
            </Typography>
            <Grid container spacing={2}>
              {/* Add event cards here */}
              <Grid item xs={12} sm={6}>
                <Card>
                  <CardMedia
                    component="img"
                    height="140"
                    image="https://source.unsplash.com/random/400x200?event"
                    alt="Event"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h6">
                      Spring Festival
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Join us for an amazing celebration of spring with music, food, and games!
                    </Typography>
                    <Button
                      variant="contained"
                      size="small"
                      sx={{ mt: 2 }}
                      onClick={() => {/* Handle book ticket */}}
                    >
                      Book Ticket
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <List>
              <ListItem button onClick={() => {/* Handle browse events */}}>
                <EventIcon sx={{ mr: 2 }} />
                <ListItemText primary="Browse Events" />
              </ListItem>
              <ListItem button onClick={() => {/* Handle view tickets */}}>
                <TicketIcon sx={{ mr: 2 }} />
                <ListItemText primary="My Tickets" />
              </ListItem>
              <ListItem button onClick={() => {/* Handle view orders */}}>
                <ReceiptIcon sx={{ mr: 2 }} />
                <ListItemText primary="Order History" />
              </ListItem>
            </List>
          </Paper>

          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            <List>
              {/* Add activity items here */}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StudentDashboard; 