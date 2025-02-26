const express = require('express');
const router = express.Router();

// Import controllers (we'll create these later)
const {
  getUsers,
  getUser,
  updateUser,
  deleteUser,
  updateProfile,
  getUserFavorites,
  addToFavorites,
  removeFromFavorites
} = require('../controllers/user.controller');

// Import middleware
const { protect, authorize } = require('../middleware/auth.middleware');

// Routes
// Admin routes
router.route('/')
  .get(protect, authorize('admin'), getUsers);

router.route('/:id')
  .get(getUser)
  .put(protect, authorize('admin'), updateUser)
  .delete(protect, authorize('admin'), deleteUser);

// User profile routes
router.put('/profile', protect, updateProfile);

// Favorites management
router.get('/favorites', protect, getUserFavorites);
router.post('/favorites/:type/:id', protect, addToFavorites);
router.delete('/favorites/:type/:id', protect, removeFromFavorites);

module.exports = router; 