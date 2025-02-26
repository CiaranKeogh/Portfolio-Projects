import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Grid,
  Button,
  Card,
  CardContent,
  Divider,
  CircularProgress,
  Tabs,
  Tab,
  Chip,
} from '@mui/material';
import {
  Route as RouteIcon,
  Place as PlaceIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

// Helper function to safely get map image URL with fallback
const getMapImageUrl = (mapName, layout = 'Domination') => {
  try {
    return `/assets/maps/${mapName}/MapLayout_${layout}_${mapName}_ABRBSB.jpg`;
  } catch (error) {
    console.error(`Error getting map image for ${mapName}:`, error);
    return '/assets/maps/default_map.jpg';
  }
};

// Sample map data for demonstration purposes
const sampleMaps = [
  {
    _id: '1',
    name: 'Advance to the Rhine',
    description: 'Urban combat with varied engagement distances from close quarters to mid-range city fighting.',
    imageUrl: '/assets/maps/Advance to the Rhine/MapLayout_Domination_Advance to the Rhine_ABRBSB.jpg',
    thumbnailUrl: '/assets/maps/Advance to the Rhine/MapLayout_Conquest1_Advance to the Rhine_ABRBSB.jpg',
    gameModes: ['Domination', 'Conquest', 'Battle'],
    dimensions: { width: 2048, height: 2048 },
    objectives: [
      {
        type: 'capture',
        name: 'A',
        position: { x: 512, y: 512 },
        gameMode: 'Domination'
      },
      {
        type: 'capture',
        name: 'B',
        position: { x: 1024, y: 1024 },
        gameMode: 'Domination'
      },
      {
        type: 'capture',
        name: 'C',
        position: { x: 1536, y: 512 },
        gameMode: 'Domination'
      }
    ],
    routes: [
      {
        _id: '1',
        title: 'North Ridge Flanking Route',
        vehicleType: 'Light Tank',
        upvotes: 42
      },
      {
        _id: '2',
        title: 'Central Push Strategy',
        vehicleType: 'Medium Tank',
        upvotes: 28
      }
    ],
    positions: [
      {
        _id: '1',
        title: 'Market Square Sniper Position',
        type: 'Sniping Spot',
        upvotes: 35
      },
      {
        _id: '2',
        title: 'Eastern Ruins Cover',
        type: 'Cover Position',
        upvotes: 23
      }
    ],
    versionHistory: [
      {
        version: '1.0',
        changes: 'Initial release',
        releaseDate: '2023-01-15T00:00:00Z'
      }
    ]
  },
  {
    _id: '2',
    name: 'Berlin',
    description: 'Dense urban warfare with destroyed buildings providing numerous sniping positions.',
    imageUrl: '/assets/maps/Berlin/MapLayout_Domination_Berlin_ABRBSB.jpg',
    thumbnailUrl: '/assets/maps/Berlin/MapLayout_Conquest1_Berlin_ABRBSB.jpg',
    gameModes: ['Domination', 'Conquest'],
    dimensions: { width: 2048, height: 2048 },
    objectives: [
      {
        type: 'capture',
        name: 'A',
        position: { x: 500, y: 500 },
        gameMode: 'Domination'
      },
      {
        type: 'capture',
        name: 'B',
        position: { x: 1000, y: 1000 },
        gameMode: 'Domination'
      },
      {
        type: 'capture',
        name: 'C',
        position: { x: 1500, y: 500 },
        gameMode: 'Domination'
      }
    ],
    routes: [
      {
        _id: '3',
        title: 'Eastern Flank Route',
        vehicleType: 'Medium Tank',
        upvotes: 36
      },
      {
        _id: '4',
        title: 'City Center Push',
        vehicleType: 'Heavy Tank',
        upvotes: 42
      }
    ],
    positions: [
      {
        _id: '3',
        title: 'Cathedral Sniping Position',
        type: 'Sniping Spot',
        upvotes: 31
      },
      {
        _id: '4',
        title: 'Reichstag Cover',
        type: 'Cover Position',
        upvotes: 27
      }
    ],
    versionHistory: [
      {
        version: '1.0',
        changes: 'Initial release',
        releaseDate: '2023-02-10T00:00:00Z'
      }
    ]
  },
  {
    _id: '4',
    name: 'Finland',
    description: 'Winter map with forests, hills and small villages providing diverse combat scenarios.',
    imageUrl: '/assets/maps/Finland/MapLayout_Domination_Finland_ABRBSB.jpg',
    thumbnailUrl: '/assets/maps/Finland/MapLayout_Conquest1_Finland_ABRBSB.jpg',
    gameModes: ['Domination', 'Conquest', 'Battle'],
    dimensions: { width: 2048, height: 2048 },
    objectives: [
      {
        type: 'capture',
        name: 'A',
        position: { x: 400, y: 400 },
        gameMode: 'Domination'
      },
      {
        type: 'capture',
        name: 'B',
        position: { x: 1000, y: 1000 },
        gameMode: 'Domination'
      },
      {
        type: 'capture',
        name: 'C',
        position: { x: 1600, y: 400 },
        gameMode: 'Domination'
      }
    ],
    routes: [
      {
        _id: '5',
        title: 'Forest Flanking Route',
        vehicleType: 'Light Tank',
        upvotes: 28
      },
      {
        _id: '6',
        title: 'Village Defense Strategy',
        vehicleType: 'Tank Destroyer',
        upvotes: 23
      }
    ],
    positions: [
      {
        _id: '5',
        title: 'Hill Overlook Position',
        type: 'Sniping Spot',
        upvotes: 25
      },
      {
        _id: '6',
        title: 'Village Center Ambush',
        type: 'Ambush Point',
        upvotes: 19
      }
    ],
    versionHistory: [
      {
        version: '1.0',
        changes: 'Initial release',
        releaseDate: '2023-03-05T00:00:00Z'
      }
    ]
  }
];

const MapDetail = () => {
  const { id } = useParams();
  const [map, setMap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    const fetchMapData = async () => {
      try {
        setLoading(true);
        
        // Simulate API call with setTimeout
        setTimeout(() => {
          // Find the correct map data based on the ID parameter
          const mapData = sampleMaps.find(m => m._id === id);
          
          if (mapData) {
            setMap(mapData);
          } else {
            setError('Map not found');
          }
          
          setLoading(false);
        }, 1000);
      } catch (err) {
        console.error('Error fetching map:', err);
        setError('Failed to load map data. Please try again later.');
        setLoading(false);
      }
    };

    fetchMapData();
  }, [id]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 8, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="body1" sx={{ mt: 2 }}>
          Loading map data...
        </Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h6" color="error" gutterBottom>
          {error}
        </Typography>
        <Button variant="contained" component={Link} to="/maps">
          Return to Maps
        </Button>
      </Container>
    );
  }

  if (!map) {
    return (
      <Container maxWidth="lg" sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Map not found
        </Typography>
        <Button variant="contained" component={Link} to="/maps">
          Return to Maps
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Map header */}
      <Typography variant="h4" component="h1" gutterBottom>
        {map.name}
      </Typography>
      
      <Grid container spacing={4}>
        {/* Map image */}
        <Grid item xs={12} md={8}>
          <Box
            component="img"
            src={map.imageUrl || getMapImageUrl(map.name)}
            alt={map.name}
            sx={{
              width: '100%',
              height: 'auto',
              borderRadius: 2,
              boxShadow: 3,
            }}
          />
        </Grid>
        
        {/* Map details */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Map Details
              </Typography>
              <Typography variant="body2" paragraph>
                {map.description}
              </Typography>
              
              <Typography variant="subtitle2" gutterBottom>
                Game Modes:
              </Typography>
              <Box sx={{ mb: 2 }}>
                {map.gameModes.map((mode) => (
                  <Chip
                    key={mode}
                    label={mode}
                    size="small"
                    color="primary"
                    sx={{ mr: 0.5, mb: 0.5 }}
                  />
                ))}
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Button
                  variant="outlined"
                  startIcon={<RouteIcon />}
                  component={Link}
                  to={`/routes/create?mapId=${map._id}`}
                >
                  Add Route
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<PlaceIcon />}
                  component={Link}
                  to={`/positions/create?mapId=${map._id}`}
                >
                  Add Position
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Tabs for routes, positions, and info */}
      <Box sx={{ width: '100%', mt: 4 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="map content tabs">
            <Tab label="Tactical Routes" icon={<RouteIcon />} iconPosition="start" />
            <Tab label="Power Positions" icon={<PlaceIcon />} iconPosition="start" />
            <Tab label="Map Information" icon={<InfoIcon />} iconPosition="start" />
          </Tabs>
        </Box>
        
        {/* Routes tab */}
        <div role="tabpanel" hidden={tabValue !== 0}>
          {tabValue === 0 && (
            <Box sx={{ py: 3 }}>
              <Typography variant="h6" gutterBottom>
                Tactical Routes for {map.name}
              </Typography>
              
              {map.routes && map.routes.length > 0 ? (
                <Grid container spacing={3}>
                  {map.routes.map((route) => (
                    <Grid item xs={12} md={6} key={route._id}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6">{route.title}</Typography>
                          <Typography variant="body2" color="textSecondary">
                            Vehicle Type: {route.vehicleType}
                          </Typography>
                          <Typography variant="body2">
                            👍 {route.upvotes}
                          </Typography>
                          <Button
                            variant="text"
                            component={Link}
                            to={`/routes/${route._id}`}
                            sx={{ mt: 1 }}
                          >
                            View Route
                          </Button>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              ) : (
                <Typography variant="body1" align="center" sx={{ py: 4 }}>
                  No routes have been created for this map yet.
                  <Button
                    variant="contained"
                    component={Link}
                    to={`/routes/create?mapId=${map._id}`}
                    sx={{ display: 'block', mx: 'auto', mt: 2 }}
                  >
                    Create the First Route
                  </Button>
                </Typography>
              )}
            </Box>
          )}
        </div>
        
        {/* Positions tab */}
        <div role="tabpanel" hidden={tabValue !== 1}>
          {tabValue === 1 && (
            <Box sx={{ py: 3 }}>
              <Typography variant="h6" gutterBottom>
                Power Positions for {map.name}
              </Typography>
              
              {map.positions && map.positions.length > 0 ? (
                <Grid container spacing={3}>
                  {map.positions.map((position) => (
                    <Grid item xs={12} md={6} key={position._id}>
                      <Card>
                        <CardContent>
                          <Typography variant="h6">{position.title}</Typography>
                          <Typography variant="body2" color="textSecondary">
                            Type: {position.type}
                          </Typography>
                          <Typography variant="body2">
                            👍 {position.upvotes}
                          </Typography>
                          <Button
                            variant="text"
                            component={Link}
                            to={`/positions/${position._id}`}
                            sx={{ mt: 1 }}
                          >
                            View Position
                          </Button>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              ) : (
                <Typography variant="body1" align="center" sx={{ py: 4 }}>
                  No power positions have been marked for this map yet.
                  <Button
                    variant="contained"
                    component={Link}
                    to={`/positions/create?mapId=${map._id}`}
                    sx={{ display: 'block', mx: 'auto', mt: 2 }}
                  >
                    Mark the First Position
                  </Button>
                </Typography>
              )}
            </Box>
          )}
        </div>
        
        {/* Info tab */}
        <div role="tabpanel" hidden={tabValue !== 2}>
          {tabValue === 2 && (
            <Box sx={{ py: 3 }}>
              <Typography variant="h6" gutterBottom>
                Map Information
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle1">Capture Points</Typography>
                      <Divider sx={{ my: 1 }} />
                      {map.objectives
                        .filter((obj) => obj.type === 'capture')
                        .map((point, index) => (
                          <Box key={index} sx={{ mb: 1 }}>
                            <Typography variant="body2">
                              <strong>Point {point.name}</strong> - Game Mode: {point.gameMode}
                            </Typography>
                          </Box>
                        ))}
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle1">Version History</Typography>
                      <Divider sx={{ my: 1 }} />
                      {map.versionHistory.map((version, index) => (
                        <Box key={index} sx={{ mb: 2 }}>
                          <Typography variant="body2">
                            <strong>Version {version.version}</strong> - {new Date(version.releaseDate).toLocaleDateString()}
                          </Typography>
                          <Typography variant="body2" color="textSecondary">
                            {version.changes}
                          </Typography>
                        </Box>
                      ))}
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}
        </div>
      </Box>
    </Container>
  );
};

export default MapDetail; 