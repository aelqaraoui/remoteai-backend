const express = require('express');
const router = express.Router();
const profileController = require('../controllers/profile.controller');

router.post('/create', profileController.createProfile);
router.put('/update/:userId', profileController.updateProfile);
router.get('/profile/:userId', profileController.getProfileByUserId);

module.exports = router;
