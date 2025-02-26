import React, { useState, useContext } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Box,
  Menu,
  MenuItem,
  useMediaQuery,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Divider,
  Avatar,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  AccountCircle,
  Close as CloseIcon,
  Map as MapIcon,
  Route as RouteIcon,
  Place as PlaceIcon,
} from '@mui/icons-material';
import { AuthContext } from '../../context/AuthContext';

const Header = () => {
  const { user, isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  
  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };
  
  const handleMenuClose = () => {
    setAnchorEl(null);
  };
  
  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };
  
  const handleLogout = () => {
    logout();
    handleMenuClose();
    navigate('/');
  };
  
  const menuId = 'primary-search-account-menu';
  const renderMenu = (
    <Menu
      anchorEl={anchorEl}
      id={menuId}
      keepMounted
      open={Boolean(anchorEl)}
      onClose={handleMenuClose}
    >
      <MenuItem component={RouterLink} to="/profile" onClick={handleMenuClose}>
        Profile
      </MenuItem>
      <MenuItem onClick={handleLogout}>Logout</MenuItem>
    </Menu>
  );
  
  const drawer = (
    <Box sx={{ width: 250 }} role="presentation">
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 1 }}>
        <IconButton onClick={handleDrawerToggle}>
          <CloseIcon />
        </IconButton>
      </Box>
      <Divider />
      <List>
        <ListItem button component={RouterLink} to="/" onClick={handleDrawerToggle}>
          <ListItemText primary="Home" />
        </ListItem>
        <ListItem button component={RouterLink} to="/maps" onClick={handleDrawerToggle}>
          <ListItemText primary="Maps" />
        </ListItem>
        <ListItem button component={RouterLink} to="/routes" onClick={handleDrawerToggle}>
          <ListItemText primary="Tactical Routes" />
        </ListItem>
        <ListItem button component={RouterLink} to="/positions" onClick={handleDrawerToggle}>
          <ListItemText primary="Power Positions" />
        </ListItem>
      </List>
      <Divider />
      <List>
        {isAuthenticated ? (
          <>
            <ListItem button component={RouterLink} to="/profile" onClick={handleDrawerToggle}>
              <ListItemText primary="Profile" />
            </ListItem>
            <ListItem button onClick={() => { handleLogout(); handleDrawerToggle(); }}>
              <ListItemText primary="Logout" />
            </ListItem>
          </>
        ) : (
          <>
            <ListItem button component={RouterLink} to="/login" onClick={handleDrawerToggle}>
              <ListItemText primary="Login" />
            </ListItem>
            <ListItem button component={RouterLink} to="/register" onClick={handleDrawerToggle}>
              <ListItemText primary="Register" />
            </ListItem>
          </>
        )}
      </List>
    </Box>
  );
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          {isMobile && (
            <IconButton
              edge="start"
              color="inherit"
              aria-label="menu"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          
          <Typography
            variant="h6"
            component={RouterLink}
            to="/"
            sx={{
              flexGrow: 1,
              textDecoration: 'none',
              color: 'inherit',
              display: 'flex',
              alignItems: 'center',
            }}
          >
            War Thunder Tactics
          </Typography>
          
          {!isMobile && (
            <Box sx={{ display: 'flex' }}>
              <Button
                color="inherit"
                component={RouterLink}
                to="/maps"
                startIcon={<MapIcon />}
              >
                Maps
              </Button>
              <Button
                color="inherit"
                component={RouterLink}
                to="/routes"
                startIcon={<RouteIcon />}
              >
                Routes
              </Button>
              <Button
                color="inherit"
                component={RouterLink}
                to="/positions"
                startIcon={<PlaceIcon />}
              >
                Positions
              </Button>
            </Box>
          )}
          
          {isAuthenticated ? (
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <IconButton
                edge="end"
                aria-label="account of current user"
                aria-controls={menuId}
                aria-haspopup="true"
                onClick={handleProfileMenuOpen}
                color="inherit"
              >
                {user?.avatar ? (
                  <Avatar
                    alt={user.username}
                    src={user.avatar}
                    sx={{ width: 32, height: 32 }}
                  />
                ) : (
                  <AccountCircle />
                )}
              </IconButton>
            </Box>
          ) : (
            !isMobile && (
              <Box>
                <Button color="inherit" component={RouterLink} to="/login">
                  Login
                </Button>
                <Button
                  color="secondary"
                  variant="contained"
                  component={RouterLink}
                  to="/register"
                  sx={{ ml: 1 }}
                >
                  Register
                </Button>
              </Box>
            )
          )}
        </Toolbar>
      </AppBar>
      
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={handleDrawerToggle}
      >
        {drawer}
      </Drawer>
      
      {renderMenu}
    </Box>
  );
};

export default Header; 