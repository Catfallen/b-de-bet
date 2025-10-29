const roletaService = require('../service/roleta.services');
const betService = require('../service/bet.service');


async function novaRoletaBet(req, res) {
    try {
        
        const { userId, valor, aposta_id, cor } = req;
        
        const corAleatoria = require('../utils/random')();//Escolhe uma cor aleatoria
        console.log(corAleatoria)
        let resultado;
        
        //Comparação das cores
        if (corAleatoria != cor) {
            resultado = false;
        } else {
            resultado = true;
        }
        console.log(userId);
        console.log(aposta_id);
        
        //Insere um novo registro na tabela roleta e retorna o idRoleta
        const idRoleta = await roletaService.insertNewRoletaBet({ userId, aposta_id, cor_cliente: cor, cor_server: corAleatoria, resultado });
        console.log(idRoleta);
        if (!idRoleta) {
            return res.status(500).json("Não foi possivel definir um id para a roleta");
        }
        //valor do req.valor
        let newValor = valor;
        
        //resultado == true
        //Se for branco x14
        //Vermelho ou preto x2, no caso ele inverte o valor para positivo
        if (resultado) {
            if (corAleatoria == "branco") {
                newValor = newValor * -1;
                if (newValor < 0) {
                    newValor = newValor * -1;
                }
                newValor = (newValor * 14) - newValor;
            } else {
                newValor = newValor * -1
                if (newValor < 0) {
                    newValor = newValor * -1;
                }
            }
        }
        // Caso contrário ele apenas envia o valor padrão negativo
        console.log('novo valor: ');
        console.log(newValor);
        //Atualiza a aposta com o novo valor e define o status para 'approved'
        const update = await betService.updateBet({ id: aposta_id, valor: newValor });
        //Novamente o banco de dados chama uma função trigger after_update 
        //e checka se a aposta foi aprovada.
        //Se for aprovada ele insere um novo registro na tabela transações do tipo 'aposta' com valor + ou -

        if (update) {
            return res.status(200).json({ userId, valor, aposta_id, cor, corAleatoria, resultado, idRoleta });
        } else {
            return res.status(500).json({ 'msg': "Não foi possivel alterar o status da aposta" });
        }
    } catch (err) {
        return res.status(500).json({ "msg": "Não foi possivel criar aposta", err });
    }
}

module.exports = { novaRoletaBet }