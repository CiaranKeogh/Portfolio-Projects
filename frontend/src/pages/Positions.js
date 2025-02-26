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
import { getPositions, getTopRatedPositions, searchPositions } from '../services/positionService';

const Positions = () => {
  const navigate = useNavigate();
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState('All');
  
  useEffect(() => {
    const fetchPositions = async () => {
      try {
        setLoading(true);
        // In a real app, this would make an API call
        // For now, we'll just simulate a response
        setPositions([
          {
            _id: '1',
            title: 'Eastern Hill Sniper Spot',
            description: 'Excellent sniping position overlooking the B point on Karelia, perfect for tank destroyers.',
            creator: { username: 'SniperElite' },
            gameMode: 'Battle',
            type: 'Sniping Spot',
            map: { name: 'Karelia' },
            upvotes: 62,
            downvotes: 8,
            createdAt: '2023-03-10T12:00:00Z',
            effectiveness: {
              lightTank: 3,
              mediumTank: 6,
              heavyTank: 5,
              tankDestroyer: 9,
              spaa: 7
            }
          },
          {
            _id: '2',
            title: 'Central Market Ambush',
            description: 'Hidden spot behind destroyed buildings, perfect for ambushing enemies moving to A point.',
            creator: { username: 'TankAce' },
            gameMode: 'Domination',
            type: 'Ambush Point',
            map: { name: 'Advance to the Rhine' },
            upvotes: 45,
            downvotes: 10,
            createdAt: '2023-03-22T15:30:00Z',
            effectiveness: {
              lightTank: 7,
              mediumTank: 8,
              heavyTank: 6,
              tankDestroyer: 7,
              spaa: 4
            }
          },
          {
            _id: '3',
            title: 'North Ridge Cover',
            description: 'Perfect hull-down position for heavy tanks to hold the northern approach.',
            creator: { username: 'HeavyDefender' },
            gameMode: 'Conquest',
            type: 'Cover Position',
            map: { name: 'Finland' },
            upvotes: 38,
            downvotes: 5,
            createdAt: '2023-04-05T09:45:00Z',
            effectiveness: {
              lightTank: 4,
              mediumTank: 6,
              heavyTank: 9,
              tankDestroyer: 7,
              spaa: 3
            }
          },
        ]);
      } catch (err) {
        console.error('Error fetching positions:', err);
        setError('Failed to load positions. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchPositions();
  }, []);
  
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };
  
  const handleTypeFilterChange = (e) => {
    setTypeFilter(e.target.value);
  };
  
  const handlePositionClick = (positionId) => {
    navigate(`/positions/${positionId}`);
  };
  
  const filteredPositions = positions.filter(position => {
    const matchesSearch = searchTerm === '' || 
      position.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      position.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      position.map.name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesType = typeFilter === 'All' || position.type === typeFilter;
    
    return matchesSearch && matchesType;
  });
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Power Positions
      </Typography>
      <Typography variant="body1" color="textSecondary" paragraph>
        Browse strategic power positions marked by the community for War Thunder ground battles.
      </Typography>
      
      {/* Search and Filter */}
      <Box sx={{ mb: 4, mt: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={8}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Search positions by name, description or map"
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
              <InputLabel id="type-filter-label">Position Type</InputLabel>
              <Select
                labelId="type-filter-label"
                value={typeFilter}
                onChange={handleTypeFilterChange}
                label="Position Type"
              >
                <MenuItem value="All">All Types</MenuItem>
                <MenuItem value="Sniping Spot">Sniping Spots</MenuItem>
                <MenuItem value="Cover Position">Cover Positions</MenuItem>
                <MenuItem value="Ambush Point">Ambush Points</MenuItem>
                <MenuItem value="Capping Position">Capping Positions</MenuItem>
                <MenuItem value="Artillery Position">Artillery Positions</MenuItem>
                <MenuItem value="Other">Other Positions</MenuItem>
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
      
      {/* Positions List */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          {/* Results Count */}
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="textSecondary">
              Showing {filteredPositions.length} {filteredPositions.length === 1 ? 'position' : 'positions'}
            </Typography>
          </Box>
          
          {/* Positions Grid */}
          <Grid container spacing={3}>
            {filteredPositions.length > 0 ? (
              filteredPositions.map((position) => (
                <Grid item xs={12} sm={6} md={4} key={position._id}>
                  <Card elevation={2}>
                    <CardActionArea onClick={() => handlePositionClick(position._id)}>
                      <CardContent>
                        <Typography variant="h6" component="div" gutterBottom>
                          {position.title}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" paragraph sx={{ minHeight: '40px' }}>
                          {position.description.length > 80
                            ? `${position.description.substring(0, 80)}...`
                            : position.description}
                        </Typography>
                        
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                          <Typography variant="caption" color="textSecondary">
                            Map: {position.map.name}
                          </Typography>
                          <Chip
                            label={position.type}
                            size="small"
                            color="secondary"
                          />
                        </Box>
                        
                        <Divider sx={{ my: 1 }} />
                        
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="caption">
                            By {position.creator.username}
                          </Typography>
                          <Typography variant="body2">
                            👍 {position.upvotes} • 👎 {position.downvotes}
                          </Typography>
                        </Box>
                      </CardContent>
                    </CardActionArea>
                  </Card>
                </Grid>
              ))
            ) : (
              <Grid item xs={12}>
                <Typography align="center" sx={{ py: 4 }}>
                  No positions found matching your search criteria.
                </Typography>
              </Grid>
            )}
          </Grid>
        </>
      )}
    </Container>
  );
};

export default Positions; 