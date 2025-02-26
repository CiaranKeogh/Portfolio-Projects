import React, { useState, useEffect } from 'react';
import { Routes as RouterRoutes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';

// Layout components
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';

// Page components
import Home from './pages/Home';
import Maps from './pages/Maps';
import MapDetail from './pages/MapDetail';
import RoutesPage from './pages/Routes';
import RouteDetail from './pages/RouteDetail';
import CreateRoute from './pages/CreateRoute';
import Positions from './pages/Positions';
import PositionDetail from './pages/PositionDetail';
import CreatePosition from './pages/CreatePosition';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

// Auth context
import { AuthProvider } from './context/AuthContext';

// Private route component
const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
};

function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate initial loading
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <Box className="loading-spinner">
        <img src="/assets/loading.gif" alt="Loading..." width="80" height="80" />
      </Box>
    );
  }

  return (
    <AuthProvider>
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Header />
        <Box component="main" sx={{ flexGrow: 1, py: 3 }}>
          <RouterRoutes>
            <Route path="/" element={<Home />} />
            
            {/* Map routes */}
            <Route path="/maps" element={<Maps />} />
            <Route path="/maps/:id" element={<MapDetail />} />
            
            {/* Tactical routes */}
            <Route path="/routes" element={<RoutesPage />} />
            <Route path="/routes/:id" element={<RouteDetail />} />
            <Route path="/routes/create" element={
              <PrivateRoute>
                <CreateRoute />
              </PrivateRoute>
            } />
            
            {/* Power positions */}
            <Route path="/positions" element={<Positions />} />
            <Route path="/positions/:id" element={<PositionDetail />} />
            <Route path="/positions/create" element={
              <PrivateRoute>
                <CreatePosition />
              </PrivateRoute>
            } />
            
            {/* Authentication */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={
              <PrivateRoute>
                <Profile />
              </PrivateRoute>
            } />
            
            {/* 404 page */}
            <Route path="*" element={<NotFound />} />
          </RouterRoutes>
        </Box>
        <Footer />
      </Box>
    </AuthProvider>
  );
}

export default App; 