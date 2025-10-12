require('dotenv').config();
const { MercadoPagoConfig, Payment } = require('mercadopago');

// Cria o cliente do Mercado Pago com seu token
const client = new MercadoPagoConfig({
    accessToken: process.env.MP_ACCESS_TOKEN,
    options: { timeout: 5000 } // tempo limite em ms
});

// Cria instância do objeto Payment usando o cliente
const payment = new Payment(client);

// Exemplo de criação de pagamento (sem rota)
async function criarPagamento() {
    const body = {
        transaction_amount: 10.5,
        description: "Produto teste",
        payment_method_id: "pix",
        payer: { email: "cliente@test.com" }
    };

    try {
        const response = await payment.create({ body });
        console.log("Pagamento criado com sucesso:");
        console.log(response['point_of_interaction']['transaction_data']['qr_code']);
         // QR Code
        console.log("Base 64\n")
         console.log(response['point_of_interaction']['transaction_data']['qr_code_base64']); // Base64 QR
    } catch (err) {
        console.error("Erro ao criar pagamento:", err);
    }
}

// Chama a função
criarPagamento();
