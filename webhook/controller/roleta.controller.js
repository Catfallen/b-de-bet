const roletaService = require('../service/roleta.services');



async function novaRoletaBet(req,res) {
    const {userId,valor,aposta_id} = req;
    //const valor = req.valor;
    //req.valor = valor;
    //req.aposta_id = aposta_id;
    return res.status(200).json({userId,valor,aposta_id});
}

module.exports = {novaRoletaBet}