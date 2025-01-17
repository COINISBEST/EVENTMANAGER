import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import EventForm from '../../components/events/EventForm';
import { getEvent, updateEvent } from '../../api/events';
import { Event, EventUpdate } from '../../api/types';
import Loading from '../../components/common/Loading';

const EditEvent: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [event, setEvent] = useState<Event | null>(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    fetchEvent();
  }, [id]);

  const fetchEvent = async () => {
    try {
      if (!id) return;
      const data = await getEvent(parseInt(id));
      setEvent(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch event');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (values: EventUpdate) => {
    if (!id) return;
    setIsSaving(true);
    setError('');
    try {
      await updateEvent(parseInt(id), values);
      navigate('/events');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update event');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <Loading />;
  }

  if (!event) {
    return (
      <Typography color="error">
        Event not found
      </Typography>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Edit Event: {event.name}
      </Typography>
      <EventForm
        initialValues={event}
        onSubmit={handleSubmit}
        isLoading={isSaving}
        error={error}
      />
    </Box>
  );
};

export default EditEvent; 