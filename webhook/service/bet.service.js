const {pool} = require('../config/db');

async function newBet({userId,valor}) {
    try{
        const query = `insert into apostas (usuario_id,valor) values ($1,$2) RETURNING id`;
        const values = [userId,valor];
        const {rows} = await pool.query(query,values);
        return rows[0];
    }catch(err){
        console.log('Erro na criação da aposta',err);
        return false;
    }
}

module.exports = {newBet};