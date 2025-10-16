const betService = require('../service/bet.service');
const {getSaldoAtual} = require("../service/pagamentos.service");
async function novaAposta(req,res,next) {
    try{
        const userId = req.userId;
        let {valor} = req.body
        
        const saldo = await getSaldoAtual({userId});
        valor = parseFloat(valor);
        if(!saldo || parseFloat(saldo.saldo) < valor){
            return res.status(302).json("Saldo insulficiente");
        }
        const aposta_id = await betService.newBet({userId,valor});
        if(!aposta_id){
            return res.status(500).json({"msg":"NãO foi possivel criar a aposta"});
        }
        req.valor = valor;
        req.aposta_id = aposta_id.id;
        req.cor = req.body.cor;
        next();
    }catch(err){
        console.log("Erro na criação de uma nova aposta bet.Controller",err);
        return res.status(500).json({"msg":"Não foi possivel criar a aposta"})
    }
}

module.exports = {novaAposta};