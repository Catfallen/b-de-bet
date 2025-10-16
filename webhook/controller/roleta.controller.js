const roletaService = require('../service/roleta.services');
const betService = require('../service/bet.service');


async function novaRoletaBet(req,res) {
    try{
    const {userId,valor,aposta_id,cor} = req;
    const corAleatoria = require('../utils/random')();
    console.log(corAleatoria)
    let resultado;
    if(corAleatoria != cor){
        resultado = false;
    }else{
        resultado = true;
    }
    //{userId,aposta_id,cor_cliente,cor_server,resultado}
    //console.log({userId,valor,aposta_id,cor,corAleatoria,resultado,idRoleta})
    console.log(userId);
    console.log(aposta_id);
    const idRoleta = await roletaService.insertNewRoletaBet({userId,aposta_id,cor_cliente:cor,cor_server:corAleatoria,resultado});
    console.log(idRoleta);
    if(!idRoleta){
        return res.status(500).json("Não foi possivel definir um id para a roleta");
    }
    let newValor = valor;
    if (resultado){
        if(corAleatoria == "branco"){
            newValor = newValor*-1;
            if(newValor < 0){
                newValor = newValor*-1;
            }
            newValor = (newValor*14)-newValor;
        }else{
            newValor = newValor*-1
            if(newValor < 0){
                newValor = newValor*-1;
            }
        }
    }
    /*
    if(resultado){
        if (corAleatoria == "preto"){
            newValor = newValor*2
        }else if(corAleatoria == "vermelho"){
            newValor = newValor*2
        }else{
            newValor = newValor*14
        }
        if (newValor< 0){
            newValor = newValor*-1
        }
    }else{
        newValor = valor;
    }
    */
    console.log('novo valor: ');
    console.log(newValor);
    const update = await betService.updateBet({id:aposta_id,valor:newValor});
    if(update){
        return res.status(200).json({userId,valor,aposta_id,cor,corAleatoria,resultado,idRoleta});
    }else{
        return res.status(500).json({'msg':"Não foi possivel alterar o status da aposta"});
    }
    }catch(err){ 
        return res.status(500).json({"msg":"Não foi possivel criar aposta",err});
    }
}

module.exports = {novaRoletaBet}