const express = require('express');
const router = express.Router();
const paymentController = require('../controller/payment.controller');
const authMiddleware = require('../middlewares/authMiddleware');

router.post('/pagar',authMiddleware,paymentController.pagar); //rota para pegar o qr code
//Faz um registro na tabela pagamentos com o valor 'pending'
//Verifica também se o pagamento já existe

router.post('/webhook',paymentController.webhook); //nesta rota o mercado pago envia uma notificação
//Verifica se o pagamento existe e atualiza para o valor recebido no caso 'approved'

/*Assim que o pagamento é aprovado, o banco de dados usa um trigger 'after_update' para inserir um novo registro na tabela transações.
Um registro do tipo 'deposito'
*/



router.post("/pagamentos/list",authMiddleware,paymentController.paymentsList) //Lista de pagamentos
router.post('/transacoes/list',authMiddleware,paymentController.transacoes_aprovadas)//Lista de transações

router.post('/saldo',authMiddleware,paymentController.saldoAtual);//saldo atual
//O calculo do saldo é feito a partir da soma do registros de transações
//No caso a tabela transações tem os tipos deposito(+) e aposta(- ou +);

router.get('/teste',authMiddleware,async (req,res)=>{
    try{
        console.log(req.userId);
        res.status(200).json({"msg":req.userId});
    }catch(err){
        console.log("")
    }
});

module.exports = router