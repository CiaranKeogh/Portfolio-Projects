import React, { useState, useContext, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Avatar,
  Button,
  Divider,
  Grid,
  Card,
  CardContent,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  CircularProgress,
  Chip,
  TextField,
} from '@mui/material';
import {
  Edit as EditIcon,
  SaveAlt as SaveIcon,
  Route as RouteIcon,
  Place as PlaceIcon,
  Star as StarIcon,
} from '@mui/icons-material';
import { AuthContext } from '../context/AuthContext';

const Profile = () => {
  const { user, logout } = useContext(AuthContext);
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [editMode, setEditMode] = useState(false);
  
  const [userProfile, setUserProfile] = useState({
    username: 'TankCommander',
    email: 'commander@example.com',
    bio: 'Experienced War Thunder player specializing in German tanks and tactical gameplay.',
    avatar: '/assets/avatar.jpg',
    reputation: 250,
    createdRoutes: [
      {
        _id: '1',
        title: 'North Ridge Flanking Route',
        map: { name: 'Advance to the Rhine' },
        upvotes: 42,
      },
      {
        _id: '2',
        title: 'South Forest Ambush Path',
        map: { name: 'Finland' },
        upvotes: 28,
      },
    ],
    createdPositions: [
      {
        _id: '1',
        title: 'Eastern Hill Sniper Spot',
        map: { name: 'Karelia' },
        upvotes: 35,
      },
    ],
    favoriteRoutes: [
      {
        _id: '3',
        title: 'Central Push Strategy',
        map: { name: 'Berlin' },
        upvotes: 67,
        creator: { username: 'StrategyMaster' },
      },
    ],
    favoritePositions: [
      {
        _id: '2',
        title: 'Central Ridge Cover',
        map: { name: 'Advance to the Rhine' },
        upvotes: 54,
        creator: { username: 'SniperElite' },
      },
    ],
  });
  
  const [editForm, setEditForm] = useState({
    username: '',
    email: '',
    bio: '',
  });
  
  useEffect(() => {
    // In a real app, this would fetch the user profile from the API
    // For now, we'll just use the static data above
    setEditForm({
      username: userProfile.username,
      email: userProfile.email,
      bio: userProfile.bio || '',
    });
  }, [userProfile]);
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  const handleEditToggle = () => {
    if (editMode) {
      // If we're currently in edit mode and toggling off, we need to save changes
      handleSaveProfile();
    }
    setEditMode(!editMode);
  };
  
  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setEditForm({
      ...editForm,
      [name]: value,
    });
  };
  
  const handleSaveProfile = () => {
    setLoading(true);
    
    // In a real app, this would make an API call to update the user profile
    setTimeout(() => {
      setUserProfile({
        ...userProfile,
        username: editForm.username,
        email: editForm.email,
        bio: editForm.bio,
      });
      setLoading(false);
      setEditMode(false);
    }, 1000);
  };
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Grid container spacing={4}>
        {/* Profile Information */}
        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
                <Avatar
                  src={userProfile.avatar}
                  alt={userProfile.username}
                  sx={{ width: 120, height: 120, mb: 2 }}
                />
                {!editMode ? (
                  <>
                    <Typography variant="h5" gutterBottom>
                      {userProfile.username}
                    </Typography>
                    <Chip 
                      label={`Reputation: ${userProfile.reputation}`} 
                      color="primary" 
                      variant="outlined" 
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2" color="textSecondary" align="center">
                      {userProfile.bio || 'No bio provided'}
                    </Typography>
                  </>
                ) : (
                  <Box sx={{ width: '100%', mt: 2 }}>
                    <TextField
                      fullWidth
                      label="Username"
                      name="username"
                      value={editForm.username}
                      onChange={handleFormChange}
                      margin="normal"
                      variant="outlined"
                    />
                    <TextField
                      fullWidth
                      label="Email"
                      name="email"
                      value={editForm.email}
                      onChange={handleFormChange}
                      margin="normal"
                      variant="outlined"
                    />
                    <TextField
                      fullWidth
                      label="Bio"
                      name="bio"
                      value={editForm.bio}
                      onChange={handleFormChange}
                      margin="normal"
                      variant="outlined"
                      multiline
                      rows={3}
                    />
                  </Box>
                )}
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Box sx={{ display: 'flex', justifyContent: 'space-around' }}>
                <Button
                  variant="contained"
                  startIcon={editMode ? <SaveIcon /> : <EditIcon />}
                  onClick={handleEditToggle}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : (editMode ? 'Save' : 'Edit Profile')}
                </Button>
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={logout}
                >
                  Logout
                </Button>
              </Box>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Stats
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Routes Created
                  </Typography>
                  <Typography variant="h6">
                    {userProfile.createdRoutes.length}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Positions Marked
                  </Typography>
                  <Typography variant="h6">
                    {userProfile.createdPositions.length}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Favorite Routes
                  </Typography>
                  <Typography variant="h6">
                    {userProfile.favoriteRoutes.length}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Favorite Positions
                  </Typography>
                  <Typography variant="h6">
                    {userProfile.favoritePositions.length}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
        
        {/* User Content Tabs */}
        <Grid item xs={12} md={8}>
          <Card>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={tabValue} onChange={handleTabChange} aria-label="user content tabs">
                <Tab label="My Routes" icon={<RouteIcon />} iconPosition="start" />
                <Tab label="My Positions" icon={<PlaceIcon />} iconPosition="start" />
                <Tab label="Favorites" icon={<StarIcon />} iconPosition="start" />
              </Tabs>
            </Box>
            
            {/* My Routes Tab */}
            <div role="tabpanel" hidden={tabValue !== 0}>
              {tabValue === 0 && (
                <Box sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">
                      My Tactical Routes
                    </Typography>
                    <Button
                      variant="contained"
                      component={RouterLink}
                      to="/routes/create"
                      size="small"
                    >
                      Create New Route
                    </Button>
                  </Box>
                  
                  {userProfile.createdRoutes.length > 0 ? (
                    <List>
                      {userProfile.createdRoutes.map((route) => (
                        <React.Fragment key={route._id}>
                          <ListItem
                            button
                            component={RouterLink}
                            to={`/routes/${route._id}`}
                          >
                            <ListItemAvatar>
                              <Avatar>
                                <RouteIcon />
                              </Avatar>
                            </ListItemAvatar>
                            <ListItemText
                              primary={route.title}
                              secondary={`Map: ${route.map.name} • Upvotes: ${route.upvotes}`}
                            />
                          </ListItem>
                          <Divider variant="inset" component="li" />
                        </React.Fragment>
                      ))}
                    </List>
                  ) : (
                    <Typography variant="body1" align="center" sx={{ py: 4 }}>
                      You haven't created any routes yet.
                    </Typography>
                  )}
                </Box>
              )}
            </div>
            
            {/* My Positions Tab */}
            <div role="tabpanel" hidden={tabValue !== 1}>
              {tabValue === 1 && (
                <Box sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">
                      My Power Positions
                    </Typography>
                    <Button
                      variant="contained"
                      component={RouterLink}
                      to="/positions/create"
                      size="small"
                    >
                      Mark New Position
                    </Button>
                  </Box>
                  
                  {userProfile.createdPositions.length > 0 ? (
                    <List>
                      {userProfile.createdPositions.map((position) => (
                        <React.Fragment key={position._id}>
                          <ListItem
                            button
                            component={RouterLink}
                            to={`/positions/${position._id}`}
                          >
                            <ListItemAvatar>
                              <Avatar>
                                <PlaceIcon />
                              </Avatar>
                            </ListItemAvatar>
                            <ListItemText
                              primary={position.title}
                              secondary={`Map: ${position.map.name} • Upvotes: ${position.upvotes}`}
                            />
                          </ListItem>
                          <Divider variant="inset" component="li" />
                        </React.Fragment>
                      ))}
                    </List>
                  ) : (
                    <Typography variant="body1" align="center" sx={{ py: 4 }}>
                      You haven't marked any positions yet.
                    </Typography>
                  )}
                </Box>
              )}
            </div>
            
            {/* Favorites Tab */}
            <div role="tabpanel" hidden={tabValue !== 2}>
              {tabValue === 2 && (
                <Box sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Favorite Routes
                  </Typography>
                  
                  {userProfile.favoriteRoutes.length > 0 ? (
                    <List>
                      {userProfile.favoriteRoutes.map((route) => (
                        <React.Fragment key={route._id}>
                          <ListItem
                            button
                            component={RouterLink}
                            to={`/routes/${route._id}`}
                          >
                            <ListItemAvatar>
                              <Avatar>
                                <RouteIcon />
                              </Avatar>
                            </ListItemAvatar>
                            <ListItemText
                              primary={route.title}
                              secondary={`Map: ${route.map.name} • By: ${route.creator.username} • Upvotes: ${route.upvotes}`}
                            />
                          </ListItem>
                          <Divider variant="inset" component="li" />
                        </React.Fragment>
                      ))}
                    </List>
                  ) : (
                    <Typography variant="body1" align="center" sx={{ py: 2 }}>
                      You haven't saved any routes as favorites yet.
                    </Typography>
                  )}
                  
                  <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
                    Favorite Positions
                  </Typography>
                  
                  {userProfile.favoritePositions.length > 0 ? (
                    <List>
                      {userProfile.favoritePositions.map((position) => (
                        <React.Fragment key={position._id}>
                          <ListItem
                            button
                            component={RouterLink}
                            to={`/positions/${position._id}`}
                          >
                            <ListItemAvatar>
                              <Avatar>
                                <PlaceIcon />
                              </Avatar>
                            </ListItemAvatar>
                            <ListItemText
                              primary={position.title}
                              secondary={`Map: ${position.map.name} • By: ${position.creator.username} • Upvotes: ${position.upvotes}`}
                            />
                          </ListItem>
                          <Divider variant="inset" component="li" />
                        </React.Fragment>
                      ))}
                    </List>
                  ) : (
                    <Typography variant="body1" align="center" sx={{ py: 2 }}>
                      You haven't saved any positions as favorites yet.
                    </Typography>
                  )}
                </Box>
              )}
            </div>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Profile; 