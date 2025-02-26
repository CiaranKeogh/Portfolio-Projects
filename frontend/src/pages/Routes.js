import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardActionArea,
  TextField,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Divider,
  Chip,
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { getRoutes, getTopRatedRoutes, searchRoutes } from '../services/routeService';

const Routes = () => {
  const navigate = useNavigate();
  const [routes, setRoutes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [vehicleFilter, setVehicleFilter] = useState('All');
  
  useEffect(() => {
    const fetchRoutes = async () => {
      try {
        setLoading(true);
        // In a real app, this would make an API call
        // For now, we'll just simulate a response
        setRoutes([
          {
            _id: '1',
            title: 'North Ridge Flanking Route',
            description: 'Quick flanking route for light tanks on the eastern side of Advance to the Rhine.',
            creator: { username: 'TankCommander' },
            gameMode: 'Domination',
            vehicleType: 'Light Tank',
            map: { name: 'Advance to the Rhine' },
            upvotes: 42,
            downvotes: 5,
            createdAt: '2023-03-15T12:00:00Z',
          },
          {
            _id: '2',
            title: 'Southern Sniping Approach',
            description: 'Excellent route for tank destroyers on Karelia that provides good overwatch.',
            creator: { username: 'SniperElite' },
            gameMode: 'Battle',
            vehicleType: 'Tank Destroyer',
            map: { name: 'Karelia' },
            upvotes: 38,
            downvotes: 7,
            createdAt: '2023-04-02T14:30:00Z',
          },
          {
            _id: '3',
            title: 'Middle Cap Rush',
            description: 'Fast route to the central capture point on Berlin for medium tanks.',
            creator: { username: 'SpeedDemon' },
            gameMode: 'Conquest',
            vehicleType: 'Medium Tank',
            map: { name: 'Berlin' },
            upvotes: 27,
            downvotes: 3,
            createdAt: '2023-04-10T09:15:00Z',
          },
        ]);
      } catch (err) {
        console.error('Error fetching routes:', err);
        setError('Failed to load routes. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchRoutes();
  }, []);
  
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };
  
  const handleVehicleFilterChange = (e) => {
    setVehicleFilter(e.target.value);
  };
  
  const handleRouteClick = (routeId) => {
    navigate(`/routes/${routeId}`);
  };
  
  const filteredRoutes = routes.filter(route => {
    const matchesSearch = searchTerm === '' || 
      route.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      route.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      route.map.name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesVehicle = vehicleFilter === 'All' || route.vehicleType === vehicleFilter;
    
    return matchesSearch && matchesVehicle;
  });
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Tactical Routes
      </Typography>
      <Typography variant="body1" color="textSecondary" paragraph>
        Browse community-created routes and tactical paths for War Thunder ground battles.
      </Typography>
      
      {/* Search and Filter */}
      <Box sx={{ mb: 4, mt: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={8}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Search routes by name, description or map"
              value={searchTerm}
              onChange={handleSearchChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth variant="outlined">
              <InputLabel id="vehicle-filter-label">Vehicle Type</InputLabel>
              <Select
                labelId="vehicle-filter-label"
                value={vehicleFilter}
                onChange={handleVehicleFilterChange}
                label="Vehicle Type"
              >
                <MenuItem value="All">All Vehicles</MenuItem>
                <MenuItem value="Light Tank">Light Tanks</MenuItem>
                <MenuItem value="Medium Tank">Medium Tanks</MenuItem>
                <MenuItem value="Heavy Tank">Heavy Tanks</MenuItem>
                <MenuItem value="Tank Destroyer">Tank Destroyers</MenuItem>
                <MenuItem value="SPAA">SPAA</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Box>
      
      <Divider sx={{ mb: 4 }} />
      
      {/* Error Message */}
      {error && (
        <Typography color="error" align="center" sx={{ my: 2 }}>
          {error}
        </Typography>
      )}
      
      {/* Routes List */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          {/* Results Count */}
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="textSecondary">
              Showing {filteredRoutes.length} {filteredRoutes.length === 1 ? 'route' : 'routes'}
            </Typography>
          </Box>
          
          {/* Routes Grid */}
          <Grid container spacing={3}>
            {filteredRoutes.length > 0 ? (
              filteredRoutes.map((route) => (
                <Grid item xs={12} key={route._id}>
                  <Card elevation={2}>
                    <CardActionArea onClick={() => handleRouteClick(route._id)}>
                      <CardContent>
                        <Typography variant="h6" component="div" gutterBottom>
                          {route.title}
                        </Typography>
                        <Grid container spacing={2}>
                          <Grid item xs={12} md={8}>
                            <Typography variant="body2" color="textSecondary" paragraph>
                              {route.description}
                            </Typography>
                            <Typography variant="caption" color="textSecondary">
                              Created by {route.creator.username} • Map: {route.map.name}
                            </Typography>
                          </Grid>
                          <Grid item xs={12} md={4}>
                            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
                              <Box sx={{ mb: 1 }}>
                                <Chip 
                                  label={route.gameMode} 
                                  size="small" 
                                  color="primary" 
                                  sx={{ mr: 1 }} 
                                />
                                <Chip 
                                  label={route.vehicleType} 
                                  size="small" 
                                  color="secondary" 
                                />
                              </Box>
                              <Typography variant="body2">
                                👍 {route.upvotes} • 👎 {route.downvotes}
                              </Typography>
                            </Box>
                          </Grid>
                        </Grid>
                      </CardContent>
                    </CardActionArea>
                  </Card>
                </Grid>
              ))
            ) : (
              <Grid item xs={12}>
                <Typography align="center" sx={{ py: 4 }}>
                  No routes found matching your search criteria.
                </Typography>
              </Grid>
            )}
          </Grid>
        </>
      )}
    </Container>
  );
};

export default Routes; 