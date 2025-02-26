import React from 'react';
import { Box, Container, Typography, Link, Grid, Divider } from '@mui/material';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[900],
        color: 'white',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={3}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              War Thunder Tactics
            </Typography>
            <Typography variant="body2">
              A community-driven platform for sharing tactical information for War Thunder ground battles.
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Quick Links
            </Typography>
            <Link href="/maps" color="inherit" display="block" sx={{ mb: 1 }}>
              Maps
            </Link>
            <Link href="/routes" color="inherit" display="block" sx={{ mb: 1 }}>
              Routes
            </Link>
            <Link href="/positions" color="inherit" display="block" sx={{ mb: 1 }}>
              Positions
            </Link>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Legal
            </Typography>
            <Link href="/privacy" color="inherit" display="block" sx={{ mb: 1 }}>
              Privacy Policy
            </Link>
            <Link href="/terms" color="inherit" display="block" sx={{ mb: 1 }}>
              Terms of Service
            </Link>
            <Typography variant="body2" sx={{ mt: 2 }}>
              War Thunder™ is a trademark of Gaijin Entertainment. This site is not affiliated with Gaijin Entertainment.
            </Typography>
          </Grid>
        </Grid>
        <Divider sx={{ my: 2, backgroundColor: 'rgba(255, 255, 255, 0.2)' }} />
        <Typography variant="body2" align="center">
          {'© '}
          {new Date().getFullYear()}
          {' War Thunder Tactics. All rights reserved.'}
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer; 