const express = require('express');
const router = express.Router();
const paymentController = require('../controller/payment.controller');
const authMiddleware = require('../middlewares/authMiddleware');

router.post('/pagar',authMiddleware,paymentController.pagar);
router.post('/webhook',paymentController.webhook);
router.post("/pagamentos/list",authMiddleware,paymentController.paymentsList)
router.post('/transacoes/list',authMiddleware,paymentController.transacoes_aprovadas)
router.post('/saldo',authMiddleware,paymentController.saldoAtual);

router.get('/teste',authMiddleware,async (req,res)=>{
    try{
        console.log(req.userId);
        res.status(200).json({"msg":req.userId});
    }catch(err){
        console.log("")
    }
});

module.exports = router