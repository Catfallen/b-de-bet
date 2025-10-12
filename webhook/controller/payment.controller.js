const { MercadoPagoConfig, Payment } = require('mercadopago');

const client = new MercadoPagoConfig({
    accessToken: process.env.MP_ACCESS_TOKEN,
    options: { timeout: 5000 }
});

const payment = new Payment(client);
const processedPayments = new Set();

async function pagar(req, res) {
    const { transaction_amount, description, payer_email } = req.body;
    if (!transaction_amount || !description || !payer_email)
        return res.status(400).json({ error: 'Campos obrigatórios faltando.' });

    try {
        const response = await payment.create({
            body: {
                transaction_amount: Number(transaction_amount),
                description,
                payment_method_id: 'pix',
                payer: { email: payer_email }
            }
        });

        const txData = response.point_of_interaction.transaction_data;
        console.log("Pagamento criado com sucesso!");
        return res.status(201).json(txData);
    } catch (err) {
        console.error('Erro ao criar pagamento:', err);
        return res.status(500).json({ error: 'Erro ao processar pagamento.' });
    }
}

async function webhook(req, res) {
    try {
        res.sendStatus(200);

        const body = req.body;
        const paymentId = body.data?.id || body.id;
        if (!paymentId) {
            console.warn("⚠️ Webhook recebido sem payment id:", body);
            return;
        }

        if (processedPayments.has(paymentId)) {
            console.log("Pagamento já processado:", paymentId);
            return;
        }
        processedPayments.add(paymentId);
        setTimeout(() => processedPayments.delete(paymentId), 60000);

        const paymentInstance = new Payment(client);
        const info = await paymentInstance.get({ id: paymentId });

        const status = info.status || 'unknown';
        console.log(`💰 Pagamento ${paymentId} status: ${status}`);

        if (status === 'approved') {
            console.log(`✅ Pagamento aprovado!`);
            // ex: atualizar DB, enviar email, etc.
        } else if (status === 'rejected') {
            console.log(`❌ Pagamento rejeitado.`);
        } else {
            console.log(`🕒 Pagamento pendente.`);
        }

    } catch (err) {
        console.error("❗Erro processando webhook:", err);
    }
}

module.exports = { pagar, webhook };
