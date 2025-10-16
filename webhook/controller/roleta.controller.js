const roletaService = require('../service/roleta.services');



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
    if(!idRoleta){
        return res.status(500).json("Não foi possivel definir um id para a roleta");
    }


    return res.status(200).json({userId,valor,aposta_id,cor,corAleatoria,resultado,idRoleta});
    }catch(err){ 
        return res.status(500).json({"msg":"Não foi possivel criar aposta"});
    }
}

module.exports = {novaRoletaBet}