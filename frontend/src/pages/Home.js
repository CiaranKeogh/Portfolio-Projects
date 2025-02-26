import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Container,
  Grid,
  Typography,
  Divider,
  CircularProgress,
} from '@mui/material';
import { Map as MapIcon, Route as RouteIcon, Place as PlaceIcon } from '@mui/icons-material';
import { getRecentRoutes } from '../services/routeService';
import { getRecentPositions } from '../services/positionService';

// Helper function to safely get map image URL with fallback
const getMapImageUrl = (mapName, layout = 'Domination') => {
  try {
    return `/assets/maps/${mapName}/MapLayout_${layout}_${mapName}_ABRBSB.jpg`;
  } catch (error) {
    console.error(`Error getting map image for ${mapName}:`, error);
    return '/assets/maps/default_map.jpg';
  }
};

const Home = () => {
  const navigate = useNavigate();
  const [recentRoutes, setRecentRoutes] = useState([]);
  const [recentPositions, setRecentPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchRecentData = async () => {
      try {
        const [routesData, positionsData] = await Promise.all([
          getRecentRoutes(),
          getRecentPositions(),
        ]);
        
        setRecentRoutes(routesData.data.slice(0, 3));
        setRecentPositions(positionsData.data.slice(0, 3));
      } catch (error) {
        console.error('Error fetching recent data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchRecentData();
  }, []);
  
  const heroSection = (
    <Box
      sx={{
        bgcolor: 'primary.main',
        color: 'white',
        py: 8,
        mb: 6,
        borderRadius: 2,
        backgroundImage: 'url(/assets/hero-background.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.6)',
          borderRadius: 2,
        },
      }}
    >
      <Container maxWidth="lg">
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          <Typography
            variant="h2"
            component="h1"
            gutterBottom
            sx={{ fontWeight: 'bold' }}
          >
            War Thunder Tactics
          </Typography>
          <Typography variant="h5" paragraph>
            Share and discover the best tactical routes and power positions for War Thunder ground battles.
          </Typography>
          <Box sx={{ mt: 4 }}>
            <Button
              variant="contained"
              color="secondary"
              size="large"
              onClick={() => navigate('/maps')}
              startIcon={<MapIcon />}
              sx={{ mr: 2, mb: 2 }}
            >
              Browse Maps
            </Button>
            <Button
              variant="outlined"
              color="inherit"
              size="large"
              onClick={() => navigate('/register')}
              sx={{ mb: 2 }}
            >
              Join Community
            </Button>
          </Box>
        </Box>
      </Container>
    </Box>
  );
  
  const featureSection = (
    <Box sx={{ py: 6 }}>
      <Container maxWidth="lg">
        <Typography variant="h4" component="h2" align="center" gutterBottom>
          Features
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          <Grid item xs={12} md={4}>
            <Card elevation={2} sx={{ height: '100%' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <MapIcon color="primary" sx={{ fontSize: 60, mb: 2 }} />
                <Typography variant="h5" component="h3" gutterBottom>
                  Interactive Maps
                </Typography>
                <Typography variant="body1">
                  High-resolution maps of all War Thunder ground battle locations with the ability to zoom, pan, and filter by game mode.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card elevation={2} sx={{ height: '100%' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <RouteIcon color="primary" sx={{ fontSize: 60, mb: 2 }} />
                <Typography variant="h5" component="h3" gutterBottom>
                  Route Creation
                </Typography>
                <Typography variant="body1">
                  Draw and share optimal vehicle routes on maps with color-coding for different vehicle types and detailed waypoints.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card elevation={2} sx={{ height: '100%' }}>
              <CardContent sx={{ textAlign: 'center' }}>
                <PlaceIcon color="primary" sx={{ fontSize: 60, mb: 2 }} />
                <Typography variant="h5" component="h3" gutterBottom>
                  Power Positions
                </Typography>
                <Typography variant="body1">
                  Mark and discover strategic positions with effectiveness ratings for different vehicle classes and line-of-sight visualization.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
  
  const recentContentSection = (
    <Box sx={{ py: 6, bgcolor: 'grey.100' }}>
      <Container maxWidth="lg">
        <Typography variant="h4" component="h2" align="center" gutterBottom>
          Recent Contributions
        </Typography>
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <Typography variant="h5" component="h3" sx={{ mt: 4, mb: 2 }}>
              Latest Routes
            </Typography>
            <Grid container spacing={3}>
              {recentRoutes.length > 0 ? (
                recentRoutes.map((route) => (
                  <Grid item xs={12} sm={6} md={4} key={route._id}>
                    <Card>
                      <CardActionArea onClick={() => navigate(`/routes/${route._id}`)}>
                        <CardMedia
                          component="img"
                          height="140"
                          image={getMapImageUrl(route.map.name)}
                          alt={route.title}
                        />
                        <CardContent>
                          <Typography variant="h6" component="div" noWrap>
                            {route.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            {route.map.name} - {route.vehicleType}
                          </Typography>
                          <Typography variant="body2" noWrap>
                            {route.description}
                          </Typography>
                        </CardContent>
                      </CardActionArea>
                    </Card>
                  </Grid>
                ))
              ) : (
                <Grid item xs={12}>
                  <Typography variant="body1" align="center">
                    No routes available yet. Be the first to contribute!
                  </Typography>
                </Grid>
              )}
            </Grid>
            
            <Divider sx={{ my: 4 }} />
            
            <Typography variant="h5" component="h3" sx={{ mb: 2 }}>
              Latest Power Positions
            </Typography>
            <Grid container spacing={3}>
              {recentPositions.length > 0 ? (
                recentPositions.map((position) => (
                  <Grid item xs={12} sm={6} md={4} key={position._id}>
                    <Card>
                      <CardActionArea onClick={() => navigate(`/positions/${position._id}`)}>
                        <CardMedia
                          component="img"
                          height="140"
                          image={getMapImageUrl(position.map.name)}
                          alt={position.title}
                        />
                        <CardContent>
                          <Typography variant="h6" component="div" noWrap>
                            {position.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            {position.map.name} - {position.type}
                          </Typography>
                          <Typography variant="body2" noWrap>
                            {position.description}
                          </Typography>
                        </CardContent>
                      </CardActionArea>
                    </Card>
                  </Grid>
                ))
              ) : (
                <Grid item xs={12}>
                  <Typography variant="body1" align="center">
                    No power positions available yet. Be the first to contribute!
                  </Typography>
                </Grid>
              )}
            </Grid>
            
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate('/maps')}
                size="large"
              >
                Explore All Maps
              </Button>
            </Box>
          </>
        )}
      </Container>
    </Box>
  );
  
  return (
    <>
      {heroSection}
      {featureSection}
      {recentContentSection}
    </>
  );
};

export default Home; 