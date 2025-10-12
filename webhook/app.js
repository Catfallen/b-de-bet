require('dotenv').config();
const express = require('express');
const { MercadoPagoConfig, Payment } = require('mercadopago');
const crypto = require('crypto');

const app = express();
app.use(express.json({ limit: '1mb' }));
app.use(express.json({
    verify: (req, res, buf) => {
        req.rawBody = buf.toString(); // mantém o raw body para validar a assinatura
    }
}));
const PORT = process.env.PORT || 3000;

// Configuração do Mercado Pago
const client = new MercadoPagoConfig({
    accessToken: process.env.MP_ACCESS_TOKEN,
    options: { timeout: 5000 }
});

const payment = new Payment(client);

// Cache simples para evitar processar o mesmo paymentId várias vezes
const processedPayments = new Set();

/**
 * Rota POST /pagar
 * Body esperado:
 * {
 *   "transaction_amount": 10.5,
 *   "description": "Produto teste",
 *   "payer_email": "cliente@test.com"
 * }
 */
app.post('/pagar', async (req, res) => {
    const { transaction_amount, description, payer_email } = req.body;

    if (!transaction_amount || !description || !payer_email) {
        return res.status(400).json({ error: 'Campos obrigatórios faltando.' });
    }

    const body = {
        transaction_amount: Number(transaction_amount),
        description,
        payment_method_id: 'pix',
        payer: { email: payer_email }
    };

    try {
        const response = await payment.create({ body });
        const txData = response['point_of_interaction']['transaction_data'];
        console.log("post /pagar")
        console.log("Pagamento criado com sucesso:");
        //console.log("QR Code:", txData['qr_code']);
        //console.log("Base64 QR Code:", txData['qr_code_base64']);
        console.log('\n')
        return res.status(201).json(txData);
    } catch (err) {
        console.error('Erro ao criar pagamento:', err);
        return res.status(500).json({ error: 'Erro ao processar pagamento.' });
    }
});

/**
 * Rota POST /webhook
 * Recebe notificações do Mercado Pago
 */
app.post('/webhook', async (req, res) => {
    try {
        res.sendStatus(200); // responde rápido pro MP

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
        setTimeout(() => processedPayments.delete(paymentId), 60 * 1000);

        // Cria uma nova instância da classe Payment (como no /pagar)
        const paymentInstance = new Payment(client);
        const info = await paymentInstance.get({ id: paymentId });

        const status = info.status || 'unknown';
        console.log("Webhook")
        console.log(`💰 Pagamento ${paymentId} status: ${status}`);

        if (status === 'pending') {
            console.log(`🕒 Pagamento ${paymentId} ainda está pendente.`);
        } else if (status === 'approved') {
            console.log(`✅ Pagamento ${paymentId} aprovado!`);
            // liberar produto, enviar email, etc.
        } else if (status === 'rejected') {
            console.log(`❌ Pagamento ${paymentId} foi rejeitado.`);
        }
        console.log("\n")

    } catch (err) {
        console.error("❗Erro processando webhook:", err);
    }
});



app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});
