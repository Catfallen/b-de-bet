const express = require('express');
const router = express.Router();
const authController = require('../controller/authController');
const authMiddleware = require('../middlewares/authMiddleware');

router.post('/register', authController.register);
router.post('/login', authController.login);
router.get('/protected', authMiddleware, authController.protectedRoute);

module.exports = router;
