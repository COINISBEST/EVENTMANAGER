import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import EventForm from '../../components/events/EventForm';
import { createEvent } from '../../api/events';
import { EventCreate } from '../../api/types';

const CreateEvent: React.FC = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (values: EventCreate) => {
    setIsLoading(true);
    setError('');
    try {
      await createEvent(values);
      navigate('/events');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create event');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Create Event
      </Typography>
      <EventForm
        onSubmit={handleSubmit}
        isLoading={isLoading}
        error={error}
      />
    </Box>
  );
};

export default CreateEvent; 