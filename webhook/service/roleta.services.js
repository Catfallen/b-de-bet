const {pool} = require('../config/db');

async function insertNewRoletaBet({userId,aposta_id,cor_cliente,cor_server,resultado}) {
    try{
        const query = `insert into roleta (usuario_id,aposta_id,cor_cliente,cor_server,resultado) values ($1,$2,$3,$4,$5) RETURNING *`;
        const values = [userId,aposta_id,cor_cliente,cor_server,resultado];
        const {rows} = await pool.query(query,values);
        console.log(rows);
        return rows[0];
    }catch(err){
        console.log("Erro no insert da tabela roleta",err);
        return false;
    }
}


module.exports = {
    insertNewRoletaBet
}