const express = require('express');
const router = express.Router();

// Import controllers (we'll create these later)
const {
  getRoutes,
  getRoute,
  createRoute,
  updateRoute,
  deleteRoute,
  voteRoute,
  getRoutesByMap,
  getRoutesByUser,
  getTopRatedRoutes,
  getRecentRoutes,
  searchRoutes
} = require('../controllers/route.controller');

// Import middleware
const { protect, authorize } = require('../middleware/auth.middleware');

// Routes
router.route('/')
  .get(getRoutes)
  .post(protect, createRoute);

router.route('/:id')
  .get(getRoute)
  .put(protect, updateRoute)
  .delete(protect, deleteRoute);

router.put('/:id/vote', protect, voteRoute);
router.get('/map/:mapId', getRoutesByMap);
router.get('/user/:userId', getRoutesByUser);
router.get('/top', getTopRatedRoutes);
router.get('/recent', getRecentRoutes);
router.get('/search/:searchTerm', searchRoutes);

module.exports = router; 