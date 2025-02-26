const express = require('express');
const router = express.Router();

// Import controllers (we'll create these later)
const { 
  register, 
  login, 
  getMe, 
  forgotPassword,
  resetPassword,
  updatePassword
} = require('../controllers/auth.controller');

// Import middleware (we'll create this later)
const { protect } = require('../middleware/auth.middleware');

// Routes
router.post('/register', register);
router.post('/login', login);
router.get('/me', protect, getMe);
router.post('/forgotpassword', forgotPassword);
router.put('/resetpassword/:resettoken', resetPassword);
router.put('/updatepassword', protect, updatePassword);

module.exports = router; 