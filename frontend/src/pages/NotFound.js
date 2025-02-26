import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Button, Container, Typography } from '@mui/material';
import { Home as HomeIcon } from '@mui/icons-material';

const NotFound = () => {
  return (
    <Container maxWidth="md">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '70vh',
          textAlign: 'center',
        }}
      >
        <Typography variant="h1" color="primary" sx={{ fontWeight: 'bold', fontSize: { xs: '5rem', md: '8rem' } }}>
          404
        </Typography>
        <Typography variant="h4" color="textSecondary" gutterBottom>
          Page Not Found
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, mb: 4, maxWidth: '600px' }}>
          The page you are looking for might have been removed, had its name changed,
          or is temporarily unavailable. Please check the URL or return to the homepage.
        </Typography>
        <Box
          component="img"
          src="/assets/tank-404.svg"
          alt="Tank broken down"
          sx={{
            maxWidth: '100%',
            height: 'auto',
            width: '300px',
            my: 4,
          }}
        />
        <Button
          variant="contained"
          color="primary"
          component={RouterLink}
          to="/"
          startIcon={<HomeIcon />}
          sx={{ mt: 2 }}
        >
          Back to Home
        </Button>
      </Box>
    </Container>
  );
};

export default NotFound; 