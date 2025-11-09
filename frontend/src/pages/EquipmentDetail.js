import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Paper,
  Typography,
  Button,
  Box,
  CircularProgress,
  TextField,
  Alert,
  Chip,
  Grid,
} from '@mui/material';
import api from '../services/api';

const EquipmentDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [equipment, setEquipment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [requesting, setRequesting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [formData, setFormData] = useState({
    start_date: '',
    end_date: '',
  });

  useEffect(() => {
    fetchEquipment();
  }, [id]);

  const fetchEquipment = async () => {
    try {
      const response = await api.get(`/equipment/${id}`);
      setEquipment(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching equipment:', error);
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setRequesting(true);

    try {
      await api.post('/requests', {
        equipment_id: parseInt(id),
        start_date: formData.start_date,
        end_date: formData.end_date,
      });
      setSuccess('Request submitted successfully!');
      setFormData({ start_date: '', end_date: '' });
      setTimeout(() => {
        navigate('/requests');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to submit request');
    } finally {
      setRequesting(false);
    }
  };

  const getConditionColor = (condition) => {
    const colors = {
      excellent: 'success',
      good: 'info',
      fair: 'warning',
      poor: 'error',
    };
    return colors[condition] || 'default';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (!equipment) {
    return (
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6">Equipment not found</Typography>
        <Button onClick={() => navigate('/equipment')} sx={{ mt: 2 }}>
          Back to Equipment List
        </Button>
      </Paper>
    );
  }

  return (
    <Box>
      <Button onClick={() => navigate('/equipment')} sx={{ mb: 2 }}>
        ← Back to Equipment List
      </Button>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          {equipment.name}
        </Typography>
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body1" color="textSecondary">
              Category: {equipment.category}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Chip
              label={equipment.condition}
              color={getConditionColor(equipment.condition)}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body1">
              Available: {equipment.available} / {equipment.quantity}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1" paragraph>
              {equipment.description || 'No description available'}
            </Typography>
          </Grid>
        </Grid>

        {equipment.available > 0 && (
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Request Equipment
            </Typography>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            {success && (
              <Alert severity="success" sx={{ mb: 2 }}>
                {success}
              </Alert>
            )}
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <TextField
                label="Start Date"
                type="date"
                required
                value={formData.start_date}
                onChange={(e) =>
                  setFormData({ ...formData, start_date: e.target.value })
                }
                InputLabelProps={{ shrink: true }}
                inputProps={{ min: new Date().toISOString().split('T')[0] }}
              />
              <TextField
                label="End Date"
                type="date"
                required
                value={formData.end_date}
                onChange={(e) =>
                  setFormData({ ...formData, end_date: e.target.value })
                }
                InputLabelProps={{ shrink: true }}
                inputProps={{ min: formData.start_date || new Date().toISOString().split('T')[0] }}
              />
            </Box>
            <Button
              type="submit"
              variant="contained"
              disabled={requesting || equipment.available === 0}
            >
              {requesting ? 'Submitting...' : 'Submit Request'}
            </Button>
          </Box>
        )}

        {equipment.available === 0 && (
          <Alert severity="warning" sx={{ mt: 2 }}>
            This equipment is currently not available.
          </Alert>
        )}
      </Paper>
    </Box>
  );
};

export default EquipmentDetail;

