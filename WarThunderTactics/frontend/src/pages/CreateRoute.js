import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Paper,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
  Grid,
  CircularProgress,
  Alert,
  Stepper,
  Step,
  StepLabel,
  Slider,
} from '@mui/material';
import {
  Save as SaveIcon,
  ArrowBack as ArrowBackIcon,
  ArrowForward as ArrowForwardIcon,
} from '@mui/icons-material';
import { createRoute } from '../services/routeService';
import { getMaps } from '../services/mapService';

const vehicleTypes = [
  'Light Tank',
  'Medium Tank',
  'Heavy Tank',
  'Tank Destroyer',
  'SPAA',
  'Any',
];

const gameModes = [
  'Domination',
  'Conquest',
  'Battle',
  'Break',
];

const CreateRoute = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [maps, setMaps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [routeData, setRouteData] = useState({
    title: '',
    description: '',
    mapId: '',
    gameMode: '',
    vehicleType: '',
    effectiveness: 3,
    coordinates: [],
  });
  const [formErrors, setFormErrors] = useState({});
  
  // Fetch available maps
  useEffect(() => {
    const fetchMaps = async () => {
      try {
        setLoading(true);
        const data = await getMaps();
        setMaps(data || []);
      } catch (err) {
        console.error('Error fetching maps:', err);
        setError('Failed to load maps. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchMaps();
  }, []);
  
  const validateStep = (step) => {
    const errors = {};
    
    switch (step) {
      case 0: // Basic Info
        if (!routeData.title.trim()) {
          errors.title = 'Title is required';
        }
        if (!routeData.description.trim()) {
          errors.description = 'Description is required';
        }
        if (!routeData.mapId) {
          errors.mapId = 'Map selection is required';
        }
        break;
        
      case 1: // Details
        if (!routeData.gameMode) {
          errors.gameMode = 'Game mode is required';
        }
        if (!routeData.vehicleType) {
          errors.vehicleType = 'Vehicle type is required';
        }
        break;
        
      case 2: // Route Drawing
        if (routeData.coordinates.length < 2) {
          errors.coordinates = 'Route must have at least 2 points';
        }
        break;
        
      default:
        break;
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };
  
  const handleNext = () => {
    if (validateStep(activeStep)) {
      setActiveStep((prevActiveStep) => prevActiveStep + 1);
    }
  };
  
  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setRouteData({
      ...routeData,
      [name]: value,
    });
    
    // Clear error for this field
    if (formErrors[name]) {
      setFormErrors({
        ...formErrors,
        [name]: '',
      });
    }
  };
  
  const handleEffectivenessChange = (event, newValue) => {
    setRouteData({
      ...routeData,
      effectiveness: newValue,
    });
  };
  
  const handleSubmit = async () => {
    // Validate all steps before submission
    for (let i = 0; i <= 2; i++) {
      if (!validateStep(i)) {
        setActiveStep(i);
        return;
      }
    }
    
    try {
      setSubmitting(true);
      setError('');
      
      // Add creator info (would come from auth context in a real app)
      const routeToSubmit = {
        ...routeData,
        creator: { _id: 'user1', username: 'CurrentUser' },
      };
      
      const newRoute = await createRoute(routeToSubmit);
      navigate(`/routes/${newRoute._id}`);
    } catch (err) {
      console.error('Error creating route:', err);
      setError('Failed to create route. Please try again later.');
    } finally {
      setSubmitting(false);
    }
  };
  
  // Mock function for route drawing - in a real app this would use a map library
  const addWaypoint = () => {
    // This is a simplified example - in a real app, this would come from clicking on a map
    const newCoordinates = [...routeData.coordinates];
    newCoordinates.push({
      x: Math.floor(Math.random() * 200) + 50,
      y: Math.floor(Math.random() * 200) + 50,
      order: newCoordinates.length,
      timestamp: 'Mid-game',
      notes: '',
    });
    
    setRouteData({
      ...routeData,
      coordinates: newCoordinates,
    });
    
    // Clear coordinate error if it exists
    if (formErrors.coordinates) {
      setFormErrors({
        ...formErrors,
        coordinates: '',
      });
    }
  };
  
  const getStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Basic Information
            </Typography>
            <TextField
              margin="normal"
              required
              fullWidth
              id="title"
              label="Route Title"
              name="title"
              value={routeData.title}
              onChange={handleChange}
              error={!!formErrors.title}
              helperText={formErrors.title}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="description"
              label="Route Description"
              name="description"
              multiline
              rows={4}
              value={routeData.description}
              onChange={handleChange}
              error={!!formErrors.description}
              helperText={formErrors.description}
            />
            <FormControl fullWidth margin="normal" error={!!formErrors.mapId}>
              <InputLabel id="map-select-label">Map</InputLabel>
              <Select
                labelId="map-select-label"
                id="mapId"
                name="mapId"
                value={routeData.mapId}
                onChange={handleChange}
                label="Map"
              >
                {maps.map(map => (
                  <MenuItem key={map._id} value={map._id}>
                    {map.name}
                  </MenuItem>
                ))}
              </Select>
              {formErrors.mapId && <FormHelperText>{formErrors.mapId}</FormHelperText>}
            </FormControl>
          </Box>
        );
        
      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Route Details
            </Typography>
            <FormControl fullWidth margin="normal" error={!!formErrors.gameMode}>
              <InputLabel id="gamemode-select-label">Game Mode</InputLabel>
              <Select
                labelId="gamemode-select-label"
                id="gameMode"
                name="gameMode"
                value={routeData.gameMode}
                onChange={handleChange}
                label="Game Mode"
              >
                {gameModes.map(mode => (
                  <MenuItem key={mode} value={mode}>
                    {mode}
                  </MenuItem>
                ))}
              </Select>
              {formErrors.gameMode && <FormHelperText>{formErrors.gameMode}</FormHelperText>}
            </FormControl>
            
            <FormControl fullWidth margin="normal" error={!!formErrors.vehicleType}>
              <InputLabel id="vehicletype-select-label">Vehicle Type</InputLabel>
              <Select
                labelId="vehicletype-select-label"
                id="vehicleType"
                name="vehicleType"
                value={routeData.vehicleType}
                onChange={handleChange}
                label="Vehicle Type"
              >
                {vehicleTypes.map(type => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </Select>
              {formErrors.vehicleType && <FormHelperText>{formErrors.vehicleType}</FormHelperText>}
            </FormControl>
            
            <Box sx={{ mt: 4 }}>
              <Typography id="effectiveness-slider" gutterBottom>
                Effectiveness Rating
              </Typography>
              <Slider
                value={routeData.effectiveness}
                onChange={handleEffectivenessChange}
                aria-labelledby="effectiveness-slider"
                valueLabelDisplay="auto"
                step={0.5}
                marks
                min={1}
                max={5}
              />
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                {routeData.effectiveness < 2
                  ? 'Not very effective'
                  : routeData.effectiveness < 3
                  ? 'Somewhat effective'
                  : routeData.effectiveness < 4
                  ? 'Moderately effective'
                  : routeData.effectiveness < 5
                  ? 'Very effective'
                  : 'Extremely effective'}
              </Typography>
            </Box>
          </Box>
        );
        
      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Draw Route
            </Typography>
            
            {/* Map would be here in a real app */}
            <Box 
              sx={{ 
                height: 400, 
                bgcolor: 'grey.100', 
                borderRadius: 1, 
                mb: 3, 
                display: 'flex', 
                flexDirection: 'column',
                justifyContent: 'center', 
                alignItems: 'center' 
              }}
            >
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Map interface would be displayed here
              </Typography>
              <Button variant="contained" onClick={addWaypoint}>
                Add Waypoint (Simulated)
              </Button>
            </Box>
            
            {formErrors.coordinates && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {formErrors.coordinates}
              </Alert>
            )}
            
            <Typography variant="subtitle1" gutterBottom>
              Waypoints: {routeData.coordinates.length}
            </Typography>
            
            <Grid container spacing={2}>
              {routeData.coordinates.map((coord, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="subtitle2">
                      Waypoint {index + 1}
                    </Typography>
                    <Typography variant="body2">
                      Position: ({coord.x}, {coord.y})
                    </Typography>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Box>
        );
        
      default:
        return 'Unknown step';
    }
  };
  
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="70vh">
        <CircularProgress />
      </Box>
    );
  }
  
  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 8 }}>
      <Paper sx={{ p: { xs: 2, md: 4 } }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Create Tactical Route
        </Typography>
        
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}
        
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          <Step>
            <StepLabel>Basic Info</StepLabel>
          </Step>
          <Step>
            <StepLabel>Details</StepLabel>
          </Step>
          <Step>
            <StepLabel>Draw Route</StepLabel>
          </Step>
        </Stepper>
        
        {getStepContent(activeStep)}
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            color="inherit"
            disabled={activeStep === 0}
            onClick={handleBack}
            startIcon={<ArrowBackIcon />}
          >
            Back
          </Button>
          
          <Box>
            <Button
              color="inherit"
              onClick={() => navigate('/routes')}
              sx={{ mr: 1 }}
            >
              Cancel
            </Button>
            
            {activeStep === 2 ? (
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmit}
                disabled={submitting}
                startIcon={submitting ? <CircularProgress size={24} /> : <SaveIcon />}
              >
                {submitting ? 'Saving...' : 'Save Route'}
              </Button>
            ) : (
              <Button
                variant="contained"
                color="primary"
                onClick={handleNext}
                endIcon={<ArrowForwardIcon />}
              >
                Next
              </Button>
            )}
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default CreateRoute; 