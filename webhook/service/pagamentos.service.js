const {pool} = require('../config/db');


// 4️⃣ Inserir o pagamento na tabela 'pagamentos'
//    - payment_id deve vir de txData.id ou response.id
//    - status inicialmente será 'pending' até o webhook atualizar
//    - valor = transaction_amount
//    - payload = response completo (opcional)
//    - data_recebimento = NOW()
        
async function novoPagamento({payment_id,status,valor,payload,userId}) {
    console.log("service novo pagamento")
    console.log(userId);//resposta do console.log 1
    try{
        const paymentIdBigInt = BigInt(payment_id);
        const query = `INSERT INTO pagamentos (payment_id, status, valor, payload, usuario_id)
VALUES ($1, $2, $3, $4, $5)
ON CONFLICT (payment_id) 
DO UPDATE SET status = EXCLUDED.status,
              valor = EXCLUDED.valor,
              payload = EXCLUDED.payload,
              usuario_id = EXCLUDED.usuario_id
RETURNING *;
`
        const values = [paymentIdBigInt, status, valor, payload, userId];
        const {rows} = await pool.query(query,values);
        return rows[0];
    }catch(err){
        console.error("Erro ao inserir pagamento: ",err);
        return false;
    }
}


async function atualizarPagamento({ payment_id, status, payload }) {
    try {
        const paymentIdBigInt = BigInt(payment_id);

        const query = `
            UPDATE pagamentos
            SET status = $1,
                payload = $2
            WHERE payment_id = $3
            RETURNING *;
        `;

        const values = [status, payload, paymentIdBigInt];
        const { rows } = await pool.query(query, values);

        if (rows.length === 0) {
            console.warn(`Pagamento ${payment_id} não encontrado para atualização.`);
            return null;
        }

        return rows[0];
    } catch (err) {
        console.error("Erro ao atualizar pagamento:", err);
        return false;
    }
}

async function getPagamentos({userId}) {
    try{
        const query = `select id,usuario_id,payment_id,status,valor,data_recebimento from pagamentos where usuario_id = $1`;
        const values = [userId];
        const {rows} = await pool.query(query,values);
        console.log(rows);
        return rows;
    }catch(err){
        console.log("Erro na consulta do pagamentos",err);
        return false;
    }
}

async function getTransacoes({userId}) {
    try{
        const query = `select * from transacoes where usuario_id = $1`
        const values = [userId];
        const {rows} = await pool.query(query,values);
        return rows;
    }catch(err){
        console.log("Erro na consulta das transações",err)
    }
}

async function getSaldoAtual({userId}) {
    try{
        console.log('iniciando consulta do saldo atual')
        console.log(userId);
        const query = `select saldo from saldo_atual where usuario_id = $1`;
        const values = [userId];
        const {rows} = await pool.query(query,values);
        console.log(rows);
        return rows[0];
    }catch(err){
        console.log("Erro na consulta do saldo atual");
        return false;
    }
}

module.exports = {
    novoPagamento,
    atualizarPagamento,
    getPagamentos,
    getTransacoes,
    getSaldoAtual
};
