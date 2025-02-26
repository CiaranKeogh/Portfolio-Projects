const express = require('express');
const router = express.Router();

// Import controllers (we'll create these later)
const {
  getPositions,
  getPosition,
  createPosition,
  updatePosition,
  deletePosition,
  votePosition,
  getPositionsByMap,
  getPositionsByUser,
  getTopRatedPositions,
  getRecentPositions,
  searchPositions
} = require('../controllers/position.controller');

// Import middleware
const { protect, authorize } = require('../middleware/auth.middleware');

// Routes
router.route('/')
  .get(getPositions)
  .post(protect, createPosition);

router.route('/:id')
  .get(getPosition)
  .put(protect, updatePosition)
  .delete(protect, deletePosition);

router.put('/:id/vote', protect, votePosition);
router.get('/map/:mapId', getPositionsByMap);
router.get('/user/:userId', getPositionsByUser);
router.get('/top', getTopRatedPositions);
router.get('/recent', getRecentPositions);
router.get('/search/:searchTerm', searchPositions);

module.exports = router; 