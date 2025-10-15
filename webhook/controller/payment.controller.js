const { MercadoPagoConfig, Payment } = require('mercadopago');
const pagamentoService = require('../service/pagamentos.service');
const client = new MercadoPagoConfig({
    accessToken: process.env.MP_ACCESS_TOKEN,
    options: { timeout: 5000 }
});

const payment = new Payment(client);
const processedPayments = new Set();

async function pagar(req, res) {
    // 1️⃣ Obter o ID do usuário que está fazendo o pagamento
    //    - Esse ID provavelmente vem do token JWT ou do middleware de autenticação
    const userId = req.userId;
    console.log(req.userId);
    console.log('/pagar user id: \n');
    console.log(req.userId);
    console.log("===================")
    // 2️⃣ Extrair informações obrigatórias do body
    const { transaction_amount, description, payer_email } = req.body;
    if (!transaction_amount || !description || !payer_email)
        return res.status(400).json({ error: 'Campos obrigatórios faltando.' });

    try {
        // 3️⃣ Criar o pagamento no Mercado Pago via SDK
        const response = await payment.create({
            body: {
                transaction_amount: Number(transaction_amount),
                description,
                payment_method_id: 'pix',
                payer: { email: payer_email }
            }
        });

        //const txData = response.point_of_interaction.transaction_data;
        const txData = response;
        console.log("Pagamento criado com sucesso!");

        // 4️⃣ Inserir o pagamento na tabela 'pagamentos'
        //    - payment_id deve vir de txData.id ou response.id
        //    - status inicialmente será 'pending' até o webhook atualizar
        //    - valor = transaction_amount
        //    - payload = response completo (opcional)
        //    - data_recebimento = NOW()
        const sucess = await pagamentoService.novoPagamento({
            payment_id: response.id,
            status: 'pending',
            valor: transaction_amount,
            payload: response,
            userId: userId
        });
        

        // 6️⃣ Retornar ao front-end os dados do QR Code ou link de pagamento
        return res.status(201).json({'id':txData.id,"sucess":sucess,'payload':txData.point_of_interaction.transaction_data});

    } catch (err) {
        // 7️⃣ Tratar erro caso o pagamento não seja criado
        console.error('Erro ao criar pagamento:', err);
        return res.status(500).json({ error: 'Erro ao processar pagamento.' });
    }
}
async function webhook(req, res) {
    try {
        // 1️⃣ Responde rápido para o Mercado Pago
        res.sendStatus(200);

        // 2️⃣ Extrai o body e o paymentId
        const body = req.body;
        const paymentId = body.data?.id || body.id;
        if (!paymentId) {
            console.warn("⚠️ Webhook recebido sem payment id:", body);
            return;
        }

        // 3️⃣ Evita processar duplicado
        if (processedPayments.has(paymentId)) {
            console.log("Pagamento já processado:", paymentId);
            return;
        }

        processedPayments.add(paymentId);
        setTimeout(() => processedPayments.delete(paymentId), 60000);

        // 4️⃣ Consulta detalhes do pagamento
        const paymentInstance = new Payment(client);
        const info = await paymentInstance.get({ id: paymentId });

        // 5️⃣ Extrai o status
        const status = info.status || 'unknown';
        console.log(`💰 Pagamento ${paymentId} status: ${status}`);

        // 6️⃣ Atualiza ou registra o pagamento
        const success = await pagamentoService.atualizarPagamento({
            payment_id: info.id,
            status,
            payload: info
        });

        if (!success) {
            console.log("❌ Erro ao atualizar pagamento no banco de dados");
        } else {
            console.log("💾 Pagamento atualizado com sucesso:", info.id);
        }

        // 7️⃣ Ações conforme o status
        if (status === 'approved') {
            console.log(`✅ Pagamento aprovado!`);
            // ex: atualizar saldo, liberar acesso, etc.
        } else if (status === 'rejected') {
            console.log(`❌ Pagamento rejeitado.`);
        } else if (status === 'pending') {
            console.log(`🕒 Pagamento pendente.`);
        } else if (status === 'cancelled') {
            console.log(`🚫 Pagamento cancelado.`);
        } else {
            console.log("⚠️ Status desconhecido:", status);
        }

    } catch (err) {
        console.error("❗Erro processando webhook:", err);
    }
}

async function paymentsList(req,res) {
    try{
        const userId = req.userId;
        const lista = await pagamentoService.getPagamentos({userId})
        if (!lista){
            return res.status(404).json("Não foi possivel fazer a consulta dos pagamentos");
        }
        return res.status(200).json(lista);
    }catch(err){
        return res.status(500).json({"msg":"Erro na consulta dos pagamentos"})
    }
}

async function transacoes_aprovadas(req,res) {
     try{
        const userId = req.userId;
        const lista = await pagamentoService.getTransacoes({userId})
        if (!lista){
            return res.status(404).json("Não foi possivel fazer a consulta dos pagamentos");
        }
        return res.status(200).json(lista);
    }catch(err){
        return res.status(500).json({"msg":"Erro na consulta das transações"})
    }
}

async function saldoAtual(req,res) {
    try{
        const userId = req.userId;
        const saldo = await pagamentoService.getSaldoAtual({userId});
        if(!saldo){
            return res.status(404).json("Saldo não encontrado");
        }
        return res.status(200).json(saldo);
    }catch(err){
        return res.status(500).json({'msg':"Erro na consulta do saldo atual"});
    }
}

module.exports = { 
    pagar, 
    webhook, 
    paymentsList,
    transacoes_aprovadas,
    saldoAtual
};