import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Paper,
  Button,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  Chip,
  Avatar,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  IconButton,
  TextField,
  Alert,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Favorite as FavoriteIcon,
  FavoriteBorder as FavoriteBorderIcon,
  ThumbUp as ThumbUpIcon,
  ThumbDown as ThumbDownIcon,
  Send as SendIcon,
  DirectionsCar as DirectionsCarIcon,
  Flag as FlagIcon,
} from '@mui/icons-material';
import { getRouteById, voteOnRoute, addComment } from '../services/routeService';

const RouteDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [route, setRoute] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [comment, setComment] = useState('');
  const [commenting, setCommenting] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    const fetchRouteData = async () => {
      try {
        setLoading(true);
        const data = await getRouteById(id);
        setRoute(data);
        // Check if this route is in user's favorites (would be implemented with auth context in a real app)
        setIsFavorite(false);
      } catch (err) {
        console.error('Error fetching route:', err);
        setError('Failed to load route details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchRouteData();
  }, [id]);

  const handleVote = async (voteType) => {
    try {
      const updatedRoute = await voteOnRoute(id, voteType);
      setRoute(updatedRoute);
    } catch (err) {
      console.error('Error voting on route:', err);
      setError('Failed to register your vote. Please try again.');
    }
  };

  const handleCommentSubmit = async () => {
    if (!comment.trim()) return;

    try {
      setCommenting(true);
      // In a real app, you'd get the user info from auth context
      const commentData = {
        user: { _id: 'user1', username: 'CurrentUser' },
        content: comment
      };
      
      const updatedRoute = await addComment(id, commentData);
      setRoute(updatedRoute);
      setComment('');
    } catch (err) {
      console.error('Error adding comment:', err);
      setError('Failed to add your comment. Please try again.');
    } finally {
      setCommenting(false);
    }
  };

  const toggleFavorite = () => {
    // In a real app, this would call an API to add/remove from favorites
    setIsFavorite(!isFavorite);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="70vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate(-1)}
          sx={{ mt: 2 }}
        >
          Go Back
        </Button>
      </Container>
    );
  }

  if (!route) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="info">Route not found</Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/routes')}
          sx={{ mt: 2 }}
        >
          Back to Routes
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate(-1)}
        sx={{ mb: 2 }}
      >
        Back
      </Button>
      
      <Paper elevation={2} sx={{ p: { xs: 2, md: 4 }, borderRadius: 2 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            {route.title}
          </Typography>
          <IconButton onClick={toggleFavorite} color={isFavorite ? 'secondary' : 'default'}>
            {isFavorite ? <FavoriteIcon /> : <FavoriteBorderIcon />}
          </IconButton>
        </Box>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 3 }}>
          <Chip 
            icon={<DirectionsCarIcon />} 
            label={route.vehicleType} 
            color="primary" 
            variant="outlined"
          />
          <Chip 
            icon={<FlagIcon />} 
            label={route.gameMode} 
            color="secondary" 
            variant="outlined"
          />
          <Chip 
            label={`Effectiveness: ${route.effectiveness}/5`} 
            variant="outlined"
          />
        </Box>
        
        <Typography variant="body1" paragraph>
          {route.description}
        </Typography>
        
        <Divider sx={{ my: 3 }} />
        
        {/* Route Visualization - In a real app, this would be a canvas or map showing the route */}
        <Box 
          sx={{ 
            height: 400, 
            bgcolor: 'grey.100', 
            borderRadius: 1, 
            mb: 3, 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center' 
          }}
        >
          <Typography variant="body2" color="textSecondary">
            Map visualization would be displayed here
          </Typography>
        </Box>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Created by
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ mr: 2 }}>
                    {route.creator.username.charAt(0)}
                  </Avatar>
                  <Typography>{route.creator.username}</Typography>
                </Box>
                <Typography variant="body2" color="textSecondary">
                  Created: {new Date(route.createdAt).toLocaleDateString()}
                </Typography>
                {route.updatedAt !== route.createdAt && (
                  <Typography variant="body2" color="textSecondary">
                    Updated: {new Date(route.updatedAt).toLocaleDateString()}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={8}>
            <Card variant="outlined">
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">
                    Voting
                  </Typography>
                  <Box>
                    <Button 
                      startIcon={<ThumbUpIcon />} 
                      onClick={() => handleVote('up')}
                      color="primary"
                    >
                      {route.upvotes}
                    </Button>
                    <Button 
                      startIcon={<ThumbDownIcon />} 
                      onClick={() => handleVote('down')}
                      color="error"
                      sx={{ ml: 1 }}
                    >
                      {route.downvotes}
                    </Button>
                  </Box>
                </Box>
                
                <Divider sx={{ my: 2 }} />
                
                <Typography variant="h6" gutterBottom>
                  Comments ({route.comments.length})
                </Typography>
                
                <List>
                  {route.comments.map((comment) => (
                    <ListItem key={comment._id} alignItems="flex-start" sx={{ px: 0 }}>
                      <ListItemAvatar>
                        <Avatar>{comment.user.username.charAt(0)}</Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="subtitle2">{comment.user.username}</Typography>
                            <Typography variant="caption" color="textSecondary">
                              {new Date(comment.createdAt).toLocaleDateString()}
                            </Typography>
                          </Box>
                        }
                        secondary={comment.content}
                      />
                    </ListItem>
                  ))}
                </List>
                
                <Box sx={{ display: 'flex', mt: 2 }}>
                  <TextField
                    fullWidth
                    variant="outlined"
                    placeholder="Add a comment..."
                    size="small"
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    disabled={commenting}
                  />
                  <Button
                    color="primary"
                    startIcon={<SendIcon />}
                    onClick={handleCommentSubmit}
                    disabled={!comment.trim() || commenting}
                    sx={{ ml: 1 }}
                  >
                    Post
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default RouteDetail; 