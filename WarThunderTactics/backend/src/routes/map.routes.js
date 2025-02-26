const express = require('express');
const router = express.Router();

// Import controllers (we'll create these later)
const { 
  getMaps,
  getMap,
  createMap,
  updateMap,
  deleteMap,
  getMapsByGameMode,
  searchMaps
} = require('../controllers/map.controller');

// Import middleware
const { protect, authorize } = require('../middleware/auth.middleware');

// Routes
router.route('/')
  .get(getMaps)
  .post(protect, authorize('admin', 'moderator'), createMap);

router.route('/:id')
  .get(getMap)
  .put(protect, authorize('admin', 'moderator'), updateMap)
  .delete(protect, authorize('admin'), deleteMap);

router.get('/gamemode/:gameMode', getMapsByGameMode);
router.get('/search/:searchTerm', searchMaps);

module.exports = router; 