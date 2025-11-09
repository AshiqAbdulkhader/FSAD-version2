import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  TextField,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Chip,
} from '@mui/material';
import api from '../services/api';

const EquipmentList = () => {
  const [equipment, setEquipment] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchEquipment();
    fetchCategories();
  }, [categoryFilter]);

  const fetchEquipment = async () => {
    try {
      const params = {};
      if (categoryFilter) params.category = categoryFilter;
      if (search) params.search = search;
      
      const response = await api.get('/equipment', { params });
      setEquipment(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching equipment:', error);
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get('/equipment/categories');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleSearch = (e) => {
    setSearch(e.target.value);
    if (e.target.value === '') {
      fetchEquipment();
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchEquipment();
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

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Equipment Catalog
      </Typography>
      <Box component="form" onSubmit={handleSearchSubmit} sx={{ mb: 3, display: 'flex', gap: 2 }}>
        <TextField
          fullWidth
          label="Search equipment"
          variant="outlined"
          value={search}
          onChange={handleSearch}
          placeholder="Search by name or description..."
        />
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Category</InputLabel>
          <Select
            value={categoryFilter}
            label="Category"
            onChange={(e) => setCategoryFilter(e.target.value)}
          >
            <MenuItem value="">All Categories</MenuItem>
            {categories.map((cat) => (
              <MenuItem key={cat} value={cat}>
                {cat}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Button type="submit" variant="contained" sx={{ minWidth: 100 }}>
          Search
        </Button>
      </Box>
      <Grid container spacing={3}>
        {equipment.map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {item.name}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  {item.category}
                </Typography>
                <Box sx={{ mt: 1, mb: 1 }}>
                  <Chip
                    label={item.condition}
                    color={getConditionColor(item.condition)}
                    size="small"
                  />
                </Box>
                <Typography variant="body2" color="textSecondary" paragraph>
                  {item.description || 'No description available'}
                </Typography>
                <Typography variant="body2">
                  Available: {item.available} / {item.quantity}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={() => navigate(`/equipment/${item.id}`)}
                >
                  View Details
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      {equipment.length === 0 && (
        <Typography variant="body1" align="center" sx={{ mt: 4 }}>
          No equipment found.
        </Typography>
      )}
    </Box>
  );
};

export default EquipmentList;

