import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardMedia,
  Grid,
  Typography,
  IconButton,
  Chip,
  Pagination,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { getEvents } from '../../api/events';
import { Event } from '../../api/types';
import { format } from 'date-fns';
import Loading from '../../components/common/Loading';

const EventsList: React.FC = () => {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();
  const limit = 12;

  useEffect(() => {
    fetchEvents();
  }, [page]);

  const fetchEvents = async () => {
    try {
      const data = await getEvents({
        skip: (page - 1) * limit,
        limit,
      });
      setEvents(data);
      // Assuming the total count comes from the backend
      // setTotalPages(Math.ceil(totalCount / limit));
    } catch (error) {
      console.error('Failed to fetch events:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Events</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => navigate('/events/create')}
        >
          Create Event
        </Button>
      </Box>

      <Grid container spacing={3}>
        {events.map((event) => (
          <Grid item xs={12} sm={6} md={4} key={event.id}>
            <Card>
              {event.poster_url && (
                <CardMedia
                  component="img"
                  height="140"
                  image={event.poster_url}
                  alt={event.name}
                />
              )}
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="h6" gutterBottom>
                    {event.name}
                  </Typography>
                  <Chip
                    label={event.is_active ? 'Active' : 'Inactive'}
                    color={event.is_active ? 'success' : 'default'}
                    size="small"
                  />
                </Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {format(new Date(event.date), 'PPP')}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {event.venue}
                </Typography>
                <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                  <IconButton
                    size="small"
                    onClick={() => navigate(`/events/${event.id}/edit`)}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton size="small" color="error">
                    <DeleteIcon />
                  </IconButton>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <Pagination
          count={totalPages}
          page={page}
          onChange={(_, value) => setPage(value)}
          color="primary"
        />
      </Box>
    </Box>
  );
};

export default EventsList; 