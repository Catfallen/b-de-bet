require('dotenv').config();
const express = require('express');
const http = require('http');
const {WebSocketServer} = require('ws');
const app = express();
//teste do websocket 
const server = http.createServer(app);

// ✅ Middleware JSON unificado com rawBody preservado
app.use(express.json({
    limit: '1mb',
    verify: (req, res, buf) => {
        req.rawBody = buf.toString();
    }
}));

const PORT = process.env.PORT || 3000;

const paymentRoutes = require('./routes/payment.routes'); //rotas de pagamentos
const authRoutes = require('./routes/authRoutes'); //routas de autenticação
const betRoutes = require('./routes/bet.routes'); //rota dos jogos



app.use('/auth',authRoutes,betRoutes);
app.use("/payments", paymentRoutes);
app.use("/bet",betRoutes)


//servidor WebSocket
const wss = new WebSocketServer({server});
wss.on("connection", (ws)=>{
    console.log("Cliente conectado via WebSocket!");
    ws.send("Bem-vindo ao servidor!");
});

server.listen(3000, () => console.log("HTTP + WebSocket rodando!"));