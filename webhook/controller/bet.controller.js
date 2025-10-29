const betService = require('../service/bet.service');
const {getSaldoAtual} = require("../service/pagamentos.service");
async function novaAposta(req,res,next) {
    try{
        //Valores do body da requisição
        const userId = req.userId;
        let {valor} = req.body
        
        //Saldo atua
        const saldo = await getSaldoAtual({userId});
        valor = parseFloat(valor);
        
        //Verifica se o saldo é sulficiente
        if(!saldo || parseFloat(saldo.saldo) < valor){
            return res.status(302).json("Saldo insulficiente");
        }
        if(valor > 0){ //valor padrão deve ser negativo
            valor = valor*-1;
        }
        //insere um novo registro na tabela apostas e retorna o aposta_id
        const aposta_id = await betService.newBet({userId,valor});
        if(!aposta_id){
            return res.status(500).json({"msg":"NãO foi possivel criar a aposta"});
        }
        //define os valores para o proximo controlelr
        req.valor = valor;
        req.aposta_id = aposta_id.id;
        req.cor = req.body.cor;
        next(); //redireciona para o controller (roletaController.novaRoletaBet)
    }catch(err){
        console.log("Erro na criação de uma nova aposta bet.Controller",err);
        return res.status(500).json({"msg":"Não foi possivel criar a aposta"})
    }
}

module.exports = {novaAposta};