const express = require('express');
const authMiddleware = require('../middlewares/authMiddleware');
const router = express.Router();


router.post("/apostar/roleta",authMiddleware);
router.post("/apostar/mines",authMiddleware);
router.post("/apostar/777_classic",authMiddleware);

module.exports = router;