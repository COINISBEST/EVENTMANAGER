import React from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import {
  Box,
  Button,
  TextField,
  Grid,
  Paper,
  Typography,
  Alert,
} from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { Event, EventCreate } from '../../api/types';

interface EventFormProps {
  initialValues?: Event;
  onSubmit: (values: EventCreate) => Promise<void>;
  isLoading: boolean;
  error?: string;
}

const validationSchema = Yup.object({
  name: Yup.string().required('Required'),
  description: Yup.string().required('Required'),
  venue: Yup.string().required('Required'),
  date: Yup.date().required('Required'),
  capacity: Yup.number()
    .required('Required')
    .min(1, 'Must be greater than 0'),
  poster_url: Yup.string().url('Must be a valid URL'),
});

const EventForm: React.FC<EventFormProps> = ({
  initialValues,
  onSubmit,
  isLoading,
  error,
}) => {
  const formik = useFormik({
    initialValues: initialValues || {
      name: '',
      description: '',
      venue: '',
      date: new Date(),
      capacity: 100,
      poster_url: '',
    },
    validationSchema,
    onSubmit: async (values) => {
      await onSubmit(values);
    },
  });

  return (
    <Paper sx={{ p: 3 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <form onSubmit={formik.handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              id="name"
              name="name"
              label="Event Name"
              value={formik.values.name}
              onChange={formik.handleChange}
              error={formik.touched.name && Boolean(formik.errors.name)}
              helperText={formik.touched.name && formik.errors.name}
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              id="description"
              name="description"
              label="Description"
              value={formik.values.description}
              onChange={formik.handleChange}
              error={formik.touched.description && Boolean(formik.errors.description)}
              helperText={formik.touched.description && formik.errors.description}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              id="venue"
              name="venue"
              label="Venue"
              value={formik.values.venue}
              onChange={formik.handleChange}
              error={formik.touched.venue && Boolean(formik.errors.venue)}
              helperText={formik.touched.venue && formik.errors.venue}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DateTimePicker
                label="Date and Time"
                value={formik.values.date}
                onChange={(value) => formik.setFieldValue('date', value)}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    fullWidth
                    error={formik.touched.date && Boolean(formik.errors.date)}
                    helperText={formik.touched.date && formik.errors.date}
                  />
                )}
              />
            </LocalizationProvider>
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              id="capacity"
              name="capacity"
              label="Capacity"
              type="number"
              value={formik.values.capacity}
              onChange={formik.handleChange}
              error={formik.touched.capacity && Boolean(formik.errors.capacity)}
              helperText={formik.touched.capacity && formik.errors.capacity}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              id="poster_url"
              name="poster_url"
              label="Poster URL"
              value={formik.values.poster_url}
              onChange={formik.handleChange}
              error={formik.touched.poster_url && Boolean(formik.errors.poster_url)}
              helperText={formik.touched.poster_url && formik.errors.poster_url}
            />
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
              <Button
                type="submit"
                variant="contained"
                disabled={isLoading}
              >
                {initialValues ? 'Update Event' : 'Create Event'}
              </Button>
            </Box>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default EventForm; 