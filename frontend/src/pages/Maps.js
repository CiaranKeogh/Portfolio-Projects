import React, { useState, useEffect } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  Typography,
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
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
import SearchIcon from '@mui/icons-material/Search';

// Helper function to safely get map image URL with fallback
const getMapImageUrl = (mapName, layout = 'Domination') => {
  try {
    return `/assets/maps/${mapName}/MapLayout_${layout}_${mapName}_ABRBSB.jpg`;
  } catch (error) {
    console.error(`Error getting map image for ${mapName}:`, error);
    return '/assets/maps/default_map.jpg';
  }
};

const Maps = () => {
  const [maps, setMaps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [gameMode, setGameMode] = useState('all');
  
  // Sample map data (in a real app, this would come from an API)
  const sampleMaps = [
    {
      _id: '1',
      name: 'Advance to the Rhine',
      description: 'Urban combat with varied engagement distances from close quarters to mid-range city fighting.',
      imageUrl: '/assets/maps/Advance to the Rhine/MapLayout_Domination_Advance to the Rhine_ABRBSB.jpg',
      gameModes: ['Ground Arcade', 'Ground Realistic', 'Ground Simulator'],
      size: 'Medium',
      routes: 12,
      positions: 8,
    },
    {
      _id: '2',
      name: 'Berlin',
      description: 'Dense urban warfare with destroyed buildings providing numerous sniping positions.',
      imageUrl: '/assets/maps/Berlin/MapLayout_Domination_Berlin_ABRBSB.jpg',
      gameModes: ['Ground Arcade', 'Ground Realistic'],
      size: 'Large',
      routes: 18,
      positions: 15,
    },
    {
      _id: '3',
      name: 'Karelia',
      description: 'Forest and rock formations with narrow chokepoints and some open areas.',
      imageUrl: '/assets/maps/Karelia/MapLayout_Domination_Karelia_ABRBSB.jpg',
      gameModes: ['Ground Arcade', 'Ground Realistic', 'Ground Simulator'],
      size: 'Small',
      routes: 7,
      positions: 9,
    },
    {
      _id: '4',
      name: 'Finland',
      description: 'Winter map with forests, hills and small villages providing diverse combat scenarios.',
      imageUrl: '/assets/maps/Finland/MapLayout_Domination_Finland_ABRBSB.jpg',
      gameModes: ['Ground Arcade', 'Ground Realistic'],
      size: 'Medium',
      routes: 5,
      positions: 6,
    },
    {
      _id: '5',
      name: 'Sinai',
      description: 'Desert combat with open sightlines and some rocky formations for cover.',
      imageUrl: '/assets/maps/Sinai/MapLayout_Domination_Sinai_ABRBSB.jpg',
      gameModes: ['Ground Arcade', 'Ground Realistic', 'Ground Simulator'],
      size: 'Large',
      routes: 9,
      positions: 11,
    },
    {
      _id: '6',
      name: 'Normandy',
      description: 'Countryside with hills, hedgerows, and a small town, offering various tactical options.',
      imageUrl: '/assets/maps/Fields of Normandy/MapLayout_Domination_Fields of Normandy_ABRBSB.jpg',
      gameModes: ['Ground Arcade', 'Ground Realistic'],
      size: 'Medium',
      routes: 14,
      positions: 10,
    },
  ];
  
  useEffect(() => {
    // Simulate API fetch with setTimeout
    const fetchMaps = async () => {
      try {
        setLoading(true);
        
        // In a real app, this would be an API call
        setTimeout(() => {
          setMaps(sampleMaps);
          setLoading(false);
        }, 1000);
      } catch (error) {
        setError('Failed to fetch maps. Please try again later.');
        setLoading(false);
      }
    };
    
    fetchMaps();
  }, []);
  
  // Filter maps based on search term and selected game mode
  const filteredMaps = maps.filter((map) => {
    const matchesSearch = map.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         map.description.toLowerCase().includes(searchTerm.toLowerCase());
                         
    const matchesGameMode = gameMode === 'all' || map.gameModes.includes(gameMode);
    
    return matchesSearch && matchesGameMode;
  });
  
  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };
  
  const handleGameModeChange = (event) => {
    setGameMode(event.target.value);
  };
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        War Thunder Maps
      </Typography>
      
      <Typography variant="subtitle1" color="textSecondary" paragraph align="center" sx={{ mb: 4 }}>
        Browse all available maps and discover tactical routes and power positions
      </Typography>
      
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={8}>
            <TextField
              fullWidth
              variant="outlined"
              label="Search Maps"
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
              <InputLabel id="game-mode-label">Game Mode</InputLabel>
              <Select
                labelId="game-mode-label"
                id="game-mode-select"
                value={gameMode}
                onChange={handleGameModeChange}
                label="Game Mode"
              >
                <MenuItem value="all">All Game Modes</MenuItem>
                <MenuItem value="Ground Arcade">Ground Arcade</MenuItem>
                <MenuItem value="Ground Realistic">Ground Realistic</MenuItem>
                <MenuItem value="Ground Simulator">Ground Simulator</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Box>
      
      <Divider sx={{ mb: 4 }} />
      
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 8 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error" align="center" sx={{ my: 8 }}>
          {error}
        </Typography>
      ) : filteredMaps.length === 0 ? (
        <Typography align="center" sx={{ my: 8 }}>
          No maps match your search criteria. Try adjusting your filters.
        </Typography>
      ) : (
        <Grid container spacing={4}>
          {filteredMaps.map((map) => (
            <Grid item key={map._id} xs={12} sm={6} md={4}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardActionArea component={RouterLink} to={`/maps/${map._id}`}>
                  <CardMedia
                    component="img"
                    height="200"
                    image={map.imageUrl || getMapImageUrl(map.name)}
                    alt={map.name}
                    sx={{ objectFit: 'cover' }}
                  />
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography gutterBottom variant="h5" component="h2">
                      {map.name}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" paragraph>
                      {map.description}
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                      {map.gameModes.map((mode) => (
                        <Chip key={mode} label={mode} size="small" />
                      ))}
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">
                        Size: {map.size}
                      </Typography>
                      <Typography variant="body2">
                        {map.routes} Routes • {map.positions} Positions
                      </Typography>
                    </Box>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default Maps; 