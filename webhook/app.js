require('dotenv').config();
const express = require('express');
const app = express();

// ✅ Middleware JSON unificado com rawBody preservado
app.use(express.json({
    limit: '1mb',
    verify: (req, res, buf) => {
        req.rawBody = buf.toString();
    }
}));

const PORT = process.env.PORT || 3000;

// Importa as rotas de pagamento
const paymentRoutes = require('./routes/payment.routes');
const authRoutes = require('./routes/authRoutes');

app.use('/auth',authRoutes);

// Rota principal para pagamentos
app.use("/payments", paymentRoutes);

app.listen(PORT, () => {
    console.log(`✅ Servidor rodando em http://localhost:${PORT}`);
});
