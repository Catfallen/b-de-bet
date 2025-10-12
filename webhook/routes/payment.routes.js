const express = require('express');
const router = express.Router();
const paymentController = require('../controller/payment.controller');
const authMiddleware = require('../../api/middlewares/authMiddleware');

router.post('/pagar',authMiddleware,paymentController.pagar);
router.post('/webhook',paymentController.webhook);


module.exports = router